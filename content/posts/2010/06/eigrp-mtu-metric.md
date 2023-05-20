---
date: 2010-06-08 07:34:00+02:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP MTU “metric”
url: /2010/06/eigrp-mtu-metric.html
---
Every so often I get a question about the MTU metric in EIGRP and whether it's used at all or not. It actually is: if your router would have to ignore some equal-cost paths to the same destination (the number of equal-cost paths exceeds the value of the **maximum-paths** router configuration parameter), it ignores those with the lowest MTU metric.
<!--more-->
The MTU metric behaves [similarly to the *load* and *reliability* metrics](https://blog.ipspace.net/2009/06/eigrp-load-and-reliability-metrics.html):

-   A change in the MTU does not trigger a routing update.
-   Whenever a "real" change in topology triggers an EIGRP update, the MTU metric is updated to reflect the then-current [interface **ip mtu** value](https://blog.ipspace.net/2007/10/tale-of-three-mtus.html).

When processing inbound EIGRP updates, the minimum of the MTU value in the inbound UPDATE packet and the interface MTU is stored in the EIGRP topology database. No MTU processing is done on the outbound updates. The MTU metric thus represents the minimum unidirectional MTU between the current router and the originating router.
