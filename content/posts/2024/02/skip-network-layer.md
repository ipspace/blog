---
title: "Can We Skip the Network Layer?"
date: 2024-02-12 10:52:00+0100
tags: [ networking fundamentals ]
comment: |
  In early 2020 I created the _[Network Layer Addressing](https://my.ipspace.net/bin/get/Net101/NA3.1%20-%20Network%20Layer%20Addressing.mp4?doccode=Net101)_ video as part of the _[How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work)_. This blog post is an edited transcript of the first part of that video.
---
I mentioned that [you don't need node addresses when dealing with only two entities](/2023/09/addresses-in-network-stack.html). Now and then, someone tries to extend this concept and suggests that the network layer addressing isn’t needed if the solution is local. For instance, if we have a solution that is supposed to run only on a single Ethernet segment, we don’t need network layer addressing because we already have data link layer addresses required for Ethernet to work (see also: [ATAoE](https://blog.ipspace.net/2010/09/ataoe-for-converged-data-center.html)).

Too often in the past, an overly ingenious engineer or programmer got the idea to simplify everyone's life and use the data link layer addresses as the ultimate addresses of individual nodes. They would then put the transport layer on top of that to get reliable packet transport. Finally, put whatever application on top of the transport layer. Problem solved.
<!--more-->
{{<figure src="/2024/02/addr-local.png">}}

Digital Equipment Corporation (DEC) was very fond of this idea. One reason they wanted to eliminate the network layer was the complexity of DECnet, their network-layer protocol. It consumed a lot of memory in low-end 16-bit nodes like PCs or (in their case) terminal servers. Implementing proper DECnet in terminal servers would consume too much memory and CPU cycles.

{{<note info>}}Terminal servers were (relatively) cheap devices that allowed asynchronous terminals to be connected to DEC minicomputers over Ethernet.{{</note>}}

Someone came up with this "great" idea that they could design a dedicated protocol (LAT) for local-area terminal services. It would sit straight on top of Ethernet, making everyone's life easier. They even had another protocol called MOP, maintenance and operations protocol, that you could use to connect to the terminal server or download software to a terminal server. MOP was an early equivalent of a PXE boot.

As expected, things didn’t end well. They hit the wall when the first customer wanted to have two segments with terminal servers accessing the same computer, and the computer was not sitting between the two segments. Someone quickly came up with the idea that they could connect the two segments, but the laws of physics were as harsh in those days as they are now. In those days, a single Ethernet segment could be up to 500 meters long, but you couldn’t connect two of them.

And so someone dropped by Radia Perlman saying, well, Radia, we have this problem. We have these two Ethernet segments, and we need to make them into one segment because, you know, we’ve sold the solution to the customer, and the customer wants to stretch the whole thing. And we can’t do it because Ethernet was not designed that way.

Supposedly (so the myth goes), over a weekend, she designed transparent bridging and the spanning tree protocol (STP) that detects loops when you're connecting multiple transparent bridges in a redundant topology. The rest is history, and we’re still dealing with the consequences of someone having a great idea that it makes perfect sense to stretch a single data link layer across longer distances. Virtualization vendors (VMware in particular) went one step further -- their marketing departments and consultants keep suggesting that it makes sense to stretch a single segment across the continent and move virtual machines across that stretched VLAN. We'll leave that sad story for another day, but if you insist, I ranted against it too often.

**Lesson (not) learned**: there are sound engineering reasons for separate data-link- and network layers in a protocol stack.

{{<next-in-series page="/posts/2024/02/interface-node-addresses.md">}}**Coming up next:** Interface or Node Addresses?{{</next-in-series>}}
