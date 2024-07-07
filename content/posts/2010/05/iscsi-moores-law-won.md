---
date: 2010-05-24 07:09:00.005000+02:00
tags:
- IP services
- SAN
- workshop
title: 'iSCSI: Moore’s Law Won'
url: /2010/05/iscsi-moores-law-won/
---
A while ago I was [criticizing the network-blindness of the storage industry](/2009/12/iscsi-and-san-two-decades-of-rigid/) that decided to run 25-year old protocol (SCSI) over the most resource-intensive transport protocol (TCP) instead of fixing their stuff or choosing a more lightweight transport mechanism.

My argument (although theoretically valid) became moot a few months ago: [Intel and Microsoft have demonstrated an iSCSI solution](http://download.intel.com/support/network/sb/inteliscsiwp.pdf) that can saturate a 10GE link and perform more than 1 million I/O operations per second. Another clear victory for the Moore's Law.
<!--more-->
{{<note info>}}Please note that this blog post was written in 2010. While the fundamental principles haven't change, Moore Law kept going. A single CPU core can process tens of Gbps of packets without TCP offload, and Netflix managed to [stream 700 Gbps of encrypted video from a single server in 2022](/2022/12/are-dpu-any-good/).{{</note>}}

**Why is this important?** iSCSI was always considered an inferior (but admittedly cheaper) solution when compared with Fiber Channel (FC). This benchmark clearly shows that iSCSI performance no longer lags behind FC. iSCSI is thus a viable alternative for network designers that want to build converged LAN/SAN networks.

**How did they do it?** Intel has built a large number of TCP acceleration techniques in its Gigabit Ethernet chipsets ([here's a quick summary](http://blog.fosketts.net/2010/03/19/microsoft-intel-starwind-iscsi/)). For example, the Intel 82599 10GE controller handles IP, TCP and UDP checksums, and [TCP offload](https://en.wikipedia.org/wiki/TCP_offload_engine) including transmit-side TCP segmentation and [Receive Segment Coalescing](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh997024(v=ws.11)). Going even further, Intel CPUs starting with  [Nehalem](http://en.wikipedia.org/wiki/Intel_Nehalem_(microarchitecture)) and [Westmere](http://en.wikipedia.org/wiki/Intel_Westmere_(microarchitecture)) [microarchitectures](http://en.wikipedia.org/wiki/Microarchitecture) have dedicated instructions that can [compute CRC checksums extremely efficiently](https://en.wikipedia.org/wiki/SSE4#SSE4.2).

{{<note info>}}You might think that you don't need CRC32 checksum in iSCSI as TCP already checksums its payload and the transmission errors are discovered by layer-2 checksums. Designers of iSCSI disagreed -- TCP checksum is a [simple sum of packet contents](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Checksum_computation) and thus a very weak error checking mechanism.{{</note>}}

**Why did Intel add TCP offload to its NICs?** Definitely not just to solve the iSCSI performance problems; iSCSI is just one of the high-bandwidth TCP applications, other such applications include web hosting of static content or [Netflix-style video streaming](/2009/07/netflix-summary/). Without TCP offload, an Intel-based server tops out at Fast Ethernet or Gigabit Ethernet speeds (with CPU running at 100% utilization). Offload functions in the Gigabit Ethernet controllers help you get the 10GE speeds at reasonable CPU loads.

{{<note>}}Last but not least, you might wonder why I'm interested in this topic. Chipsets and computer architectures were my first (geek) love before I've discovered networking. I've even designed and [wire-wrapped](http://en.wikipedia.org/wiki/Wire_wrap) my own [Z80](http://en.wikipedia.org/wiki/Z80)-based motherboard and run an [emulation of CP/M environment](http://en.wikipedia.org/wiki/CP/M) and [Turbo Pascal](http://en.wikipedia.org/wiki/Turbo_pascal) on it.{{</note>}}
