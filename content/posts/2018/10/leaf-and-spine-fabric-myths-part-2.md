---
date: 2018-10-10 09:04:00+02:00
dcbgp_tag: design
series:
- dcbgp
series_weight: 600
tags:
- design
- data center
- fabric
- BGP
title: Leaf-and-Spine Fabric Myths (Part 2)
url: /2018/10/leaf-and-spine-fabric-myths-part-2/
---
The next set of [Leaf-and-Spine Fabric Myths](/2018/10/leaf-and-spine-fabric-myths-part-1/) listed by [Evil CCIE](/2018/06/is-ebgp-really-better-than-ospf-in-leaf/#c4430946733793890437) focused on BGP:

> BGP is the best choice for leaf-and-spine fabrics.

I wrote about this particular one [here](/2018/06/is-ebgp-really-better-than-ospf-in-leaf/). If you're not a BGP guru don't overcomplicate your network. OSPF, IS-IS, and EIGRP are good enough for most environments. Also, don't ever [turn BGP into RIP with AS-path length serving as hop count](/2018/09/implications-of-valley-free-routing-in/).
<!--more-->
> BGP is a good choice as it allows granular policy control

As anyone who ever tried to implement a consistent QoS policy across a large network knows **maintaining a policy and adjusting it** **to changing conditions** **quickly becomes a huge operational burden**. In most data center environments it's cheaper to buy more bandwidth.

Also, don't believe in the magic [powers of intent-based networking](/2018/06/what-is-intent-based-networking/). I [explained the drawbacks of this idea](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar, here's the TL&DW summary: it will probably cost you more than buying faster leaf-to-spine links.

Finally, the next time a \$vendor Sales Engineer makes this argument, quote RFC 1925 Rule 4 and ask him when was the last time he was maintaining a complex policy in a production environment for more than a few years (and how painful it was).

> BGP has less churn

Assuming you care. Most enterprise environments need layer-2 fabrics anyway, which usually translates into VXLAN overlay these days. It doesn't matter whether you use static VXLAN ingress replication lists or EVPN -- the core OSPF process doesn't need more than a single router LSA per switch.

> BGP scales far better

In principle, it's true. In practice, most environments don't need that scale. I asked that same question several times in [RIFT](/2018/03/data-center-routing-with-rift-on/) and [OpenFabric](/2018/04/openfabric-with-russ-white-on-software/) podcasts and we came to an agreement that decent OSPF implementations shouldn't have a problem with a few hundred switches in the same area. Dinesh Dutt also had [quite a few things to say about the *BGP-is-my-hammer-where's-the-nail* approach](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on/).

### Now What?

As far as I can see, you have (approximately) four options when selecting the underlay routing protocol:

-   [You don't need more than two switches](https://www.ipspace.net/Optimize_Data_Center_Infrastructure), making all design discussions moot;
-   You select OSPF, IS-IS or EBGP based on the last blog post you found on the Internet... and get the fabric you deserve ;)
-   You use EBGP because you trust your \$vendor;
-   You figure out how data center fabrics really work (if you do them right, they are nothing more than simple IP networks), and then use the routing and switching knowledge you already have to design them.

If you decide to take the red pill (last option), you might find the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) and [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinars useful. They are both part of [Standard ipSpace.net subscription](https://www.ipspace.net/Subscription).
