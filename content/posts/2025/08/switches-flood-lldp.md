---
title: "When Switches Flood LLDP Traffic"
date: 2025-08-25 09:13:00+0200
tags: [ bridging, data center ]
---
A networking engineer (let's call him Joe[^RA]) sent me an interesting challenge: they built a data center network with Cisco switches, and the switches *flood LLDP packets* between servers.

That would be interesting by itself (the whole network would appear as a single hub), but they're also using DCBX (which is riding in LLDP TLVs), and the DCBX parameters are negotiated *between servers* (not between servers and adjacent switches), sometimes resulting in NIC resets[^NR].
<!--more-->
[^RA]: Who wishes to remain anonymous for obvious reasons

[^NR]: Definitely a fun thing to have in a production environment

My initial response was "_that's crazy, of course the LLDP packets should not be flooded_ 🤦‍♂️," and a quick glance at the IEEE 802.1 standards confirmed my intuition. Here's the relevant part of the 802.1AB (LLDP) standard. It effectively says that the switches conforming to the 802.1D standard **MUST NOT** forward LLDP packets.

{{<figure src="/2025/08/802.1ab.png">}}

Interestingly, assuming the servers would implement DCBX correctly, flooding the LLDP packets might be a non-issue. Here's what the 802.1Qaz (DCBX) standard has to say:

{{<figure src="/2025/08/802.1Qaz.png">}}

However, it looks like Joe's network has a single server sending DCBX packets, and all other servers are in listen-only mode. Those servers thus have no chance to detect multiple LLDP neighbors per NIC 🤷‍♂️

Anyway, of course Joe opened a case with Cisco TAC, and of course the response was "_our switches work as expected_", in particular:

> On the NCS series, an untagged l2transport sub-interface behaves like a generic bridge-domain (BD) endpoint. All traffic, including MAC-multicast and reserved-MAC traffic, is treated as data and flooded across the domain.

Ah, the plot thickens. Joe's network does not use data center switches (the Nexus product line) but service provider gear that implements Metro Ethernet Forum (MEF) standards. Let's look at what MEF has to say about LLDP flooding.

The relevant standard document is [MEF 45.1](https://www.mplify.net/wp-content/uploads/2018/12/MEF-45-1.pdf) (Layer 2 Control Protocols in Ethernet Services) from August 2018, and I would recommend you read it for all the background information it contains. For example, it starts with a nice overview of IEEE-reserved MAC addresses (Table 3, Bridge Reserved Addresses), where we learn that the LLDP MAC address (01-80-C2-00-00-0E) really means  *Nearest Bridge, Individual LAN Scope* and that it should always be filtered. Score one for IEEE.

However, MEF 45.1 then introduces the concept of the *L2CP Decision Point* (section 7.1) where a switch can decide to pass a L2 control-plane packet, to drop it, or to peer with the adjacent device (like a "normal" 802.1D-compliant bridge). After a lengthy deliberation process it finally brings us to the crux of the discussion: the *L2CP Address Set Service Attribute* (section 8.1), where the C-Tag Blind Option 2 (CTB-2) effectively means *meh, forward almost everything* (Table 6) apart from Pause/PFC frames (Table 8), including LLDP packets (Table 9). Score one for Cisco.

However, there's one more thing. Section 10 of MEF 45.1 defines the *Service Requirements for L2CP*, effectively saying:

1. You MUST behave like an 802.1D bridge on VLAN-based services (Ethernet Virtual Private _Something_ services) (Table 11)
2. You CAN behave like an 802.1D bridge (CTB) or be completely transparent (CTB-2) on Ethernet Private Line (EPL) service (Table 12)
3. You MUST behave like an 802.1D bridge (CTB) on Ethernet Private LAN (EP-LAN) or Tree service (Table 12)

Assuming Joe's network uses NCS 5500 to implement any-to-any connectivity between servers, they're using the EP-LAN service. In that environment, the switches MUST behave under CTB rules and MUST NOT pass LLDP packets (Table 6). Can we call this a foul on Cisco's part?

**Long story short:**

* If you want an easy life, do not use service provider gear to build data center networks.
* The service provider gear can be made to work the way you expect data center switches to work, but it might require extra configuration.
* According to my reading of the MEF 45.1 standard, the IOS/XR version Joe uses is not exactly compliant because it uses CTB-2 behavior on EP-LAN service, but I would love to hear your thoughts.
