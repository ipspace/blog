---
date: 2020-05-21 07:03:00+00:00
dcbgp_tag: design
evpn_tag: design
mlag_tag: design
series:
- mlag
- dcbgp
series_weight: 800
tags:
- BGP
- EVPN
- data center
- fabric
- design
title: BGP AS Numbers on MLAG Members
---
I got this question about the use of AS numbers on data center leaf switches participating in an MLAG cluster:

> In the _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ you [made the recommendation](https://my.ipspace.net/bin/get/Clos/7.12%20-%20Routing%20Protocol%20Selection.mp4?doccode=Clos) to have the same AS number on all members of an MLAG cluster and run iBGP between them. In the _[Autonomous Systems and AS Numbers](https://www.ipspace.net/Data_Center_BGP/Autonomous_Systems_and_AS_Numbers)_ article you discuss the option of having different AS number per leaf. Which one should I use… and do I still need the EBGP peering between the leaf pair?

As always, there’s a bit of a gap between theory and practice ;), but let's start with a leaf-and-spine fabric diagram illustrating both concepts:
<!--more-->
{{<figure src="https://www.ipspace.net/wk/images/thumb/9/9c/Shared_versus_Unique_AS_Numbers.png/600px-Shared_versus_Unique_AS_Numbers.png" caption="Unique versus shared AS Numbers" >}}

**In theory**, it feels right to have the same AS number for all members of an MLAG cluster (L3 and L4 in the above diagram). After all, they advertise the same subnets. If you go for that design, run IBGP on the peering link.

**In practice**, dealing with “these two switches have to have the same AS number” creates additional complexity when you want to standardize configurations as well as corner cases in configuration templates. After a lengthy discussion with [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt) we came to the conclusion that while using different AS numbers on MLAG members (L1 and L2 in the above diagram) doesn’t feel right from BGP perspective, simplified configurations might be more important.

Regardless of which design you choose, you still need BGP peering between MLAG members. One of them might lose a subnet (all ports in the subnet VLAN) and needs to know its peer still has it. However, there’s any need for additional filtering on the inter-leaf BGP session. In the EBGP case, the leaf-to-spine path will always be better (due to shorter AS path length) than leaf-leaf-spine path; in the IBGP case the external path will be preferred over the internal one.

### More Details

* Start with the [Data Center BGP](https://www.ipspace.net/Data_Center_BGP/) article
* Explore [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar
* If you're interested in deploying EVPN in your data center fabric, I can highly recommend the [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar

Need even more details? Explore our _[BGP in Data Center Fabrics ](/series/dcbgp/)_ series.