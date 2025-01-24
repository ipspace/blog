---
title: "The Ethernet/802.1 Protocol Stack"
date: 2025-01-22 08:28:00+0100
tags: [ LAN ]
---
The believers in the [There Be Four Layers](https://blog.ipspace.net/2019/09/response-osi-model-is-lie/#2501) religion think everything below IP is just a blob of stuff dealing with physical things:

{{<figure src="/2025/01/eps-ip-view.png">}}

People steeped in a [slightly more nuanced view of the world](/2019/09/on-usability-of-osi-layered-networking/) in which IP is not the centerpiece of the universe might tell you that the *blob of stuff we need* is two things:
<!--more-->
* Something that transports bits (physical layer)
* Something that organizes bits into usable entities called frames that can be transported between adjacent nodes (data link layer)

{{<figure src="/2025/01/eps-osi-view.png">}}

As always, things tend to be more complex than they seem. IEEE figured out decades ago that various *things that provide frames* share common functionality (more about that later) and grouped that common functionality into the *Logical Link Control (LLC)* that uses technology-dependent *Media Access Control (MAC)*[^MACADDR]. The Ethernet frame format is part of the MAC sublayer, and all the protocols we love to hate (STP, LACP...) are part of the LLC sublayer.

[^MACADDR]: Although it looks like the interface addresses are the ubiquitous 6-octet entities, they are technology-dependent. That's why we call them MAC addresses. Also, you should call eight bits an *[octet](https://en.wikipedia.org/wiki/Octet_(computing))*, not a *[byte](https://en.wikipedia.org/wiki/Byte)* because we had [computer architectures like PDP-10 with 6-bit bytes](https://en.wikipedia.org/wiki/36-bit_computing) in the past.

{{<figure src="/2025/01/eps-llc-mac.png">}}

The IEEE 802.3 group came to similar conclusions. The *stuff that transports bits* is split into the Reconciliation Sublayer (RS), the Physical Coding Sublayer (PCS), the Physical Medium Attachment (PMA) sublayer, and the Physical Medium Dependent (PMD) sublayer. The one interesting to us from the protocol perspective is the Reconciliation Sublayer that implements the [auto-negotiation](https://en.wikipedia.org/wiki/Autonegotiation) and the Gigabit Ethernet Link Fault Signalling.

### Back to Fun Protocols

Now that we know way too much about the stuff we were never interested in, let's go back to the LLC layer -- the one with the fun protocols:

* First, we might have to discover the physical connections. LLDP (Link Layer Discovery Protocol) and its equivalents (for example, CDP) work directly on top of the MAC layer.
* We might want to group physical links into Link Aggregation Groups (LAGs). LACP (or PAgP) also has to work directly on top of the MAC layer.
* The link aggregation groups (LAGs) are the logical links that Spanning Tree Protocol tries to block to prevent loops. STP is thus above LACP, as is Shortest Path Bridging (SPB).
* Finally, we might want to implement multiple virtual links on top of logical links. That's where the VLAN encapsulation comes into play.
* DTP (Dynamic Trunking Protocol), VTP (VLAN Trunking Protocol), and their rarely used IEEE cousin MVRP (Multiple VLAN Registration Protocol) are VLAN provisioning protocols and thus run aside from VLAN encapsulation.
* Per-VLAN spanning tree protocols must be associated with individual VLANs. Thus, their packets (BPDUs) include VLAN encapsulation.

{{<figure src="/2025/01/eps-llc-protocols.png">}}

### Does It Matter?

While it's good to know how things fit together[^MFY], you don't have to worry about them unless you're trying to confuse your switches with [weird native VLAN setups](https://lostintransit.se/2024/07/16/encapsulation-of-pdus-on-trunk-ports/).

[^MFY]: So you don't make a fool out of yourself like the [mansplainers @tracketpacer has to deal with](https://x.com/tracketpacer/status/1874897546302341272).

Networking on Linux is a different story. Linux considers everything a *device*:

* Ethernet interface is a device (OK)
* Link aggregation group is a *bond* device (also OK, looks like a PortChannel)
* VLAN attachment is a device (OK, this looks like a subinterface)
* A bridge is a device (I guess we should be OK; it's similar to Cisco IOS *bridge domains*).
* A VRF is a device (interesting ;)

However, you can *combine* these devices in way too many ways[^BVL]. For example, if you attach VLAN interfaces to a bridge, you'll get a *bridged VLAN* (OK) and an instance of legacy STP running with VLAN encapsulation (definitely not OK). This looks like PVST+ or RPVST+, but the frame formats are different enough that it does not work.

To get a setup that will interoperate with almost anything else out there, you have to create a VLAN-aware Linux bridge to put VLANs where they belong: *on top of* STP-enabled links.

[^BVL]: I never tried to create a bond device out of VLAN interfaces, but I wouldn't be surprised to see it work.

### Revision History

2025-01-24
: Added VTP to the list of VLAN provisioning protocols.
