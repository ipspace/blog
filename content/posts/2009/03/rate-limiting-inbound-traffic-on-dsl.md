---
date: 2009-03-27 07:23:00.007000+01:00
tags:
- QoS
title: Rate-limiting Inbound Traffic on DSL
url: /2009/03/rate-limiting-inbound-traffic-on-dsl.html
---
Julian is faced with an interesting challenge:

> In the real world, many customers using DSL solutions have their Internet connection disrupted by one internal user performing a large download. On a typical DSL solution, implementing quality of service on outbound traffic is trivial (you can use PQ, CBWFQ, policing or shaping). However, how does one rate-limit inbound traffic in a sensible fashion? Turnkey solutions like packeteer allow inbound classes of traffic like HTTP to be rate limited per flow by dynamically changing window sizes.

Cisco IOS has three basic QoS mechanisms: queuing, shaping and policing. It cannot intercept a TCP session and slow it down by reducing its window size (like [PacketShaper](http://www.bluecoat.com/products/packetshaper)).
<!--more-->
A queuing mechanism works only if the (temporary) [packet arrival rate is higher than the interface transmission rate and thus an output queue forms](/kb/tag/QoS/Queuing_Principles.html). When the router receives packets from a DSL link and sends them to an Ethernet link, the output queue remains almost empty and thus you cannot use any queuing mechanism.

[Policing works regardless of the size of the output queue](/kb/tag/QoS/QoS_Policing.html), but it cannot be fine-tuned to react to interface congestion (unless you use EEM interface triggers to detect high interface utilization). Furthermore, IOS does not have proportional policing of individual traffic flows.

The only remaining mechanism is shaping: you have to create an artificial bottleneck on the outbound (LAN) interface with the **shape** MQC command. The shaping rate should be less than the [useful speed of your DSL link](https://blog.ipspace.net/2009/03/adsl-overhead.html). The **shape** command introduces a bottleneck: the packets arrive through the DSL interface faster than they can be sent to the (shaped) LAN interface. Now you have an output queue that you can influence with further QoS policies (you need to configure hierarchical MQC). Without further configuration, the output queue created with the **shape** command uses per-flow weighted fair queuing, giving each layer-4 session a fair share of the bandwidth.

The output rate configured with the **shape** command has to be significantly smaller than the DSL rate, otherwise the output queue forms only sporadically. By shaping the inbound DSL packets on the LAN interface you reduce the maximum throughput, slightly increase latency and introduce jitter.
