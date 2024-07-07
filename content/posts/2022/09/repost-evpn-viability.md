---
date: 2022-09-27 06:53:00+00:00
evpn_tag: rant
series_title: On the Viability of EVPN
tags:
- EVPN
- VXLAN
title: 'Repost: On the Viability of EVPN'
---
Jordi left an [interesting comment](/2022/09/mlag-bridging-evpn/#1375) to my *[EVPN/VXLAN or Bridged Data Center Fabrics](/2022/09/mlag-bridging-evpn/)* blog post discussing the viability of using VXLAN and EVPN in times when the equipment lead times can exceed 12 months. Here it is:

---

Interesting article Ivan. Another major problem I see for EPVN, is the incompatibility between vendors, even though it is an open standard. With today’s crazy switch delivery times, we want a multi-vendor solution like BGP or LACP, but EVPN (due to vendors) isn’t ready for a multi-vendor production network fabric.
<!--more-->
Another issue with EVPN is cost in terms of price and project (delivery times). To have a robust & stable solution you should start with Trident III as if you go with Tomahawk I you will need re-circulation (and I would suggest avoiding that) and with Trident II+ you lack 100Gbps and 25Gbps, which it is the standard today. There are not many Trident III switches today in the secondhand market and a new one would take 1 year to be delivered. Without EVPN, you could obtain a Tomahawk switch for half the price and even lower latency if that nanosec difference really matters to you.

Another problem, that vendors have been solving lately with ranges, was the kilometer long configuration in EVPN and uniqueness with the RD for each VNI per switch, making the list of config even longer than in head-end replication.

And all these without mentioning the bugs that each vendor has when using EVPN on their switches…. Making it an unstable feature to turn on today. In the other hand, EVPN Multi-homing, on paper, solve lots of issues

---

There's so much to unpack here, and I'd love to hear your feedback on some of the issues Jordi raised as it looks like I'm still living in a forward-looking bubble.

**Hardware** issues have nothing to with EVPN and all to do with *routing in and out of VXLAN tunnels* (RIOT). If you're doing pure bridging, you should[^THS] be just fine using Tomahawk-based switches regardless of whether you use head-end replication or EVPN.

[^THS]: I guess the exact value of *should* depends on the switch vendor and the underlying hardware. I wouldn't be surprised to find a vendor that insists on using VXLAN RIOT the moment you configure EVPN.

**Configuration** verbosity is a huge deal unless you automate it (yeah, I know, I'm getting tiresome), although it's not that bad on Cumulus Linux or if you use VLAN bundles[^VLB] on Arista. Adding layer-3 to the mix obviously increases the configuration significantly.

[^VLB]: Attaching the same RD/RT to numerous VNIs -- an approach that's a perfect fit for the common *every VLAN everywhere* data center design. Unfortunately, some vendors don't support VLAN bundles.

{{<note info>}}If you're interested in templating EVPN configuration, check out the [templates](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/templates/evpn) we use in *[netlab](https://netlab.tools/)*. They will also give you an indication of how much extra configuration every VLAN or VRF brings.{{</note>}}

**Vendor bugs** have been a huge nuisance in the early days of EVPN -- I knew a customer that needed an extra year to roll out a data center hardware upgrade because they insisted on using VXLAN with EVPN multihoming instead of head-end replication with MLAG cluster -- but that was years ago. Are the bugs still haunting you?

Vendors claim they solved the **interoperability** issues, and proudly point to [interoperability test reports](https://eantc.de/fileadmin/eantc/downloads/events/2022/EANTC-InteropTest2022-TestReport.pdf) to prove that life in the EPVN land is beautiful and rosy.

The reality is a bit different. As Dinesh Dutt pointed out in the *[Multivendor Data Center EVPN](https://my.ipspace.net/bin/list?id=EVPN#MULTIVENDOR)* part of *[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)* webinar, things usually work if you're using IBGP EVPN on top of IGP (OSPF or IS-IS) -- the design promoted by almost no vendor[^BIW].

[^BIW]: ...because it's simple and works reasonably well in multi-vendor setup? Nah, that's just a conspiracy theory 😜

You might get an interesting blob of complexity if you blindly follow vendor recommendations and build [EBGP-only fabric](/series/dcbgp/) or [run EVPN IBGP between loopback interfaces advertised with underlay EBGP](/2020/02/the-evpnbgp-saga-continues/). At the very minimum, you will have to configure route targets as every EVPN implementation uses a different approach to deal with route targets of EVPN instances spanning multiple autonomous systems. Finally, building a multi-vendor IBGP-over-EBGP fabric with EVPN-based multihoming seems to be a decent bet if you're looking for a long-time job security.