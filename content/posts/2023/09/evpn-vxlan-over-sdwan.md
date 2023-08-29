---
title: "Does EVPN/VXLAN over SD-WAN Make Sense?"
date: 2023-09-17 11:43:00
tags: [ VXLAN, EVPN, SD-WAN ]
draft: True
---
SD-WAN’s tight, proprietary integration goes beyond ease-of-use. Here are two technical benefits that would be impossible with RFC standards alone:

1.  Packet duplication and deduplication, a la [Cisco Viptela SDWAN](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/ios-xe-17/policies-book-xe/packet-duplication.pdf){style="color: blue; text-decoration: underline;"}.  The sdwan ingress node sends a packet across all available links and the sdwan egress node forwards only the first one that makes it. This is especially helpful for time-sensitive voice/video packets on miserable internet links. It wastes bandwidth, for sure,  but the end result is far superior to FEC used by several other SDWAN vendors. (technically, RFCs 7197 and 7198 to touch on this approach but without path awareness and acting primarily at the endpoint)
2.  MTU interworking, a la [Silverpeak (p 36)](https://www.silver-peak.com/sites/default/files/userdocs/appliancemgr_operators_guide_menus_r8-0_revq_may2016.pdf){style="color: blue; text-decoration: underline;"}  (also supported by [Velocloud](https://docs.vmware.com/en/VMware-SD-WAN/4.2/VMware-SD-WAN-Administration-Guide/GUID-72AA55E3-C0F4-4E0A-BFBC-E4077E0F4D6E.html){style="color: blue; text-decoration: underline;"} and [Citrix](https://support.citrix.com/article/CTX236976){style="color: blue; text-decoration: underline;"} using different terminology).   The sdwan ingress node can receive jumbo MTU packets on the LAN, forward it over small MTU SDWAN, and reassemble the jumbo packet on sdwan egress.      (technically, RFC standards could do this if a router honored an order-of-operation to tunnel, fragment, and then encrypt. -- but none do, AFAIK)

The frustrating part of proprietary is that these nerdy “secret sauces” can’t easily be compared across vendors.  E.g., if I need to run EVPN/VXLAN over the WAN, I will want the behavior of “MTU interworking”  But how do I ask my vendors if they support it? I can’t say “MTU interworking” since that term only gets six hits on google.  I can describe the behavior I want, but 99% of SE’s will misunderstand and reply “yeah, we do fragmentation” or “we support jumbo frames.”  My only option is to do a labor-intensive documentation review, proof-of-concept, or otherwise become the smartest guy in the room.

---

Also, the EVPN-over-WAN idea is not hypothetical since EVPN+VXLAN is now the easiest way to build L3VPN with data center switches that don’t support MPLS LDP.  I.e., folks with no interest in EVPN’s L2 features are still using it for L3VPN.
 
As an aside, a few years ago I penned a blog on Cisco ACI versus EVPN that touched on technical, operational, and business factors. It has a few gaffes and poor wordings, but has mostly held up well. https://www.cdw.com/content/cdw/en/articles/datacenter/choosing-your-next-data-center-fabric-ciscos-aci-or-evpn-part-1.html
 
 
