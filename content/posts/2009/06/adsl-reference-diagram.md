---
date: 2009-06-22 06:38:00.003000+02:00
tags:
- WAN
- ADSL
title: ADSL Reference Diagram
url: /2009/06/adsl-reference-diagram/
lastmod: 2020-12-07 17:01:00
---
I'm getting lots of ADSL QoS questions lately[^1], so it's obviously time to cover this topic. Before going into the QoS details, I want to make sure my understanding of the implications of the [baroque ADSL protocol stack](/2009/03/adsl-overhead/) is correct.

In the most complex case, a DSL service could have up to eight separate components (including the end-user's workstation):
<!--more-->

{{<figure src="/2009/06/ADSL_Reference_Diagram.png" caption="From end-user to core ISP network: ADSL components">}}

1.  End-user workstation sends IP datagrams to the local (CPE) router.
2.  CPE router runs PPPoE session with the NAS (Network Access Server) and sends Ethernet datagrams to the DSL modem.
3.  DSL modem encapsulates Ethernet frames in RFC 1483 framing, slices them in ATM cells and sends them over the physical DSL link to DSLAM.
4.  DSLAM performs physical level concentration and sends the ATM cells (one VC per subscriber) into the network.
5.  The backhaul network (DSLAM to NAS) could be partly ATM based. The ATM cells could thus pass through several ATM switches.
6.  Eventually the ATM cells have to be reassembled into PPPoE frames. In a worst-case scenario, an ATM-to-Ethernet switch would perform that function.
7.  The backhaul network could be extended with Ethernet switches.
8.  Finally, the bridged PPPoE frames arrive @ NAS which terminates the PPPoE session and emits the IP datagrams into the IP core network.

I sincerely hope no network is as complex as the above diagram. In most cases, the backhaul would be either completely ATM-based ...

{{<figure src="/2009/06/ADSL_Reference_Diagram_ATM.png" caption="ADSL access network with ATM backhaul">}}

... or Ethernet based (when the DSLAM has Ethernet uplink interface):

{{<figure src="/2009/06/ADSL_Reference_Diagram_Ethernet.png" caption="ADSL access network with Ethernet backhaul">}}

The NAS could also be adjacent to DSLAM or even integrated in the same chassis.

Am I missing anything important? I know you could deploy numerous additional devices (for example, Cisco is promoting the [Service Exchange Framework](http://www.cisco.com/en/US/netsol/ns746/networking_solutions_sub_solution.html) and [Service Control Engine](http://www.cisco.com/en/US/netsol/ns746/networking_solutions_sub_solution.html)), but these devices would be placed deeper into the IP core.

[^1]: It's not that ADSL would become popular in 2020. I wrote the blog post in 2009, and recreated the diagrams from old drawings in 2020.