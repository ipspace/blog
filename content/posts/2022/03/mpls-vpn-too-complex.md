---
title: "Is MPLS/VPN Too Complex?"
date: 2022-03-31 08:37:00
tags: [ MPLS VPN ]
---
Henk Smit made the following claim in one of his comments:

> I think BGP-MPLS-VPNs are over-complicated. And you don't get enough return for that extra complexity.

**TL&DR**: He's right (and I just violated *[Betteridge's law of headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines)*)

The history of how we got to the current morass might be interesting for engineers who want to look behind the curtain, so here we go...
<!--more-->
To understand the MPLS/VPN design concepts, one has to realize what the alternatives were in late 1990s:

* Nobody was crazy enough to think about bridging over WAN; we were still recovering from the nightmares caused by people trying to do that with *brouters* or Ethernet bridges. Carrier Ethernet was nowhere to be seen -- WAN Ethernet circuits were simply not a thing yet.
* The only alternative to the shaky semi-reliable public Internet were various circuit-based WAN technologies like ATM or Frame Relay. There were even people building VPNs over X.25[^X25C].

[^X25C]: ...and paying dearly for every byte transferred.

Circuit-based WAN technologies were a perfect fit for traditional hierarchical networks, but became an absolute nightmare when you were trying to build an any-to-any network. You had to:

* Figure out which sites are most likely to communicate and order a separate virtual circuit for every pair of sites. The traffic between other sites would still be exchanged over hub sites.
* Guesstimate how much traffic you might see between a pair of sites and specify that bandwidth when provisioning the virtual circuit.

Customers hated that, and even smart service providers weren't exactly happy. They had to deal with a spaghetti mess of point-to-point virtual circuits that were burning precious hardware forwarding resources on every switch on the way[^ATMVP].

Now imagine a vendor coming along saying "_imagine you could build an Internet-like service for every customer_":

* **There would be no explicit virtual circuits** -- routing protocols would sort out where the traffic should go.
* **You could specify ingress- and egress bandwidth per node**, do ingress/egress policing or marking on the PE-routers, and let differentiated queuing/dropping in the network core do its job.
* Customer would need a **single routing adjacency on the PE-CE link** instead of a complex setup supporting partially-meshed Frame Relay WAN.

No wonder everyone was so enthusiastic about MPLS/VPN.

The early MPLS/VPN implementations were sane (because the nerd knobs weren't there yet). For example, AT&T offered MPLS/VPN on Frame Relay access links using EBGP as the PE-CE routing protocol. You could use existing EBGP mechanisms (MED or AS Path prepending) to implement primary/backup links, and it all just worked.

And then the feature requests started:

* **I want to use OSPF** between PE routers and CE routers (OSPF down bits, extra VPNv4 extended communities)
* **My customer has OSPF backup links**, so we need OSPF sham links between PE-routers
* **I want to use EIGRP** and I don't want you to redistribute site routes back into the same site on PE-routers (requiring site-of-origin community)
* **My customer has more than 1000 sites**, resulting in crazy AS path handling hacks[^4ASN]
* **I want differentiated QoS for every customer** resulted in all sorts of "solutions" too ugly to mention.
* **I want fast failover** eventually brought us PIC Edge and associated BGP hacks.
* **My customers want to reinvent Frame Relay with MPLS/VPN** because some people wanted to have lower-priced service providing the complex scenarios of the higher-priced service[^SAYNO]. Welcome to hub-and-spoke VPN designs.

The list of MPLS/VPN features goes on and on. We have VRF selection using PBR, half-duplex VRF, RT rewrite, Inter-AS MPLS/VPN, RT-based ORF... There's a story behind every one of these features, often starting with a large service provider forcing a vendor to implement a nerd knob to fix a broken design.

On top of that, service providers lacking the technical skills needed to run an outsourced core IP network increased the bad rap of MPLS/VPN technology. I had several customers who went directly from Frame Relay to Internet-based IPsec VPNs because they didn't trust the service provider to do a decent job. Those same service providers [want to offer managed SD-WAN services today](/2020/03/sdwan-service-provider-perspective/). I wish their customers plenty of luck; they might need it 🥴

In the meantime (it's been over 20 years since my MPLS/VPN book was published), Carrier Ethernet became a viable alternative, and as much as it hurts me, I'm usually recommending customer-managed routers attached to Carrier Ethernet as a better (and safer) alternative to MPLS/VPN. You'll find more details in the _[Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)_ webinar.

[^ATMVP]: ATM Virtual Path concept introduced some hierarchy, but ATM circuits were awfully expensive (and wasted bandwidth due to cell tax). On the other hand, Frame Relay switches didn't offer the high speed interfaces; the service providers had to deal with all sorts of complex FR-to-ATM interworking solutions.

[^4ASN]: Instead of implementing 4-byte ASN. Networking industry loves to solve things with hacks. See also: NAT and CGN instead of IPv6.

[^SAYNO]: And the SP account team would never say "_we don't do that because we'd be losing money on your stupid design_" (aka "_we sold it, it's Ops problem now_"). It's more convenient to wave a large P/O in front of the vendor account team, yell about missing features, and then blame the vendor for resulting complexity.

### Revision History

2022-04-05
: Added a link to "SD-WAN: A Service Provider Perspective" blog post.
