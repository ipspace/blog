---
date: 2007-04-18 11:56:00+02:00
eigrp_tag: details
tags:
- EIGRP
title: Changes in EIGRP Summary Address Are no Longer Disruptive
url: /2007/04/changes-in-eigrp-summary-address-are-no.html
pre_scroll: True
---
Early EIGRP implementation treated changes in EIGRP summary address configuration (configured with the **ip summary-address eigrp** interface configuration command) very disruptively: all EIGRP sessions across the affected interface were cleared, sometimes resulting in a large number of routes entering *active* state, potentially leading to a *stuck-in-active* condition.
<!--more-->
Newer Cisco IOS releases are more lenient: router with a change in summary address requests a resync (logged as graceful-restart on adjacent routers). A lot of updates and queries are still sent, but the adjacencies themselves are preserved:

-   When configuring a summary route, all more specific prefixes on downstream routers enter *active* state.
-   When a summary is removed, only the summary prefix itself enters *active* state and the affected router sends queries to all its neighbors, while the more specific prefixes are sent as regular EIGRP updates to the neighbors across the affected interface.

A change in EIGRP summary generates the following output on the router under configuration:

```a1(config)#interface serial 0/0/0.100
a1(config-subif)#ip summary-address eigrp 1 0.0.0.0 0.0.0.0
%DUAL-5-NBRCHANGE: IP-EIGRP(0) 1: Neighbor 172.16.1.2 (Serial0/0/0.100) is resync: summary configured
a1(config-subif)#no ip summary-address eigrp 1 0.0.0.0 0.0.0.0
%DUAL-5-NBRCHANGE: IP-EIGRP(0) 1: Neighbor 172.16.1.2 (Serial0/0/0.100) is resync: summary configured
```

The downstream router generates similar log messages:

```
%DUAL-5-NBRCHANGE: IP-EIGRP(0) 1: Neighbor 172.16.1.1 (Serial0/0/0.100) is resync: peer graceful-restart
```
