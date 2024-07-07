---
date: 2009-05-22 06:30:00+02:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP Neighbor Loss Detection
url: /2009/05/eigrp-neighbor-loss-detection/
---
Vijay sent me an interesting EIGRP query:

> I know EIGRP hello packets are used to discover and maintain EIGRP neighborship and when an EIGRP router doesn't receive a hello packet from its neighbor within the Hold timer, that router will be declared dead. But when would EIGRP declare a neighbor dead after sending 16 unicast packets?

The primary mechanism to detect EIGRP neighbor loss is the hello protocol. It's a bit unreliable as it does not detect unidirectional communication, but has an interesting advantage that you can use asymmetrical hello/hold timers (each router can specify what hold timer its neighbors should use for its hello packets).
<!--more-->
However, the EIGRP neighbor loss might also be detected during the network convergence phase. EIGRP requires reliable routing updates; each neighbor thus has to acknowledge every packet sent to it. If a neighbor does not reply to a multicast packet (or a unicast packet in point-to-point and NBMA networks), the sending router switches to unicast and retries to send the packet up to 16 times. If the retransmissions fail, the EIGRP neighbor is also declared dead.

This behavior helps to avoid weird conditions including unidirectional communication that cannot be detected with HELLO packets. It also ensures that the network convergence completes in a reasonable time frame (EIGRP might use hold times up to 180 seconds on low-speed Frame Relay links).
