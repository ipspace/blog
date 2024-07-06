---
date: 2018-04-04 10:38:00+02:00
dcbgp_tag: design
evpn_tag: design
series:
- dcbgp
series_weight: 800
tags:
- design
- BGP
- EVPN
title: BGP in EVPN-Based Data Center Fabrics (Updated)
url: /2018/04/bgp-in-evpn-based-data-center-fabrics.html
---
My [BGP in EVPN-Based Data Center Fabrics](/2018/01/bgp-in-evpn-based-data-center-fabrics.html) blog post generated numerous comments from engineers disagreeing with my views on using IBGP-over-EBGP.

As usual, there were three kinds of comments:
<!--more-->
-   People like [Alexander Grigorenko](https://www.linkedin.com/in/grigorenkoae/) arguing with the technical merits of what I wrote (Alex published a [blog post describing his perspective](http://jncie.tech/2018/01/28/bgp-design-options-for-evpn-in-data-center-fabrics/)). They were right -- I should have spent more time on the details;
-   People like Paul [saying](/2018/01/bgp-in-evpn-based-data-center-fabrics.html?showComment=1521833306308#c5055854090187969717) "while I understand your discussion, nothing else would work for my fabric". Fair point -- if you have to carry 1M prefixes around you cannot use generic design guidelines found on the Internet;
-   Anonymous commenters being annoyed because I called their baby ugly (more about this in another blog post).

Anyway, Alex' comments triggered a major rewrite of the [BGP in EVPN-Based Data Center Fabrics](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) section of [Using BGP in Data Center Leaf-and-Spine Fabrics article](http://www.ipspace.net/Data_Center_BGP). It took me a long time to figure out how to structure it, and then more than a week ironing out the kinks based on feedback from people way closer to actual BGP source code than I ever was.

The [new version of the document is online](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics). There are still a few missing bits and pieces, like route target implications of using numerous AS numbers in a single EVPN fabric, or performance differences between IBGP and EBGP-based EVPN designs.

For even more details, watch [*EVPN Technical Deep Dive*](http://www.ipspace.net/EVPN_Technical_Deep_Dive) and [*Leaf and Spine Architectures*](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinars (both part of [ipSpace.net subscription](http://www.ipspace.net/Subscription)).

{{<jump>}}
[More...](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics)
{{</jump>}}
