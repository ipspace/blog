---
title: "Leave BGP Next Hops Unchanged on Reflected Routes"
date: 2022-10-27 06:38:00
tags: [ BGP ]
---
Here's the last question I'll answer from that [long list Daniel Dib posted weeks ago](https://twitter.com/danieldibswe/status/1579674196833366017) ([answer to Q1](/2022/10/ospf-external-routes.html), [answer to Q2](/2022/10/ibgp-full-mesh.html)).

> I am trying to understand what made the BGP designers decide that RR should not change the BGP Next Hop for IBGP-learned routes.

{{<note>}}If anyone wants to have the answer to the very last question in Daniel's list, they're free to search for "BGP Next Hops" on my blog and start exploring. Studying OSPF Forwarding Address might provide additional clues.{{</note>}}
<!--more-->
As always, there are (at least) two answers to that question:

* BGP route reflectors are solving the "propagation of information" problem, not the "finding the optimal path" problem. Think of them as the flooding part of OSPF, not the SPF part.
* You might not want to bring all the traffic to the route reflector, inspect it there[^WTD], and send it to the egress router.

[^WTD]: What else could you do once you pulled it there? The poor route reflector has to figure out where to send it next, and to do that in needs to do a full lookup.

That last bit was especially true in the days of yore when the routers forwarded packets in software[^SDN]. Core routers needed all the performance they could squeeze out of their software, which meant more expensive CPUs and really expensive high-speed memory. Nobody thought about wasting all that hardware on calculating and disseminating BGP routes -- route reflectors were often placed outside of the forwarding path. Changing BGP next hop on reflected routes to put an underpowered device into the forwarding path was a perfect recipe for disaster.

{{<note warn>}}Advertising an out-of-forwarding-path IP address as the next hop for a destination would also result in a wonderful routing loop. The proof is left as an exercise for the reader.{{</note>}}

[^SDN]: ... and we weren't arrogant enough to call that *Software-Defined Networking*.

The days have changed, high-speed packet forwarding is done in hardware[^SDX], and it doesn't matter which device in the network is used as a route reflector. Most data center switching vendors that publish designs combining IBGP with IGP deploy BGP route reflectors on spines (because the CPU on the spines has nothing to do anyway). In that case, it might be OK to change the BGP next hops on spines -- every IP packet has to cross a spine switch anyway, so who cares. However, the kids who want to look really cool build their fabrics with EBGP, and don't care about route reflectors anyway.

[^SDX]: ... and *Software-Defined Networking* means whatever a funding-desperate startup is doing.

Even in leaf-and-spine fabrics you don't want to mess with the BGP next hops if you're doing anything else but pure IP transport. MPLS is so last millennium, so let's take the new kid on the block: SRv6. Assume you're building Ethernet-over-SRv6 service with EVPN control plane[^JS]. Do you really want all tenant packets to land on the spine switches for further inspection and forwarding? You do? Then why exactly did you waste millions on SRv6-capable gear in the first place? You could have bought the cheapest white box switches and run bridging on them.

Also, are you sure you want to have all VLANs and VRFs defined on the spine switches? If you don't have them configured, the spine switch cannot figure out what to do with the packets rushing to it.[^FTT]. Finally, do you want to pollute the spine forwarding tables with MAC+IP addresses and prefixes from every tenant?

[^JS]: What else could give you such a cushy job security?

[^FTT]: Such a setup would be a doozy to troubleshoot

The same reasoning applies to more mundane technologies like VXLAN.

**Long story short**: Don't you dare to change the BGP next hop in the middle of the fabric.

Totally off-topic: The above requirement trips all the cool kids who were so proud of their EBGP-only fabrics, because EBGP loves changing BGP next hops. There's a single vendor I'm aware of who realized the SNAFU and implemented EVPN in a way that violates the usual EBGP expectations. Everyone else has to deal with awkward configurations or crazy stuff like IBGP sessions between loopbacks advertised with EBGP... and every now and then a senior manager working for a large vendor gets extremely upset when I call that concoction stupid.

Anyway, back to BGP route reflectors. By now you should be able to explain why it's a bad idea to change the BGP next hop on reflected routes, but there's a single scenario I'm aware of where doing that is a must: [hub-and-spoke DMVPN tunnels](/2014/04/changes-in-ibgp-next-hop-processing.html). I'm guessing a similar reasoning applies if you bought hub-and-spoke (E-tree) Carrier Ethernet service. Anything else? Please leave a comment!
