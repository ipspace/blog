---
anycast_tag: fabric
date: 2013-06-04 07:16:00+02:00
series:
- anycast
tags:
- data center
- fabric
- IP routing
- LAN
title: VRRP, Anycasts, Fabrics and Optimal Forwarding
url: /2013/06/vrrp-anycasts-fabrics-and-optimal.html
---
The [Optimal L3 Forwarding with VARP/VRRP](/2013/05/optimal-l3-forwarding-with-varp-and.html) post generated numerous comments, ranging from technical questions about VARP (more about that in a few days) to remarks along the lines of "you can do that with X" or "vendor Y supports Z, which does the same thing." It seems I've opened yet another can of worms, let's try to tame and sort them.
<!--more-->
### FHRP Basics

First-hop redundancy protocols (FHRP) solve a simple problem: IPv4 has no standard host-to-router protocol. Hosts are usually configured with a static address of the first-hop router, forcing the routers to share an IP address (sometimes called Virtual Router IP Address) in redundant environments. In most cases the routers also share the MAC address of the shared first-hop router IP address to work around broken or ~~misconfigured~~ secured IP stacks that ignore gratuitous ARPs sent after the ownership of the shared IP address changes.

{{<note info>}}I'll use the term FHRP throughout this document to indicate a range of protocols, including HSRP, GLBP, VRRP v2 and v3.{{</note>}}

Typical FHRP use case is a large layer-2 domain connecting numerous end hosts to more than one router. The routers are (relatively) close together, and there's some indeterminate layer-2 infrastructure (anything from a [thick coax cable](http://en.wikipedia.org/wiki/10BASE5) to large TRILL or SPB fabric) between the end hosts and the routers.

{{<figure src="/2013/06/s320-FHRP_Generic.jpg" caption="Typical FHRP use case">}}

The first-hop routers cannot rely on any particular forwarding behavior of the underlying layer-2 infrastructure; each router must have its own set of MAC addresses that have to be *active* -- traffic must be sourced from those MAC addresses lest the layer-2 switches start flooding the unicast traffic sent to one of the router's MAC address.

{{<figure src="/2013/06/s320-FHRP_Generic_Inside.jpg" caption="Connecting routers using FHRP to a fabric">}}

The *active MAC address* requirement usually limits the number of active FHRP forwarders to one -- multiple forwarders using the same MAC address would cause serious *MAC flapping* on intermediate switches, and the intermediate switches wouldn't be able to perform load balancing toward multiple identical MAC addresses anyway.

### Data Center Use Case

The primary goal of [optimal layer-3 forwarding in a data center environment](/2012/05/does-optimal-l3-forwarding-matter-in.html) is to minimize the leaf-to-spine traffic in environments where the amount of east-west (server-to-server) traffic significantly exceeds the amount of north-south (server-to-client) traffic. The only way to reach this goal is to introduce layer-3 forwarding functionality into hypervisors or (failing that) the top-of-rack (ToR) switches.

{{<figure src="/2013/06/s320-FHRP_DC.jpg" caption="High-level view of an optimal data center fabric">}}

{{<note info>}}After more than a decade, the only shipping enterprise network virtualization product supporting layer-3 forwarding a hypervisor remains [Hyper-V Network Virtualization](/2012/12/hyper-v-network-virtualization-wnvnvgre.html).{{</note>}}

The ability to [migrate a running VM between physical hosts](/2010/09/vmotion-elephant-in-data-center-room.html) (and ToR switches) introduces additional requirements: all ToR switches have to share the same MAC address; nobody likes to see the [traffic trombones](/2011/02/traffic-trombone-what-it-is-and-how-you.html) that result from a VM being pinned to a MAC address of a remote ToR switch.

### The Solutions

As always the networking industry tried to "solve" the problem by introducing all sorts of ~~hacks~~ inspired ideas, some of them more useless than the others. The most common ones (described in this blog post) are:

-   No FHRP (core switches appear as a single entity);
-   Active/Active FHRP on a MLAG pair;
-   GLBP.

More creative solutions are described in other blog posts:

-   [Optimal L3 forwarding with VARP or active/active VRRP](/2013/05/optimal-l3-forwarding-with-varp-and.html)
-   [QFabric part 3 - forwarding](/2011/09/qfabric-part-3-forwarding.html) (now mostly obsolete)
-   [Building large L3 fabrics with Brocade VDX switches](/2012/09/building-large-l3-fabrics-with-brocade.html) (completely obsolete/EoL)

