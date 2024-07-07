---
date: 2011-03-15 07:21:00.001000+01:00
tags:
- bridging
- data center
- workshop
title: Does Bridge Assurance Make UDLD Obsolete?
url: /2011/03/does-bridge-assurance-make-udld/
---
I got an interesting question from Andrew:

> Would you say that [*bridge assurance*](http://www.cisco.com/en/US/docs/switches/lan/catalyst6500/ios/12.2SX/configuration/guide/stp_enha.html#Understanding_Bridge_Assurance) makes UDLD unnecessary? It doesn\'t seem clear from any resource I\'ve found so far (either on Cisco\'s docs or on Google)."

It's important to remember that UDLD works on *physical links* whereas bridge assurance works *on top of STP* (which also implies it works above link aggregation/port channel mechanisms). UDLD can detect individual link failure (even when the link is part a LAG); bridge assurance can detect unaggregated link failures, total LAG failure, misconfigured remote port or a malfunctioning switch.
<!--more-->
Some of the reasons you might want to prefer UDLD would thus include:

-   UDLD can detect link problems even when you disable spanning tree (for example, on layer-2 data center interconnect links);
-   If you cannot use BFD, you can run UDLD on routed interfaces to detect link problems faster than the routing protocol hello mechanisms would;
-   You can run UDLD on individual ports of a static port channel (for example, redundant ports in a layer-2 DCI).

The benefits of Bridge Assurance are also obvious:

-   It can detect STP configuration problems;
-   You can use it in a mixed-vendor environment, whereas you can use UDLD only between a pair of Cisco's switches.

In complex designs, you'll probably end up using both.

### More information

To learn more about BFD, read the article I wrote about it in early 2000s. You'll find it somewhere in [this list](/kb/Internet/).
