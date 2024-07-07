---
date: 2018-09-24 09:00:00+02:00
evpn_tag: intro
tags:
- VXLAN
- data center
- fabric
- EVPN
title: VXLAN Broadcast Domain Size Limitations
url: /2018/09/vxlan-broadcast-domain-size-limitations/
---
One of the attendees of my [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course tried to figure out whether you can build larger broadcast domains with VXLAN than you could with VLANs. Here's what he sent me:

> I'm trying to understand differences or similarities between VLAN and VXLAN technologies in a view of (\*cast) domain limitation.

There's no difference between the two on the client-facing side. VXLAN is just an encapsulation technology and doesn't [change how bridging works](/2010/07/bridging-and-routing-is-there/) at all (read also [part 2](/2010/07/bridging-and-routing-part-ii/) of that story).
<!--more-->
The only difference between VLAN-based fabric and VXLAN-based fabric is the core transport. VLAN-based fabric uses STP/MLAG in the fabric core, TRILL/SPB/... based fabrics use their own routing protocols, and VXLAN uses IP routing. Edge flooding and learning behavior remains the same.

{{<note info>}}I covered the basics of TRILL and SPB (in case anyone is still interested) in [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar. Roger Lapuh did a [deeper dive into SPB](https://my.ipspace.net/bin/list?id=Clos#L2_FABRIC) during his presentation @ [Leaf-and-Spine Fabrics webinar](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures). His presentation is accessible with [free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}

[EVPN is a different story](https://www.ipspace.net/EVPN_Technical_Deep_Dive) as it's IP aware, but keep in mind that EVPN became SIP of Networking; every implementation supports a different subset of features.

Several EVPN-based fabrics support ARP proxy at the fabric edge, reducing the number of broadcasts caused by ARPs... assuming someone is not ARPing for a non-existent IP address, in which case you'd probably see those ARPs flooded. Test, test, test... and make sure you also test all possible crazy scenarios.

EVPN-based fabric could implement pure IP transport and turn off flooding altogether, turning what looks like a VLAN into stable routed IP network (admittedly doing routing on host routes). I don't think any vendor is brave enough to do that.

> Yes, we know and understand why we should keep VLAN size limited (let's say 1K hosts/guests/) but what about VXLAN segment size?

[The same limitations apply](/2016/02/vlans-and-failure-domains-revisited/). Although EPVN-based fabrics (whether using VXLAN, MPLS or GRE) could reduce the amount of ARP traffic, there's nothing stopping a single host from blasting the network with a gazillion RARPs per second (because why not) and impacting everyone else in the same segment.

> Am I right that from business risk perspective I should keep VXLAN domain small as well because someone or something can impact all my 12.000 VM\'s in one VXLAN? Or is this technology resistant against broken frames/packets, flooding...?

[A single flooding domain is a single failure domain](/2012/05/layer-2-network-is-single-failure/). A VXLAN VNI (unless turned into a pure routed solution) is a single flooding domain regardless of what the fabric and microsegmentation vendors are telling you. QED.

**Long story short**: Bridging doesn't scale. [Keep your failure domains small](/2014/02/keep-your-failure-domains-small/).
