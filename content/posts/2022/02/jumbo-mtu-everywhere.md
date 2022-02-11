---
title: "The Impact of Jumbo MTU on Data Center Switches"
date: 2022-02-17 07:51:00
tags: [ switching ]
---
[Sander Steffann](https://www.linkedin.com/in/sandersteffann/) sent me an intriguing question a long while ago:

> I was wondering if there are any downsides to setting "system mtu jumbo 
9198" by default on every switch? I mean, if all connected devices have 
MTU 1500 they won't notice that the switch could support longer frames, 
right? 

That's absolutely correct, and unless the end hosts get into UDP fights things will always work out (aka TCP MSS saves the day)... but there must be a reason switching vendors don't use jumbo MTU by default ([Cumulus Linux seems to be an exception](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-41/Whats-New/)).
<!--more-->
The only reason I could see for the persistent use of ancient 1500-byte MTU might be the hardware buffering architecture. I've seen two ways of organizing (hardware) input buffers:

* A single input buffer must be able to hold the largest possible input packet. Increasing the interface or system MTU size results in smaller number of packet buffers[^RAM] and reduced ability to absorb input bursts (example: wasting a 9K buffer to hold a 64-byte VoIP packet).
* An input packet can spill over into several buffers (sometimes called *particles*) -- a mechanism called *scatter/gather* or *[vectored I/O](https://en.wikipedia.org/wiki/Vectored_I/O)*. The MTU size doesn't matter, as large packets fill as many particles as needed.

[^RAM]: ... given the same amount of buffer memory

The only particle-based platforms I encountered were Cisco 7200 and VIP line cards in Cisco 7500 (because they used repackaged Cisco 7200s inside). I went through the publicly available Cisco Cloud ASIC presentations and while they're full of "intelligent buffering" bragging, they don't mention anything even vaguely resembling scatter/gather architecture.

The two O'Reilly books describing Juniper hardware that I happen to have on my bookshelf are uselessly vague[^BC]. [Expert Packet Walkthrough on the MX Series 3D](https://www.juniper.net/documentation/en_US/day-one-books/TW_MX3D_PacketWalkthrough.pdf) has more details; the way I read it, it claims the MX uses *parcels* (320 bytes) to store the input packets and fixed-size cells (64 bytes) to move the packets between forwarding engineers.

Finally, [Broadcom hates anyone telling us anything useful](https://blog.ipspace.net/2016/05/what-are-problems-with-broadcom.html).

**To recap**: while systems with fixed-size buffers lose the ability to absorb input bursts when you increase the MTU size, particle-based systems don't care about MTU sizes. Unfortunately we often have absolutely no idea how the expensive hardware we just bought works... or I've overlooked something, in which case I'd appreciate useful pointers in the comments.

[^DATE]: Yeah, I know, I just dated myself :(

[^BC]: No wonder, one of them is describing a product using Broadcom ASIC.