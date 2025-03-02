---
date: 2022-09-08 06:33:00+00:00
networking-fundamentals_tag: deep
series:
- ethernet
tags:
- networking fundamentals
title: From Bits to Application Data
---
Long long time ago, Daniel Dib started an interesting Twitter discussion with [this seemingly simple question](https://twitter.com/danieldibswe/status/1537671262750879745):

> How does a switch/router know from the bits it has received which layer each bit belongs to? Assume a switch received 01010101, how would it know which bits belong to the data link layer, which to the network layer and so on.

As is often the case, Peter Paluch provided an [excellent answer in a Twitter thread](https://twitter.com/Peter_Paluch/status/1537822843601403904), and allowed me to save it for posterity.
<!--more-->
---

Ethernet frame has a fixed structure -- we know for sure that the header starts with the 6B destination MAC address, then 6B source MAC address, then 2B EtherType. 

Processing of the next bytes depends on the value in the EtherType; for example, if the EtherType says 0x8100, what follows is the VLAN tag; if the EtherType says 0x0800, what follows is the IPv4 packet with its header... but again, these all have fixed format.

In other words, if we get the start of the frame right in the incoming sequence of bits, we can parse it properly because we know exactly what to expect and when. That is why we have the methods to identify the start of a frame with the preamble and/or the SoF marker.

It's important to point out that a switch does not operate by acting on a received bit right after it arrives. Store-and-forward switches wait for the entire frame (delimited by the SoF and EoF markers), and only then chop it into headers and payload to process.

Cut-through switches also need to wait to accumulate enough bytes to have the headers fields needed to make a forwarding decision, and only then start passing the frame bits out the egress interface. A switch is never required to assign an arbitrary bit (or byte) to a layer without processing the preceding bits (bytes). This is perhaps the answer: When looking at a complete frame as a sequence of bits, we are never required to tell what layer does a particular n-th bit belong to without processing the previous bits.

We always start from the beginning of the frame, and start with the assumption that the starting bits (after preamble and SoF have been parsed) are L2, and move from there. L3 bits can be identified only after L2 has been completely processed, and so on.

---

The "only" remaining question is "_how do we identify the start of an Ethernet frame_". Original Ethernet used a [special sequence to indicate the start of a frame](https://en.wikipedia.org/wiki/Ethernet_frame#Ethernet_packet_%E2%80%93_physical_layer), and loss of signal to indicate the end of a frame; I covered several similar ideas in the _[Introducing Networking Challenges](https://my.ipspace.net/bin/get/Net101/L1.1%20-%20Introducing%20Networking%20Challenges.mp4?doccode=Net101)_ video (part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar).

