---
date: 2007-10-30 07:29:00+01:00
ospf_tag: details
tags:
- OSPF
title: More Details on OSPF Route Filters
url: /2007/10/more-details-on-ospf-route-filters.html
---
I did a few follow-up tests with the **distribute-list in** OSPF configuration command and stumbled across a few interesting facts (IOS release 12.4(15)T1 on a 3725 platform):

-   Although the router allows you to configure **distribute-list *acl* in *interface***, it does not work. Routes received through that interface (or having the interface as the next-hop) are not filtered.
-   When you apply the distribute-list in command, the routing table is not changed. Clearing the IP routing table does not help, you have to clear *ALL* OSPF processes (including bringing down all OSPF adjacencies) with the **clear ip ospf process** command for the route filter to take effect.
-   The same limitations don\'t apply in the other direction: when you remove the **distribute-list in**, SPF is triggered and the routes appear in the IP routing table automatically.
-   The [somewhat undocumented **gateway** option](http://www.cisco.com/univercd/cc/td/doc/product/software/ios124/124cr/hirp_r/rte_pih.htm#wp1122418) of the **distribute-list in** command works, but not quite as I would expect: the IP next hop, not the router-ID of the router advertising the IP prefix is matched by the prefix-list.

And, last but not least, I\'ve lab-verified my previous claim: applying the **distribute-list in** on a transit router can result in a black hole, as the LSAs themselves are not filtered.
