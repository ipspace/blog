---
anycast_tag: fabric
date: 2013-05-29 07:14:00+02:00
series:
- anycast
tags:
- data center
- ARP
- fabric
- IP routing
title: Optimal L3 Forwarding with VARP and Active/Active VRRP
url: /2013/05/optimal-l3-forwarding-with-varp-and.html
---
I've blogged about the [need for optimal L3 forwarding across the whole data center](/2012/05/does-optimal-l3-forwarding-matter-in.html) in 2012 when I introduced it as one of the interesting requirements in [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar. Years later, the concept became one of the cornerstones of modern EVPN fabrics, but there are still only a few companies that can deliver this functionality in a more traditional environment.
<!--more-->
Fabric solutions that appear as a single system to the outside world usually offer optimal L3 forwarding. These solutions include:

-   Stacking ToR switches and [other similar solutions](/2010/10/multi-chassis-link-aggregation-stacking.html), including HP IRF and Juniper's Virtual Chassis) definitely fall in this category (note: [using stacked switches or virtual chassis architectures with ring-based interconnect in environments with heavy east-west traffic is NOT a good idea](/2012/11/stackable-data-center-switches-do-math.html));
-   Other architectures that present the whole fabric as a single layer-3 entity like [Juniper's QFabric](/2011/09/qfabric-part-3-forwarding.html) (now mostly obsolete).

While optimal L3 forwarding with anycast first-hop gateways became a table stake for EVPN implementations, and most vendors offer [active/active first-hop gateways in MLAG clusters](/2022/06/mlag-active-active-layer3.html), there are only a few companies I'm aware of that can implement anycast gateways across a traditional layer-2 fabric: [Arista with Virtual ARP](/2013/06/arista-eos-virtual-arp-varp-behind.html), Cumulus Linux with Virtual Router Redundancy, and Enterasys (now Extreme) with Fabric Routing.

[Arista's Virtual ARP](/2013/06/arista-eos-virtual-arp-varp-behind.html) is extremely simple[^CL] -- it's like VRRP without VRRP. You have to configure the same IP address (first-hop gateway) on a VLAN interface of all ToR switches with **ip virtual-router address** configuration command and associate a MAC address with the shared IP address with the **ip virtual-router mac-address** interface configuration command.

[^CL]: Cumulus Linux Virtual Router Redundancy is functionally equivalent to Arista's Virtual ARP.

The first switch that is hit with an ARP request for the shared virtual IP address will reply with the shared MAC address (I'm not sure about the details -- it might well be that the ARP broadcast gets flooded to all switches, in which case the sender gets numerous replies). When a host sends an IP packet to that same shared MAC address, the first ToR switch that the packet hits intercepts the packet (because it's listening to the shared MAC address), and performs L3 routing.

{{<figure src="/2013/05/s1600-Slide+-+Arista+EOS+VARP.jpg" caption="Arista EOS Virtual ARP">}}

Things might get nasty if you have configuration mismatches -- for example, missing **ip virtual-router address** configuration on one of the ToR switches. Make sure you use some sort of automation or orchestration system to configure the ToR switches.

### Revision History

2023-02-01
: * Removed mentions of obsolete products/startups.
  * Added a mention of Cumulus Linux VRR.
  * Added a link to VARP deep dive blog post
