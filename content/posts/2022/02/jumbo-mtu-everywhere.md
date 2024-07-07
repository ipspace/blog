---
title: "The Impact of Jumbo Maximum Frame Size on Data Center Switches"
date: 2022-02-17 07:51:00
lastmod: 2022-02-19 07:43:00
tags: [ switching ]
---
[Sander Steffann](https://www.linkedin.com/in/sandersteffann/) sent me an intriguing question a long while ago:

> I was wondering if there are any downsides to setting "system mtu jumbo 9198" by default on every switch? I mean, if all connected devices have MTU 1500 they won't notice that the switch could support longer frames, right? 

That's absolutely correct, and unless the end hosts get into UDP fights things will always work out (aka TCP MSS saves the day)... but there must be a reason switching vendors don't use maximum frame sizes larger than 1514 by default ([Cumulus Linux seems to be an exception](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-41/Whats-New/), and according to [Sébastien Keller](https://www.linkedin.com/in/sebastienkeller/) Arista's default maximum frame size is between 9214 and 10178 depending on the platform).
<!--more-->
{{<note>}}See _[to MTU or not to MTU](#to-mtu-or-not-to-mtu)_ section at the end of the blog post if you wonder about my avoidance of the MTU acronym.{{</note>}}

The only reason I could see for the persistent use of ancient 1514-byte maximum frame size might be the hardware buffering architecture. I've seen two ways of organizing (hardware) input buffers:

* A single input buffer must be able to hold the largest possible input packet. Increasing the interface or system maximum frame size results in smaller number of packet buffers[^RAM] and reduced ability to absorb input bursts (example: wasting a 9K buffer to hold a 64-byte VoIP packet).
* An input packet can spill over into several buffers (sometimes called *particles*) -- a mechanism called *scatter/gather* or *[vectored I/O](https://en.wikipedia.org/wiki/Vectored_I/O)*. The maximum frame size doesn't matter, as large packets fill as many particles as needed.

[^RAM]: ... given the same amount of buffer memory

The only particle-based platforms I encountered were Cisco 7200 and VIP line cards in Cisco 7500 (because they used repackaged Cisco 7200s inside). I went through the publicly available Cisco Cloud ASIC presentations and while they're full of "intelligent buffering" bragging, they don't mention anything even vaguely resembling scatter/gather architecture.

The two O'Reilly books describing Juniper hardware that I happen to have on my bookshelf are uselessly vague[^BC]. [Expert Packet Walkthrough on the MX Series 3D](https://www.juniper.net/documentation/en_US/day-one-books/TW_MX3D_PacketWalkthrough.pdf) has more details; the way I read it, it claims the MX uses *parcels* (320 bytes) to store the input packets and fixed-size cells (64 bytes) to move the packets between forwarding engines.

Finally, [Broadcom hates anyone telling us anything useful](/2016/05/what-are-problems-with-broadcom/), but as both Arista and Cumulus use large default values, it **might** be a solved problem. In any case, it would be nice to **know** the problem has been solved in data center switching ASICs (high-end ASICs like Jericho or router platforms are a totally different story), and so far I haven't seen anything that would look convincing.

**To recap**: while systems with fixed-size buffers lose the ability to absorb input bursts when you increase the maximum frame size, particle-based systems don't care. Unfortunately we often have absolutely no idea how the expensive hardware we just bought works... or I've overlooked something, in which case I'd appreciate useful pointers in the comments.

### To MTU or Not to MTU

Adam Chappell [tweeted me a nice warning](https://twitter.com/packetsource/status/1494288636384264200):

> Sometimes there's benefit in reserving the term MTU for the layer 3 protocols that may have ways of doing their own segmentation/reassembly, and calling that jumbo setting on switches exactly what it is, "maximum frame size". 

I almost became a wiseass replying _it's called Maximum Transmission Unit for a reason_ but decided to check the [ultimate source of all truth](https://en.wikipedia.org/wiki/Maximum_transmission_unit) which claimed that...

> In computer networking, the maximum transmission unit (MTU) is the size of the largest protocol data unit (PDU) that can be communicated in a single network layer transaction.

Ignoring the _single network layer transaction_ elephant cluelessly wandering around the room, the article further explains:

> The MTU relates to, but is not identical to the maximum frame size that can be transported on the data link layer, e.g. Ethernet frame.

Here we go. As switches receive Ethernet frames into their buffers, we're dealing with _maximum frame size_. Thank you Adam!

### Revision History

2022-02-19
: Added information about Arista's defaults and related conclusions

2022-02-17
: Changed _MTU_ to _maximum frame size_

[^DATE]: Yeah, I know, I just dated myself :(

[^BC]: No wonder, one of them is describing a product using Broadcom ASIC.