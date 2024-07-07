---
date: 2016-06-08 08:27:00+02:00
dcbgp_tag: rant
series:
- dcbgp
tags:
- SDN
- BGP
title: Is BGP Really that Complex?
url: /2016/06/is-bgp-really-that-complex/
---
Anyone following the popular networking blogs and podcasts is probably familiar with the claim that BGP is way too complex to be used in whatever environment. On the other hand, more and more smart people use it when building their data center or WAN infrastructure. There's something wrong with this picture.
<!--more-->
### BGP Is Complex

There's no doubt about that. BGP is complex enough to make a week-long course out of it (trust me, I created at least two of them). However, most of that complexity comes from the initial BGP use case: inter-domain routing driven primarily by the needs of routing policies.

To make matters worse, various service providers pushed vendors to implement ever-more-intricate nerd knobs instead of solving the problem the right way: building a policy server (call it an SDN controller to make marketers ecstatic) that acts as a BGP route reflector and tweaks the updates sent to individual BGP routers to enforce the desired routing policy.

However, when you start using BGP as a simple endpoint reachability distribution mechanism (example: running BGP over large DMVPN cloud), most of its intricacies become unnecessary, and you're left with an elegant and simple protocol, combining the simplicity of RIP with versatility of OSFP or IS-IS.

### Know Your Tools

A good craftsman knows his tools and uses the tool that's best suited for the job at hand (a screw needs a screwdriver even if the closes tool is a hammer). A networking engineer should do no less, even though some people believe in universality of their preferred tool. Well, while there are universal tools out there, they tend not to be good at any particular job.

{{<figure src="/images/swiss-army-knife.jpeg" caption="A magic tool that does 140 things miserably">}}

Back to the routing protocols:

-   If you have a complex haphazard mesh of links of various speeds, use OSPF or IS-IS. They were designed for that job.
-   If you have to carry a large set of prefixes within your routing domain, use IBGP on top of OSPF or IS-IS. IBGP will have no problems carrying the prefixes, and OSPF or IS-IS will do a good job finding the optimal path.
-   If you have a large highly symmetrical fabric, BGP is a perfect tool for the job, particularly when combined with BFD.

### Those Pesky Implementation Details

You might have network design that's a perfect match to BGP's capabilities, and yet you're hesitating because BGP configuration quickly becomes a nightmare. Time to shop around; there are vendors who realized BGP configuration tools designed for the initial inter-AS BGP use case don't cut it when we want to deploy BGP in the data centers.

For example:

-   Cisco implemented dynamic BGP neighbors in Cisco IOS at least twice. Together with the [changes to BGP route reflector functionality](/2014/04/changes-in-ibgp-next-hop-processing/) they make [BGP-over-DMVPN deployments almost trivial](/2014/03/scaling-bgp-based-dmvpn-networks/);
-   Cumulus Linux implemented [BGP over unnumbered interfaces](/2015/02/bgp-configuration-made-simple-with/), and relaxed the remote AS checking -- you have to specify whether the neighbor is internal or external, and the BGP routing daemon does the rest;

For more details, start with the [Simplifying BGP Configurations](https://my.ipspace.net/bin/get?doc=46d9b3b4-e1ea-11e5-a2b0-005056880254) video in which Dinesh Dutt explains how easy it is to run BGP in a leaf-and-spine fabric, and continue with the rest of the [Leaf-and-Spine Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.

Finally, do read the [BGP: Application Networking Dream](https://networkingnerd.net/2016/05/17/bgp-the-application-networking-dream/) by [Tom Hollingsworth](https://networkingnerd.net/about/).
