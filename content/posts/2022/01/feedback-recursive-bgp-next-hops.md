---
date: 2022-01-12 06:27:00+00:00
dcbgp_tag: details
series:
- dcbgp
tags:
- BGP
title: 'Feedback: Recursive BGP Next Hop Resolution'
---
The _[Recursive BGP Next Hops: an RFC 4271 Quirk](/2022/01/bgp-recursive-next-hops-rfc.html)_ blog post generated tons of feedback (thanks a million to everyone writing a comment on my blog or [LinkedIn](https://www.linkedin.com/feed/update/urn%3Ali%3Aactivity%3A6884535946654572544/)).

Starting with [Robert Razsuk](/2022/01/bgp-recursive-next-hops-rfc.html#956) who managed to track down the [original email](https://mailarchive.ietf.org/arch/msg/idr/OHlGLdQOF5lSa_NR7oOaDjse8y8/) that triggered the (maybe dubious) text in RFC 4271:

> The text in section 5.1.3 was not really targeting to prohibit load balancing. Keep in mind that it is FIB layer which constructs actual forwarding paths.
>
> The text has been suggested by Tom Petch in discussion about BGP advertising valid paths or even paths it actually installs in the RIB/FIB. The entire section 5.1.3 is about rules when advertising paths by BGP.
<!--more-->
As expected, [Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501/) added tons of behind-the-scenes details:

> First, if you go over vanilla IGP (which is normal) you'll get ECMP anyway ;-) The discussion starts to get very hairy if you resolve over next-hop that has multiple protocols underlying and similar interesting things like MPLS shortcuts (that's the preference stuff and multiple RIB resolutions that no RFC really explains since it's really implementation dependent and what differentiates a heavy lift routing device vs. a home router ;-).
>
> And more such non-trivial cases exist so first/best entry only is a safe choice (but Dr. Li as co-author may have some further comment here ;-) Beyond that, all serious stacks do all kind of load balancing across e-bgp, i-bgp and all kind of mixed 2547 paths (@ least our does ;-). Just look for the sharp-edged knobs like "multipath vpn-unequal-cost equal-external-internal" ;-) Mileage may vary and when doing this one has to understand that those knobs are peeling all kind of yellow stickers off that prevent looping in default case ;-)

A quick illustration of how complex things can get was supplied by [Blake Willis](https://www.linkedin.com/in/blakedot/): guess what happens when a BGP next hop is resolved over another BGP prefix that has multiple resolved paths. Junos has a [nerd knob just for that edge case](https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/load-balancing-bgp-session.html#id-configuring-recursive-resolution-over-bgp-multipath).

Finally, [Bela Varkonyi documented](/2022/01/bgp-recursive-next-hops-rfc.html#960) that if one reads the BGP RFC with rosy (and a bit creative) glasses, it's perfectly fine to do load balancing over IGP next hops for a particular BGP next hop... just imagine you're doing the recursive next hop calculation every time you need it (example: for every packet):

> Load balancing is still possible depending on the implementation. If you make a single lookup for a specific next hop address for all occurrences and cache this even for later use, then of course this would disable load balancing since you would get the same answer for all occurrences. But it is not prescribed. You can do an independent recursive lookup for each next hop occurrence when it is needed. Then you can pickup a different single lookup result for each individual query from multiple possible choices. This is still load balancing that is not violating section 5.1.3.
>
> The behavior all depends on how do you generate FIB entries from the RIB. You should not store and cache next hop lookups, but rather do the lookup every time independently when you need it. However, you would need some logic that returns a different value for the lookup on the same next hop at each query.

Obviously you wouldn't do anything along those lines if you need high-speed forwarding, but you could precalculate all possible results and store them into a forwarding structure, which we happen to call *hierarchical FIB*.

And yes, we are discussing how many [angels can dance](https://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F) on an ASIC, but one should have a bit of nerdy fun every now and then ;)
