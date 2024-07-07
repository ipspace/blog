---
title: "EVPN Rerouting After LAG Member Failures"
date: 2024-05-22 08:51:00+0200
mlag_tag: failure
series:
- mlag
tags:
- switching
---
In the previous two blog posts ([Dealing with LAG Member Failures](/2024/05/mlag-lag-member-rerouting/), [LAG Member Failures in VXLAN Fabrics](/2024/05/mlag-vxlan-rerouting/))  we discovered that it's almost trivial to deal with a LAG member failure in an MLAG cluster *if we have a peer link between MLAG members*. What about the holy grail of EVPN pundits: ESI-based MLAG with no peer link between MLAG members?
<!--more-->
{{<figure src="/2024/05/mlag-evpn-only.png" caption="EVPN-based MLAG">}}

{{<note warn>}}EVPN-based MLAG has numerous challenges. [We discussed them in the past](/2022/11/mlag-vxlan-evpn/). This blog post will focus solely on rerouting after a LAG member link failure.{{</note>}}

**Before moving on:** A huge THANK YOU to [Craig Weinhold](https://www.linkedin.com/in/craig-weinhold-0230236/), who did fantastic research on the topic and sent me most of the external links.

Back to EVPN. In our setup:

* S1 and S2 might both advertise MAC-A; if they do, the next hops will be different unless you're using anycast VTEP IP addresses. The type-2 routes include Ethernet Segment Identifier (ESI) to make the active-active multihoming magic work.

{{<note info>}}Please note that only one of the switches may advertise type-2 route for MAC-A.{{</note>}}

* S1 and S2 advertise the link (Ethernet Segment) to A with type-4 EVPN route, allowing other nodes to figure out they can do load balancing across the two VTEPs (assuming the ASIC supports that)
* S1 and S2 figure out who the Designated Forwarder for the segment is. Even though they both receive BUM frames for the VLANs in which A participates, only one of them sends them to A.

For more high-level details, read the excellent [Multihoming Models with EVPN](https://www.arista.com/assets/data/pdf/Whitepapers/EVPN-DC-Multihoming-for-Resiliency-WP.pdf) whitepaper. If you want even more information, I'm sure you'll find it; there are plenty of *let's dive into EVPN and dissect it* articles on the Internet. 

Now let's assume the S1-A link fails, resulting in a flurry of EVPN BGP updates. S1 revokes the type-4 (ESI) route for the S1-A link and the MAC-A type-2 (MAC) route. Once the BGP routing updates propagate to the remote PE devices (for example, Sx), the remote PE devices either remove MAC-A from their forwarding table (if S2 never advertised MAC-A) or remove VTEP-S1 from the ECMP group for all MAC addresses advertised by S1 with the S1-A ESI. In the worst case, the remote PE devices must wait for S2 to advertise the MAC-A type-2 route.

**Long story short:** Using EVPN to implement an MLAG cluster transformed a *local* data-plane action that could be performed in milliseconds into a control-plane action that has to be *propagated* (often through a BGP route reflector) and *executed on remote nodes*. The EVPN-only switchover might take two or more orders of magnitude longer than the local peer link switchover. Quoting the pretty level-headed [Arista whitepaper](https://www.arista.com/assets/data/pdf/Whitepapers/EVPN-DC-Multihoming-for-Resiliency-WP.pdf)[^NBG]:

[^NBG]: Arista supports traditional MLAG clusters, MLAG clusters with anycast VTEPs, and EVPN-only multihoming and thus has no skin in this game.

> With the A-A model relying on both the convergence of the underlay and EVPN overlay during a failover event, when compared to a similar MLAG topology, the A-A approach will result in more state churn across the EVPN domain and potentially slower convergence[^MEH].

[^MEH]: I guess that's as close as we'll get to a vendor saying "_Houston, we might have a problem_" ;)

We had a similar problem in traditional MPLS/VPN networks, where we used BGP PIC Edge to turn a distributed control-plane convergence into a local data-plane convergence. With the BGP PIC Edge, a PE router uses a stack of labels to push a packet that arrives at a node with a failed link straight to the *outgoing interface* of another node. Supposedly, we can use VTEP PIC Edge to achieve the same fast failover in VXLAN/EVPN networks. Back to Arista's whitepaper:

> To avoid any blackholing of traffic during this re-convergence, the node exhibiting the local link failure can also be configured to pre-calculate a backup path for the withdrawn routes via a VXLAN tunnel to peer node connected to the same ES, this is termed VTEP PIC edge.

[^TAC]: I love the sound of works-best-in-PowerPoint throwaway claims in vendor whitepapers.

VTEP PIC Edge has just two tiny little problems[^TAC]:

* It needs VXLAN-to-VXLAN bridging to work (see [MLAG Clusters without a Physical Peer Link](/2023/05/mlag-without-peer-link/) for more details), and [not all ASICs support that](/2022/06/vxlan-bridging-dci/).
* VXLAN header has a single "label" (Virtual Network Identifier -- VNI). Forwarding a misdirected packet to a peer node's *outgoing interface* is impossible. We can only send the packet *to the peer node* -- an excellent source of potential bridging microloops[^ML].

[^ML]: Micro loops are a fact of life. However, we're dealing with Ethernet packets that *have no TTL* and *could be flooded to multiple ports*. I know of several data centers that were brought down by flooding loops caused by bugs in MLAG software (in some cases, they lost two data centers because they [listened to VMware consultants](/2013/01/long-distance-vmotion-stretched-ha/)). Why should EVPN-based multihoming be any different?

You might not care about convergence speed after a LAG member failure. Feel free to use whatever solution you want if you're OK with a blackhole that might (worst case) persist for a few seconds[^FW]. However, if your applications depend on millisecond-speed failover, you might be better off using more traditional MLAG solutions.

[^FW]: You can find horror stories claiming [20 second](https://community.cisco.com/t5/xr-os-and-platforms/evpn-convergence-time-in-a-multihome-setup-is-about-20-seconds-2/td-p/4655483) or even [37 second](https://nwktimes.blogspot.com/2019/06/evpn-esi-multihoming-part-ii-fast/#c1399268855376082187) convergence times. I'm positive convergence times longer than a few seconds are a result of a configuration error, but even [Juniper admits](https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/topics/concept/evpn-bgp-multihoming-overview.html) that "*‌When there are changes in the network topology in a large-scale EVPN system, the convergence time might be significant.*"