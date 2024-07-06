---
comment: 'My [Open Networking Foundation rant](/2011/03/open-networking-foundation-fabric.html)
  got several thoughtful responses focusing on “*what is OpenFlow and what can we
  do with it?*” Let’s start with the easy part first: What exactly is OpenFlow?

  '
date: 2011-04-05 07:12:00.002000+02:00
openflow_101_tag: intro
series:
- openflow_101
series_weight: 280
tags:
- SDN
- switching
- data center
- OpenFlow
title: What is OpenFlow?
url: /2011/04/what-is-openflow.html
---
A typical networking device (bridge, router, switch, LSR ...) has [*control* and *data* plane](/2013/08/management-control-and-data-planes-in.html). The control plane runs all the control protocols (including port aggregation, STP, TRILL, MAC address learning and routing protocols) and downloads the forwarding instructions into the *data plane* structures, which can be simple lookup tables or specialized hardware (hash tables or TCAMs).
<!--more-->
In distributed architectures, the control plane has to use a communications protocol to download the forwarding information into data plane instances. Every vendor uses its own proprietary protocol (Cisco uses IPC – *InterProcess Communication* – to implement distributed CEF); OpenFlow tries to define a standard protocol between control plane and associated data plane elements.

The OpenFlow zealots would like you to believe that we’re just one small step away from implementing [Skynet](http://en.wikipedia.org/wiki/Skynet_(Terminator)); the reality is a bit more sobering. You need a protocol between control and data plane elements in all distributed architectures, starting with modular high-end routers and switches. Almost every modular high-end switch that you can buy today has one or more supervisor modules and numerous linecards performing distributed switching (preferably over a crossbar matrix, not over a shared bus). In such a switch, OpenFlow-like protocol runs between supervisor module(s) and the linecards.

Moving into more distributed space, the [Borg fabric architectures](/2011/03/data-center-fabric-architectures.html) use an OpenFlow-like protocol between the central control plane and forwarding instances. You might have noticed that all vendors link at most two high-end switches into Borg architecture at the moment; this decision has nothing to do with vendor lock-in and lack of open protocols but rather reflects the practical challenges of implementing a high-speed distributed architecture (alternatively, you might decide to believe the whole networking industry is a confusopoly of morons who are unable to implement what every post-graduate student can simulate with open source tools).

Moving deeper into the technical details, the [*Technical Specifications*](https://opennetworking.org/software-defined-standards/specifications/) page on the [Open Networking Foundation web site](https://opennetworking.org/) contains a links to numerous versions of OpenFlow Switch Specification, which defines:

-   OpenFlow tables (the TCAM structure used by OpenFlow);
-   OpenFlow channel (the session between an OpenFlow switch and an OpenFlow controller);
-   OpenFlow protocol (the actual protocol messages and data structures).

The designers of OpenFlow had to make the TCAM structure very generic if they wanted to offer an alternative to numerous forwarding mechanisms implemented today. Each entry in the *flow tables* contains the following fields: ingress port, source and destination MAC address, ethertype, VLAN tag & priority bits, MPLS label & traffic class, IP source and destination address (and masks), layer-4 IP protocol, IP ToS bits and TCP/UDP port numbers.

To make the data plane structures scalable, OpenFlow introduces a concept of multiple flow tables linked into a tree (and group tables to support multicasts and broadcasts). This concept allows you to implement multi-step forwarding, for example:

-   Check inbound ACL (table \#1)
-   Check QoS bits (table \#2)
-   Match local MAC addresses and move into L3/MPLS table; perform L2 forwarding otherwise (table \#3)
-   Perform L3 or MPLS forwarding (tables \#4 and \#5).

You can pass *metadata* between tables to make the architecture even more versatile.

{{<note>}}OpenFlow 1.0 uses a single TCAM (flow table) and is thus totally boring compared to rich OpenFlow 1.1+ functionality.{{</note>}}

The proposed flow table architecture is extremely versatile (and I’m positive someone got their PhD proving that it is a superset of every known and imaginable forwarding paradigm), but it failed miserably when meeting the harsh reality of switching ASICs, which [made OpenFlow obsolete within a decade after it was launched](/2022/05/openflow-still-kicking.html).

### Revision History

2022-07-15
: Replaced links to OpenFlow specs, and changed the last paragraph to reflect the reality.