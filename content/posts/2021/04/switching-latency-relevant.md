---
date: 2021-04-15 07:47:00+00:00
lastmod: 2021-05-01 18:19:00+02:00
networking-fundamentals_tag: deep
series_title: Is Switching Latency Relevant?
tags:
- switching
- networking fundamentals
title: 'Fundamentals: Is Switching Latency Relevant?'
---
One of my readers wondered whether it makes sense to buy low-latency switches from Cisco or Juniper instead of switches based on merchant silicon like Trident-3 or Jericho (regardless of whether they are running NX-OS, Junos, EOS, or Linux).

As always, the answer is *it depends*, but before getting into the details, let's revisit what latency really is. We'll start with a simple two-node network.

{{<figure src="/2021/04/latency-2nodes.png" caption="The simplest possible network">}}
<!--more-->
End-to-end latency is the time delay between first node sending the packet and the second node receiving the packet... but we need to be more precise than that. The latency that we can observe and measure from the outside is the delay between the first node *sending the first bit of the packet* and the second node *receiving the last bit of the packet* (at which point it can start processing the packet).

In our simple network, latency seems to have two components:

* **Serialization delay**: the time it takes to put all the bits on the wire. This component depends solely on the link speed.
* **Propagation delay**: the time it takes for a single bit to get across the cable. This component depends solely on the cable length and signal propagation speed.

To put things in perspective, here are a few typical serialization delays for a 1518-byte packet with a 8-byte preamble ([because Ethernet](https://en.wikipedia.org/wiki/Ethernet_frame)):

| Speed               | Latency |
|---------------------| ------: |
| ISDN (64 kbps)      | 190 ms  |
| Ethernet (10 Mbps)  | 1,22 ms |
| Gigabit Ethernet    | 12,2 µs |
| 10 GE               | 1,22 µs |
| 100 GE              | 0,122 µs|

Speed of signal propagation in a fiber optic cable is usually 70% of the speed of light in vacuum ([copper cables are a bit faster](https://www.arista.com/assets/data/pdf/Copper-Faster-Than-Fiber-Brief.pdf) -- HT [Adeilson Rateiro](https://www.linkedin.com/in/adeilson-rateiro-mba-46680329/)), or approximately 200.000 km/s, or 200 meters per microsecond.

In reality, there are two more components involved: transmit-side and receive-side transceivers. It's hard to get transceiver latency numbers, what I found (from an unreliable source) was 0.3 µs per link (transmit and receive) for SFP+ and 2.6 µs per link for 10GBASE-T. Pointers to better sources would be much appreciated.

{{<figure src="/2021/04/latency-phy.png" caption="Transceivers add latency (diagram from *Advanced Routing Protocols Topics* presentation)">}}

## Beyond Two Nodes

In a larger network, intermediate nodes have to receive packets, process them, put them in an output queue, and finally send them. 

{{<figure src="/2021/04/latency-switch.png" caption="Adding an intermediate node">}}

For every intermediate node you'll have to add:

* Switching (forwarding) latency;
* Output queuing delay;
* Serialization delay on output link unless the device uses cut-through switching.

To make matters even more interesting, there are two ways to measure switching (forwarding) latency (see Section 3.8 of [RFC 1242](https://tools.ietf.org/html/rfc1242) for details):

* In store-and-forward mode, latency is defined as the time interval between the last bit entering the switch and the first bit leaving the switch.
* In cut-through mode, switches become *bit forwarding devices* (using terminology from RFC 1242) -- latency is defined as the time interval between the first bit entering the switch and the first bit leaving the switch.

{{<figure src="/2021/04/latency-cut-through.png" caption="Cut-through Switching in a Nutshell">}}

Most data center switching vendors claim switching latency in microsecond range, with low-latency switches being below 500 nsec. Broadcom is claiming [Trident-3 forwarding latency is 900 nsec](https://docs.broadcom.com/doc/12395356), while its carefully chosen competitor has 11 µs forwarding latency (based on the marketing brouhaha from major vendors, they must have looked really hard to find someone so slow).

The best I could find on the router side was a Cisco Live presentation from 2016 claiming "tens of microseconds" for ASR Quantum Flow Processor. Yet again, I would appreciate pointers to better sources.

## Back to the Question

Coming back to the original question: does it matter? It might when you're running extremely latency-sensitive applications on high-speed links within a single data center. The moment you're using Gigabit Ethernet links, or sending data between multiple locations you probably shouldn't care any longer... unless, of course, you're in High Frequency Trading (HFT), in which case you don't care what I have to say about latency anyway.

{{<note>}}Some HFT companies went as far as building their own microwave links across a continent to reduce the propagation delay -- speed of light in air is pretty close to the maximum speed in vacuum.{{</note>}}

## Finally: Spot the Elephant

Hope you found the above discussion interesting, but it might be totally irrelevant, as I carefully avoided a few elephants in the room.

The first one is definitely congestion or queuing latency. Switching latency becomes irrelevant when you're dealing with an incast problem. 

The endpoint latency is probably a pod of blue whales compared to everything else we've been discussing, and worthy of another blog post... but it's well worth measuring and understanding. 

It doesn't make sense to optimize microseconds when the nodes connected to the network need milliseconds to respond. In other words: figure out what problem you're trying to solve, and focus on the lowest-hanging fruits first, regardless of which team is responsible for picking them.

Finally, someone also mentioned that *QoS can lower the latency even further*. Unfortunately, that's a red herring. QoS can lower the latency of high-priority traffic during periods of congestion by placing them at the front of the queue, but it cannot beat the laws of physics. No QoS tricks can reduce whatever the serialization or switching latency happen to be under idle conditions. Also, keep in mind that QoS tends to be a zero-sum game -- you give someone more resources at the expense of someone else. The only exception I'm aware of is link compression, but I haven't seen anyone doing that since the days of sub-Mbps Frame Relay or ISDN circuits.

## Revision History

2021-05-01
: Added a few pointers to the elephants strolling about the room
 
2021-04-16
: Added a link to an Arista document describing their measurement of copper/SMF/MMF latency
