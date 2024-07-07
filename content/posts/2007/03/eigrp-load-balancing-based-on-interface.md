---
date: 2007-03-31 08:18:00+02:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP Load Balancing Based on Interface Load
url: /2007/03/eigrp-load-balancing-based-on-interface/
---
**TL&DR**: Don't.

EIGRP computes its composite metric from five parameters, one of them being interface load, therefore raising the theoretical possibility of having route metrics that include interface load. However, tweaking EIGRP K-values with the `metric weights` command to include interface load in metric calculations is highly discouraged -- every change in interface load could lead to network instability.
<!--more-->
Even worse, whenever an interface load would increase, the increased composite metric of the affected routes in EIGRP topology table would cause them to enter *active* state (and the router to start the DUAL algorithm trying to find more optimum paths toward the destination).

To make the whole idea even more impractical, EIGRP does not scan the interface load (and other parameters influencing the metric) on periodical basis, but only when triggered by a change in network topology (for example, interface or neighbor up/down event).