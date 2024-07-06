---
date: 2012-01-24 07:23:00+01:00
dmvpn_tag: design
tags:
- design
- DMVPN
title: Redundant DMVPN Designs, Part 2 (Multiple Uplinks)
url: /2012/01/redundant-dmvpn-designs-part-2-multiple.html
---
In the [*Redundant DMVPN Design, Part 1*](/2012/01/redundant-dmvpn-designs-part-1-basics.html) I described the options you have when you want to connect non-redundant spokes to more than one hub. In this article, we'll go a step further and design hub and spoke sites with multiple uplinks.

### Public IP Addressing

**Fact:** DMVPN tunnel endpoints have to use public IP addresses or the hub/spoke routers wouldn't be able to send GRE/IPsec packets across the public backbone.
<!--more-->
{{<note>}}The *public IP address* in this context is an IP address routable across the Service Provider backbone your routers are connected to. If you run DMVPN over the Internet, then the *public IP address* is a globally routable IPv4 or IPv6 address; if you run DMVPN over an MPLS/VPN infrastructure, then the *public IP address* is whatever IP address is routable across the MPLS/VPN network (it could still be an RFC 1918 IPv4 address).{{</note>}}

Public IP addresses from the service provider PA address space usually get assigned to individual uplinks on the spoke routers. These IP addresses could be static or dynamically allocated through mechanisms like DHCP/DHCPv6, SLAAC or IPCP.

{{<figure src="s1600-DMVPN_1S2U.png" caption="Outside IP addresses are assigned by upstream ISPs">}}

SMB customers not having their own IP address space would most often deploy hub routers with public IP addresses assigned to individual links (similar to spoke sites). Larger organizations with their own IP address space and AS number would use BGP with the upstream service providers and a single IP address (from their IP address space) on the hub router:

{{<figure src="s1600-DMVPN_1H2U.png" caption="IP address on the hub router often belongs the customer public IP prefix">}}

### DMVPN Tunnels on Spoke Sites

**Fact:** DMVPN tunnel endpoints are tied to public IP address and thus to individual uplinks. Uplink failure causes IP address loss and subsequently tunnel interface failure.

**Conclusion**: If you want to maximize the spoke site redundancy, you have to deploy a separate DMVPN tunnel interface on each spoke router uplink.

{{<figure src="s1600-DMVPN_2TP1.png" caption="Maximally redundant design: two DMVPN tunnels">}}

**Fact:** Cisco IOS doesn't allow the same IP subnet to be used on multiple mGRE interfaces.

**Conclusion\#1:** Multiple DMVPN tunnel interfaces deployed on a spoke router have to belong to different IP subnets.

**Conclusion\#2**: You need multiple DMVPN tunnels in your network. The number of DMVPN interfaces on hub routers depends on your resiliency requirements (see below).

{{<figure src="s1600-DMVPN_1S2I2H.png" caption="Simple redundant design with each hub router belonging to one DMVPN tunnel">}}

### Outbound Routing on Spoke Routers

You can never be sure whether the upstream ISPs use RPF filters or other filtering mechanisms. It's thus mandatory to ensure proper outbound packet forwarding over the spoke uplinks: tunnel interface associated with IP address belonging to ISP-A can send packets only over the uplink connecting the spoke router to ISP-A.

You can use [**tunnel route-via** feature](/2010/09/tunnel-route-selection-recording-from.html) to force the tunnel interfaces to use correct uplinks (but it [doesn't work if you use IPsec](/2010/06/tunnel-route-selection-and-dmvpn-tunnel.html)), or you could use VRF-based tunnel interfaces:

-   Create multiple VRFs on the spoke router, one per uplink;
-   Create a static default route in each VRF pointing to the associated uplink;
-   Configure transport VRF on each DMVPN tunnel interface.

{{<note info>}}If you're not familiar with VRFs, use the tested router configurations you get with the [*DMVPN -- from basics to scalable networks*](http://www.ipspace.net/DMVPN) webinar.{{</note>}}

### DMVPN Tunnels on Hub Sites

The number of DMVPN tunnels on the hub sites depends on the DMVPN model you're using (Phase 1/2/3) and the redundancy requirements.

Assuming a two-hub network has to survive a single failure (hub router or spoke uplink), use a single hub per DMVPN tunnel (unless you\'re using Phase 3 DMVPN, in which case all hub routers probably have to be connected to all tunnels).

{{<figure src="s1600-DMVPN_2TP2.png" caption="Simple redundant design: two DMVPN tunnels, one hub per tunnel">}}

Spoke uplink failure will not isolate a spoke (it still has the other uplink), hub router failure will also not break the network (spokes can still communicate through the other hub). However, a worst-case combination of hub router and spoke uplink failure might isolate a spoke site.

If your network has to be more failure-resilient, connect all hubs to all DMVPN tunnels. This design will be able to survive multiple failures (including a concurrent hub router and spoke uplink failure).

{{<figure src="s1600-DMVPN_2IF2T.png" caption="More redundant design: both hub routers participate in both tunnels">}}

Finally, if you're using DMVPN Phase 2, you might need to deploy even more tunnels to avoid the [NHRP convergence problems](/2011/05/nhrp-convergence-issues-in-multi-hub.html). In our sample network you would need two DMVPN tunnels on each hub router (one for ISP-A spoke uplinks, the other one for ISP-B spoke uplinks) and four tunnels on the spoke routers (one for each uplink/hub combination).

### Alternate Solution: VRF Fiesta

*KAV* proposed an alternate solution in a comment to the [*Redundant DMVPN Design, Part 1*](/2012/01/redundant-dmvpn-designs-part-1-basics.html) post: put each DMVPN tunnel interface in a separate VRF and use redistribution through BGP in a VRF-lite environment to collect routes from both DMVPN VRFs in the LAN-side VRF.

**Advantage:** since each DMVPN tunnel belongs to a different VRF, you can use the same IP subnet on all spoke-router tunnels, minimizing the overall number of DMVPN tunnels (you can use a single DMVPN subnet if you're running Phase 1 or Phase 3 DMVPN).

**Drawback:** you need between three and five VRFs (three to support this design, two more for split default routing in Phase 2/3 DMVPN) on the spoke routers and route redistribution through BGP. Guess whose phone will ring when a spoke router experiences "mission-critical" problems at 2AM.

### Need Help?

Start with the [*DMVPN Technology and Configuration*](http://www.ipspace.net/DMVPN) webinar; it probably contains 95% of what you need to know about DMVPN (the [*DMVPN New Features*](http://www.ipspace.net/DMVPN_New_Features) one describes DMVPN features introduced in IOS releases 15.x). The [*Enterprise MPLS/VPN Deployment*](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment) webinar describes everything you ever wanted to know about VRFs, VRF-Lite and tunnel interfaces running inside and over VRFs. You get access to all three webinars with the [yearly subscription](http://www.ipspace.net/Subscription).
