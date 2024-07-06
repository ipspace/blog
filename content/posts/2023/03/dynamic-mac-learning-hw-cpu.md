---
title: "Dynamic MAC Learning: Hardware or CPU Activity?"
date: 2023-03-07 06:59:00
tags: [ switching ]
---
An ipSpace.net subscriber sent me a question along the lines of "_does it matter that EVPN uses BGP to implement dynamic MAC learning whereas in traditional switching that's done in hardware?_" Before going into those details, I wanted to establish the baseline: is dynamic MAC learning really implemented in hardware?

Hardware-based switching solutions usually [use a hash table to implement MAC address lookups](/2022/02/packet-forwarding-header-lookup.html). The above question should thus be rephrased as _is it possible to update the MAC hash table in hardware without punting the packet to the CPU?_ One would expect high-end (expensive) hardware to be able do it, while low-cost hardware would depend on the CPU. It turns out the reality is way more complex than that. 
<!--more-->
ASIC programming guides would be the natural places to find the definitive answer, but those are a bit hard to get, so I [decided to ask around on Twitter](https://twitter.com/ioshints/status/1631319387096399872):

> Is dynamic MAC learning (= updating MAC table) done in hardware or are the packets from unknown sources punted to the CPU? Any pointers to real-life information would be highly appreciated.

I was infinitely surprised by the high-quality answers I got. Thanks a million to everyone who took time to reply!!!

[Andrew Zonenberg](https://twitter.com/azonenberg) implemented a gigabit switch with FPGA and [open-sourced its design](https://github.com/azonenberg/latentpacket/tree/master/latentred). In his design, the [FPGA autonomously updates the MAC table](https://twitter.com/azonenberg/status/1631347089736372225):

> The MAC address table in my (WIP) open hardware switch manages all learning and lookups in gateware. No CPU interaction is required whatsoever during normal operation; all it does is translate ASCII text CLI commands to register writes when you change VLAN settings etc.

I know nothing about FPGA design languages, but [his extensive comments](https://github.com/azonenberg/latentpacket/blob/master/latentred/rtl/fabric/MACAddressTable.sv?ts=4#L34) made it easier to figure out what's going on:

* MAC hash table is used primarily for packet lookups. Updating the hash table (dynamic MAC learning) is thus a background activity;
* If the source MAC address is not in the MAC table, it's added to a FIFO queue of addresses-to-be-learned;
* Once the MAC hash table is free to be used (no packet lookup activity), the MAC addresses from that FIFO queue are inserted into it.

However, once you get enough MAC addresses in the hash table, [hash collisions](https://en.wikipedia.org/wiki/Hash_collision) become a problem. [Cuckoo hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing) is one of the workarounds, but it's a more complex algorithm that's harder to implement in hardware. Many implementations thus offload the task to the CPU even if the hardware could handle it on its own. According to [Diego Dompe](https://twitter.com/ddompe/status/1631324559264677891):

> You could easily handle the write operation in HW if you want, but when the hash table approaches full and you have to deal with collisions, the HW implementation gets ugly, so simpler solution is to go to some CPU for decision making.

But which CPU is it? The one running the network operating system or another one embedded in the ASIC? [Back to Diego](https://twitter.com/ddompe/status/1631324207677054977):

> Most of the ASICs I’m aware of will sent them to some CPU, sometimes the same CPU of the NOS, and some can have embedded CPUs inside the ASIC doing the process. In either case there is usually a fast-path for it in the CPU processing.

The behavior is configurable on higher-end hardware. [According to Andrew McCoubrey](https://twitter.com/mccoubr/status/1631322837137989632):

> It’s complicated and there are various schemes but these days the answer is both. The default in most switches is to update hardware tables automatically and also notify the CPU. But this behaviour can be configured via registers, eg Broadcom has “CPU managed Learning”

Why would you want to punt an activity to the CPU if it could be handled by the ASIC (or the CPU hidden within the ASIC)? This is how [Andrew explained the tradeoffs](https://twitter.com/mccoubr/status/1631356239249567745):

> Some products will want software to vet every new MAC-to-port entry before the forwarding table gets updated, to address DoS/security issues. eg at the edge/access
>
> Others will want the hardware updated immediately because the CPU can’t keep up. eg in the core.

The discussion might be moot in a multi-ASIC switch[^MA] -- MAC tables have to be updated on all ASICs regardless of whether they've seen the packet triggering dynamic MAC learning. As [Diego explained](https://twitter.com/ddompe/status/1631324758909263872):

> Also, if the ASIC is used in a chassis, you still need to propagate the learning to other ASICs, so NOS CPU will get involved anyway.

As is usually the case, Jeff Tantsura wrote a nice summary as [LinkedIn comment](https://www.linkedin.com/feed/update/urn:li:activity:7038768712052559872/):

> The answer is (as often) it depends ;-) most modern ASICs do it in HW(configurable). In a chassis, there would be a form of IPC (potentially multi-point) to update each LC/ASIC directly from ingress (ASIC that has learnt the new MAC).
>
> In EVPN (using generic names), there would be a L2manager talking to L2RIB/L3RIB and BGP that would emulate flooding (at the end, basic EVPN EVI emulates a bridge) and send a RT-2 route (separately MAC only and then when binding is learnt - MAC/IP) to each member of that domain (every participant that has announced their membership through RT-3 route before).

Finally, [Aaron Glenn provided a link](https://twitter.com/networkservice/status/1631329668866494467) to (public!!!) [Broadcom Jericho2 documentation](https://docs.broadcom.com/doc/88690-88800-88480-88280-Packet-Processing-Programming-Guide). It might make for a great reading if you're afraid of sleepless nights -- it has "only" 850 pages.

**Lessons learned:**

* It depends
* Dynamic MAC learning could be done in hardware, but it's harder to implement intelligent algorithms to deal with hash collisions.
* Many implementations offload dynamic MAC learning to a CPU -- either the CPU embedded in the ASIC or the main CPU.
* Sometimes the main CPU needs to be involved even if the MAC addresses are not propagated with the control plane.

[^MA]: Even fixed-configuration switches could use more than one switching ASIC