### No FHRP with Single Control Plane

Vendors that implement redundant switching fabrics with a [single control plane](/2010/10/multi-chassis-link-aggregation-stacking.html) (Cisco's VSS, HP's IRF, Juniper Virtual Chassis) don't need FHRP. After all, the whole cluster of boxes acts as a single logical device with a single set of IP and MAC addresses.

{{<note info>}}Juniper's Virtual Chassis looks exactly the same as Cisco's VSS or HP's IRF from the outside, but uses a slightly different implementation mechanism: somewhat independent control planes coordinated through a shared management plane.{{</note>}}

Before someone persuades you to solve optimal L3 forwarding problem with a virtual stack of ToR switches spread all over your data center (and I've seen consultants peddling this "design" to unsuspecting customers), consider [how the traffic will flow](/2012/11/stackable-data-center-switches-do-math.html).

#### Active/Active FHRP over MLAG

Almost every vendor offering [MLAG functionality](/2010/10/multi-chassis-link-aggregation-basics.html) across a pair of independent core switches (Cisco's vPC, Arista, Nokia...) supports active/active FHRP forwarding on the core switches:

{{<figure src="/2013/06/s320-FHRP_VPC.jpg" caption="Active/Active FHRP">}}

This solution is almost a no-brainer, although the [implementation details must be pretty complex](/2022/06/mlag-active-active-layer3.html), otherwise it's hard to understand why it took some vendors years to implement it. Here's how it works:

-   FHRP is configured on the members of the MLAG group. One of the members is elected as the active FHRP gateway and advertises the FHRP MAC address.
-   All members of the MLAG group listen to the FHRP MAC address;
-   Packets coming from the FHRP MAC address (example: VRRP advertisements) are sent over one of the LAG member links to the ToR switch -- ToR switch thus knows how to reach the FHRP MAC address;
-   Packets to the FHRP MAC address are sent from the ToR switch over one of the LAG member links (not necessarily the link over which the packet from FHRP MAC address arrived), resulting in [somewhat optimal load balancing](http://packetpushers.net/the-scaling-limitations-of-etherchannel-or-why-11-does-not-equal-2/) toward FHRP MAC address.
-   Whichever core switch receives the inbound packet to FHRP MAC address performs L3 forwarding.

As always, the devil is in the details: L3 switches might send the routed traffic from their hardware MAC address (not FHRP MAC address), thoroughly confusing devices with broken TCP stacks that [prefer to glean incoming packets instead of using standard mechanisms like ARP](http://www.jeremyfilliben.com/2010/08/hsrp-vpc-and-vpc-peer-gateway-command.html).

Active/active FHRP behavior is nice-to-have if you're satisfied with L3 forwarding on core switches. Just remember that all inter-subnet east-west traffic traverses the core even when the two VMs sit in the same hypervisor host.

{{<figure src="/2013/06/s320-FHRP_MLAG_Flow.png" caption="Inter-VLAN traffic flow with routing on core switches">}}

#### The GLBP Hack

GLBP bypassed the single forwarder limitation with an interesting trick -- different hosts would receive different MAC addresses (belonging to different routers) for the shared virtual router IP address.

While the trick might work well in original FHRP use cases (with large L2 domain between the hosts and the bank of routers), it's totally useless in data center environments requiring L3 forwarding at the ToR switches:

-   VM might get a MAC address from a random ToR switch (not the closest switch);
-   VM is pinned to a MAC address of a ToR switch and sends the traffic to that same switch even when you vMotion the VM to a totally different physical location.

{{<figure src="/2013/06/s320-FHRP_GLBP_Flow.png" caption="GLBP is useless in a data center fabric">}}

Multi-FHRP hack, where each router belongs to multiple FHRP groups on each interface and end-hosts use different first-hop gateways, is almost identical (but harder to manage) than GLBP hack

{{<figure src="/2013/06/s320-FHRP_HSRP_AB.png" caption="Multiple FHRP groups are no better than GLBP">}}

### More information

Got so far? Wow, I'm impressed. Here's more:

-   [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) webinar describes numerous data center-related technologies and challenges, including L2/L3 designs;
-   [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) webinar describes typical fabric architectures and vendor implementations;

### Revision History

2023-02-01
: * Removed references to long-gone products/startups.
  * Added links to additional relevant blog posts.
