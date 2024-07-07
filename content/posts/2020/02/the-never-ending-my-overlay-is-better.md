---
date: 2020-02-18 08:05:00+01:00
tags:
- VXLAN
- overlay networks
- NSX
title: The Never-Ending "My Overlay Is Better Than Yours" Saga
url: /2020/02/the-never-ending-my-overlay-is-better/
---
I published a [blog post describing how complex the underlay supporting VMware NSX still has to be](/2020/02/do-we-need-complex-data-center-switches/) (because someone keeps pretending a network is [just a thick yellow cable](/2015/02/lets-get-rid-of-thick-yellow-cable/)), and the [tweet announcing it](https://twitter.com/ioshints/status/1227504195701362691) admittedly looked like a clickbait.

> \[Blog\] Do We Need Complex Data Center Switches for VMware NSX Underlay

[Martin Casado](https://twitter.com/martin_casado) quickly replied **NO** (probably before reading the whole article), starting a whole barrage of overlay-focused neteng-versus-devs fun.
<!--more-->
{{<note>}}
While I [loved the concept Nicira worked on](/2011/10/what-is-nicira-really-up-to/), the [execution wasn't exactly stellar](/2014/11/open-vswitch-performance-revisited/), and once it got merged with traditional VMware approach to networking we got what I [described](/2020/02/do-we-need-complex-data-center-switches/). The end result makes me infinitely sad every time I think about its potentials... but then that water has long reached the ocean.
{{</note>}}

The best response to Martin's claim was [made by Mat Jovanovic](https://twitter.com/matjovanovic/status/1227840092108140546):

> Depends... Are we looking at a PPT, or a "I've tried it on a commodity underlay" version of the answer? Something tells me it's quite different...

In the meantime, the debate veered into "my overlay is better than your overlay", [starting with](https://twitter.com/martin_casado/status/1227793721019600897) Martin\'s claim that:

> Good news for you -- there are many fast growing overlay solutions that are adopted by apps and security teams and bypass the networking teams altogether.

Martin furthermore [pointed to Nebula](https://twitter.com/martin_casado/status/1227794153179795456) as one of his favorites. I did a quick look at their [GitHub repo](https://github.com/slackhq/nebula), and it looks like they did things the right way and [built a badly needed session layer](/2009/08/what-went-wrong-tcpip-lacks-session/).

However, being sick-and-tired of everyone claiming how great it is to build overlays on top of overlays (like we didn't learn anything in the decades [building GRE and IPsec tunnels](/2011/03/mplsvpn-over-gre-over-ipsec-does-it/)), I decided to [troll a bit more](https://twitter.com/ioshints/status/1227837256779681797):

> We had a fast-growing overlay solution in 1970s. It was called TCP. I've heard it might still be used. Why do people insist of heaping layers upon layers instead of writing decent code?

Martin\'s response [was almost as-expected](https://twitter.com/martin_casado/status/1227842655725350912):

> App developers : "I've created this amazing overlay solution that solves a bunch of our problems"
>
> Networking : "TCP has been around since the 70's, write better code"
>
> ... this is why you're not being invited to the party ;)

Someone must have had some traumatic experiences\... Anyhow, as you probably know I'm well-aware of the popularity of pointing out the state of Emperor's wardrobe (or lack thereof), and I'm way too old for FOMO, so I don't care what parties I get invited to.

However, what makes me truly sad is watching highly intelligent people ignorant of environmental limitations (see also: [fallacies of distributed computing](/2020/01/video-fallacies-of-distributed-computing/) and RFC 1925 rule 4) reinventing the wheels, and ending with what we already had (in a different disguise, see also RFC 1925 rule 11) after spending years figuring it out and repeating the mistakes we made in the past.

For example:

-   *We won't use DNS* (for whatever made-up reason), because we believe in IP addresses. Years later: We don't care about stinking IP addresses anymore, we have Consul (hint: ever heard of SRV records?)
-   *We tied everything to IP addresses*, so you [better move them across the globe](/2015/02/before-talking-about-vmotion-across/) and [into public clouds](/2019/11/stretched-layer-2-subnets-in-azure/), and [you can't change them when doing disaster recovery](/2019/12/you-dont-need-ip-renumbering-for/). Years later: containers are cool, and we use Consul anyway, so it's perfectly fine to hide a dozen of thingies behind the same IP address.
-   *We'll implement our own overlay* because your overlay sucks. Years later: OMG, [VXLAN has no security](/2015/04/omg-vxlan-encapsulation-has-no-security/), as [security researches tend to find out every other year or so](/2018/11/omg-vxlan-is-still-insecure/).
-   [Centralized control plane](/2014/05/does-centralized-control-plane-make/) is the way to go. Years later: Ouch, scalability and latency suck. Maybe we should focus on automation\... or intent\... or policies\... or whatever.

The networking engineers should know better, but even they can't resist the lure of reinventing broken wheels, for example overlays with cache-based forwarding like LISP. No surprise, such solutions quickly encounter endpoint liveliness problem (and a [few others](https://tools.ietf.org/html/draft-meyer-loc-id-implications-01)).

**Notes:**

-   I'm guessing LISP is not yet widespread enough to encounter severe cache trashing behavior that still triggers PTSD in anyone remotely involved in the days when Fast Switching crashed the Internet. That rerun might be fun to watch...
-   Of course I probably messed up at least some of these examples, so please feel to correct me in the comments.

Now here's a crazy idea: what if we'd start communicating with people who understand how stuff works, learn from them, and implement stuff in an optimal way. IT seems to be one of the few areas where we allow people to build sandcastles and ignore the tides, and then [blame someone else when the water inevitable arrives](/2013/04/this-is-what-makes-networking-so-complex/).

