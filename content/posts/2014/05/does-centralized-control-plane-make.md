---
comment: 'With Open Networking Foundation [adamantly promoting their definition of
  SDN](/2014/01/what-exactly-is-sdn-and-does-it-make.html), and based on experiences
  with previous (now mostly extinct) centralized architectures, one has to ask a simple
  question: does it make sense?


  Here’s what I thought in May 2014; for more details, read the [Packet Forwarding
  101](/series/forwarding.html) blog posts and watch the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)
  webinar.


  Also note that most of the solutions I listed as successful (limited) implementations
  of centralized control plane in 2014 withered in the meantime, and we''re back to
  distributed networking (this time often coupled with automated configuration deployment).

  '
date: 2014-05-08 07:04:00+02:00
sdn_101_tag: intro
series:
- sdn_101
series_weight: 180
tags:
- SDN
- OpenFlow
title: Does Centralized Control Plane Make Sense?
url: /2014/05/does-centralized-control-plane-make.html
---
A friend of mine sent me a challenging question:

> You\'ve stated a couple of times that you don\'t favor the OpenFlow version of SDN due to a variety of problems like scaling and latency. What model/mechanism do you like? Hybrid? Something else?

Before answering the question, let's step back and ask another one: "*Does* [*centralized control plane, as evangelized by ONF*](https://blog.ipspace.net/2014/01/what-exactly-is-sdn-and-does-it-make.html)*, make sense?*"
<!--more-->
### A Bit of History

As always, let's start with one of the greatest teachers: history. We've had centralized architectures for decades, from SNA to various WAN technologies (SDH/SONET, Frame Relay and ATM). They all share a common problem: when the network partitions, the nodes cut off from the central intelligence stop functioning (in SNA case) or remain in a frozen state (WAN technologies).

One might be tempted to conclude that the ONF version of SDN won't fare any better than the switched WAN technologies. Reality is far worse:

-   WAN technologies had little control-plane interaction with the outside world (example: Frame Relay LMI), and those interactions were run by the local devices, not from the centralized control plane;
-   WAN devices (SONET/SDH multiplexers, or ATM and Frame Relay switches) had local OAM functionality that allowed them to detect link or node failures and reroute around them using preconfigured backup paths. One could argue that those devices had local control plane, although it was never as independent as control planes used in today's routers.

{{<note>}}Interestingly, MPLS-TP wants to reinvent the glorious past and re-introduce centralized path management, yet again proving RFC 1925 section 2.11.{{</note>}}

The last architecture (that I remember) that used truly centralized control plane was SNA, and if you're old enough you know how well that ended.

### Would Central Control Plane Make Sense in Limited Deployments?

Central control plane is obviously a single point of failure, and network partitioning is a nightmare if you have a central point of control. Large-scale deployments of ONF variant of SDN are thus out of question. But does it make sense to deploy centralized control plane in smaller independent islands (campus networks, data center availability zones)?

Interestingly, numerous data center architectures already use centralized control plane, so we can analyze how well they perform:

-   Juniper XRE can control up to four EX8200 switches, or a total of 512 10GE ports;
-   Nexus 7700 can control 64 fabric extenders with 3072 ports, plus a few hundred directly attached 10GE ports[^FE];
-   HP IRF can bind together two 12916 switches for a total of 1536 10GE ports;
-   QFabric Network Node Group could control eight nodes, for a total of 384 10GE ports.

[^FE]: These were obviously marketing numbers: latest _Nexus OS Verified Scalability_ guide claims a Nexus 9500 switch (with a much more powerful CPU than the Nexus 7700) supports up to 1536 Fabric Extender server interfaces.

NEC ProgrammableFlow seems to be an outlier -- they can control up to 200 switches, for a total of over 9000 GE (not 10GE) ports... but they don't run any [control-plane protocol](https://blog.ipspace.net/2013/06/implementing-control-plane-protocols.html) (apart from ARP and dynamic MAC learning) with the outside world. No STP, LACP, LLDP, BFD or routing protocols.

One could argue that we could get an order of magnitude beyond those numbers if only we were using proper control plane hardware (Xeon CPUs, for example). I don't buy that argument till I actually see a production deployment, and do keep in mind that NEC ProgrammableFlow Controller uses decent Intel-based hardware. Real-time distributed systems with fast feedback loops are [way more complex than most people looking from the outside realize](https://blog.ipspace.net/2013/09/openflow-fabric-controllers-are-light.html) (see also RFC 1925, section 2.4).

### Does Central Control Plane Make Sense?

It does in certain smaller-scale environments (see above)... as long as you can guarantee redundant connectivity between then controller and controlled devices, or don't care what happens after link loss (see also [wireless access points](http://en.wikipedia.org/wiki/Wireless_access_point)). Does it make sense to generate a huge hoopla while reinventing this particular wheel? I would spend my energy doing something else.

{{<note>}}I absolutely understand why NEC went down this path -- they did something extraordinary to differentiate themselves in a very crowded market. I also understand why [Google decided to use this approach](https://blog.ipspace.net/2012/05/openflow-google-brilliant-but-not.html), and why they evangelize it as much as they do. I'm just saying that it doesn't make that much sense for the rest of us.{{</note>}}

Finally, do keep in mind that the whole world of IT is moving toward scale-out architectures. Netflix & Co are already there, and the enterprise world is grudgingly doing the first steps. In the meantime, OpenFlow evangelists talk about the immeasurable revolutionary merits of centralized scale-up architecture. They must be living on a different planet.

### More on SDN and OpenFlow

To learn more about the realities of OpenFlow and SDN, watch the [ipSpace.net SDN webinars](http://www.ipspace.net/Roadmap/SDN_and_OpenFlow_webinars).
