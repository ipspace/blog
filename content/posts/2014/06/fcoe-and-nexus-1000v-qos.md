---
date: 2014-06-03 07:36:00+02:00
tags:
- FCoE
- QoS
- virtualization
title: FCoE and Nexus 1000v QoS
url: /2014/06/fcoe-and-nexus-1000v-qos.html
---
One of my readers wanted to deploy FCoE on UCS in combination with Nexus 1000v and wondered how the FCoE traffic impacts QoS on Nexus 1000v. He wrote:

> Let\'s say I want 4Gb for FCoE. Should I add bandwidth shares up to 60% in the nexus 1000v CBWFQ config so that 40% are in the default-class as 1kv is not aware of FCoE traffic? Or add up to 100% with the assumption that the 1kv knows there is only 6Gb left for network? Also, will the Nexus 1000v be able to detect contention on the uplink even if it doesn\'t see the FCoE traffic?

As always, things aren't as simple as they look.

{{<note warn>}}You know [Nexus 1000v is dead](https://www.cisco.com/c/en/us/products/switches/nexus-1000v-switch-vmware-vsphere/eos-eol-notice-listing.html), right? This blog post was left online for historic reasons ;){{</note>}}
<!--more-->
### Background: adapter FEX and FCoE

The UCS Ethernet adapters implement [FCoE](https://blog.ipspace.net/2011/08/fcoe-networking-elements-classification.html) in hardware -- the operating system doesn't know it deals with a single physical adapter with a single set of 10GE uplinks. Each physical 10GE adapter appears as (at least) two PCI adapters: a 10GE Ethernet NIC and a Fiber Channel Host Bus Adapter (HBA).

{{<note>}}Every 10GE adapter implementing FCoE in hardware has NIC+HBA functionality. Cisco's adapter cards (P81E or VIC1225) or third-party adapters that support Cisco's proprietary VNTag technology (example: Broadcom BCM57810) allow you to go one step further and create numerous Ethernet adapters from the same physical NIC.{{</note>}}

[![](/2014/06/s400-AdapterFEX.png)](/2014/06/s1600-AdapterFEX.png)

The bandwidth allocation and queuing on the physical 10GE uplink is hidden from the NICs presented to the operating system. The operating system thinks it deals with multiple full-blown 10GE/FC interfaces, and it just happens that the interfaces transmit packets from the hardware TX-ring slower than one would expect... but then you could get the same results using PAUSE frames (or [PFC](https://blog.ipspace.net/2010/09/introduction-to-8021qbb-priority-flow.html)) on a dedicated 10GE interface.

### Output queuing on Nexus 1000v

Output queuing on Nexus 1000v works the same way as any other output queuing implementation: the interface driver enqueues the output packets into the [hardware TX-ring](/kb/tag/QoS/Queuing_Principles.html) until the TX-ring reaches a preset length, at which point the software queuing (CBWFQ) starts.

The interface driver doesn't need to know the exact interface bandwidth, all it needs to know is when the TX ring is below the low watermark (at which point packets are dequeued from the CBWFQ queues and moved to the TX ring). The bandwidth percentages specified in the CBWFQ affect the *relative* amount of data transferred from each individual class queue; they work equally well regardless of the physical interface speed or its actual throughput.

### Related webinars

-   [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers)
-   [VMware Networking Technical Deep Dive](http://www.ipspace.net/VMware_Networking_Deep_Dive)
