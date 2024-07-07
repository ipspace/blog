---
date: 2009-06-08 07:23:00.004000+02:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP Load and Reliability Metrics
url: /2009/06/eigrp-load-and-reliability-metrics/
---
Everyone studying the EIGRP details knows the ["famous" composite metric formula](https://en.wikipedia.org/wiki/Enhanced_Interior_Gateway_Routing_Protocol#Routing_metric), but the recommendation to keep the K values intact (or at least leaving K2 and K5 at zero) or the inability of EIGRP to adapt to changing load conditions is rarely understood.

[IGRP](http://en.wikipedia.org/wiki/Interior_Gateway_Routing_Protocol), the EIGRP's predecessor, had the same vector metric and very similar composite metric formula, but it was a true distance vector protocol (like RIP), advertising its routing information at regular intervals. The interface load and reliability was thus regularly propagated throughout the network and so it made sense to include them in the composite metric calculation (although this practice could lead to unstable or oscillating networks).

EIGRP routing updates are triggered only by a change in network topology (interface up/down event, IP addressing change or configured bandwidth/delay change) and not by change in interface load or reliability. The load/reliability numbers are thus a snapshot taken at the moment of the topology change and should be ignored.

{{<note info>}}Sending EIGRP updates whenever there's a significant change in load or reliability would be technically feasible, but would diminish the benefits of replacing distance vector behavior with DUAL.{{</note>}}

You might be wondering why Cisco decided to include the *load* and *reliability* into the EIGRP vector metric. The total compatibility of IGRP and EIGRP vector metrics allowed them to implement smooth IGRP-to-EIGRP migration strategy with automatic propagation of vector metrics in redistribution points, including the IGRP-EIGRP-IGRP redistribution scenario used in IGRP-to-EIGRP core-to-edge migrations.
