---
date: 2010-06-08 07:34:00+02:00
lastmod: 2023-10-04 10:15:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP MTU “metric”
url: /2010/06/eigrp-mtu-metric/
---
Every so often I get a question about the MTU metric in EIGRP and whether it's used at all or not. It's supposed to be used (at least it was decades ago): if your router would have to ignore some equal-cost paths to the same destination (the number of equal-cost paths exceeds the value of the **maximum-paths** router configuration parameter), it would ignore those with the lowest MTU metric.

After an email exchange with [Carlos G Mendioroz](https://www.linkedin.com/in/carlos-g-mendioroz-7230851/), I retested the above behavior with Cisco IOSv release 15.6(1)T in 2023. EIGRP MTU-related behavior changed since I last looked (in 2010): it no longer considers MTU when selecting a subset of equal-cost paths; the most stable (oldest) paths stay in the IP routing table regardless of their MTU value in the EIGRP topology table.
<!--more-->
From the information propagation perspective, the MTU metric behaves [similarly to the *load* and *reliability* metrics](/2009/06/eigrp-load-and-reliability-metrics/):

-   A change in the MTU does not trigger a routing update.
-   Whenever a "real" change in topology triggers an EIGRP update, the MTU metric is updated to reflect the then-current [interface **ip mtu** value](/2007/10/tale-of-three-mtus/).

When processing inbound EIGRP updates, the minimum of the MTU value in the inbound UPDATE packet and the interface MTU is stored in the EIGRP topology database. No MTU processing is done on the outbound updates. The MTU metric thus represents the minimum unidirectional MTU between the current router and the originating router.

### Revision History

2023-10-04
: EIGRP no longer considers MTU when selecting best paths

