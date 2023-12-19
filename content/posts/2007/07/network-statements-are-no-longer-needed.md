---
date: 2007-07-03 07:56:00+02:00
ospf_tag: config
tags:
- OSPF
title: Network Statements Are No Longer Needed in OSPF Configuration
url: /2007/07/network-statements-are-no-longer-needed.html
---
If you've ever had to configure OSPF on a Cisco router, you're well familiar with the venerable **network** statement, which effectively assigns interfaces into OSPF areas based on their IP addresses. Although our life became simpler when the [network statements stopped being order-dependent](https://blog.ipspace.net/2006/11/network-statements-in-ospf-process-are.html) (the order dependency allowed for a few nasty surprises in the troubleshooting part of the CCIE lab when the CCIE title still implied you had to be able to fix other people's mistakes :), it was still an awkward way of configuring what belongs where.
<!--more-->
In IOS release 12.3(11)T (integrated in 12.4), Cisco finally implemented OSPF the way it should have been implemented 20 years ago - you configure the OSPF area on individual interfaces with the **ip ospf *process* area *area-id*** interface configuration command.

The network statements still work as expected, and the per-interface command overrides whatever the network statement would do, so you have an extremely nice combination that allows you to assign all interfaces into a particular area (for example, **network 0.0.0.0 255.255.255.255 area 2**) and change the area for only a few interfaces (for example, uplinks into the backbone area).

{{<note warn>}}Interestingly, modern OSPF implementations like FRRouting still use both configuration mechanisms. FRRouting cannot use both simultaneously, resulting in hilarious results when you add a [half-baked abstraction layer](/2022/10/cumulus-linux-nvue.html) on top of its configuration CLI.{{</note>}}