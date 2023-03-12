---
date: 2014-05-12 07:58:00+02:00
openflow_101_tag: intro
series:
- openflow_101
series_weight: 140
tags:
- OpenFlow
title: Is OpenFlow Useful?
url: /2014/05/is-openflow-useful_12.html
---
The [*Does Centralized Control Plane Make Sense*](https://blog.ipspace.net/2014/05/does-centralized-control-plane-make.html) post triggered several comments along the lines of "*do you think there's no need for OpenFlow?*"

**TL;DR version**: OpenFlow is just a low-level tool; don't blame it for how it's being promoted... but once you figure out it's nothing more than TCAM (ACL+PBR) programming tool, you'll quickly find a few interesting use cases. If only [we'd have hardware we could use to implement them](/2022/05/openflow-still-kicking.html); most vendors gave up years ago.
<!--more-->
[OpenFlow is just a tool](https://blog.ipspace.net/2011/04/what-is-openflow.html) that allows you to install PBR-like forwarding entries into networking devices using a standard protocol that *should* work across multiple vendors. From this perspective, OpenFlow offers slightly more advanced functionality than BGP FlowSpec.

Where could you use PBR-like functionality? I'm positive you already have a dozen ideas with [various levels of craziness](https://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html); here are a few more:

-   [Network monitoring](http://demo.ipspace.net/get/3%20-%20Network%20Monitoring.mp4) (flow entries have counters);
-   [Intelligent SPAN ports](http://demo.ipspace.net/get/4%20-%20Tap%20Aggregation%20Networks.mp4) that collect only the traffic you're interested in;
-   [Transparent service insertion](http://demo.ipspace.net/get/5%20-%20Service%20Insertion.mp4);
-   [Scale-out stateful network services](http://demo.ipspace.net/get/6%20-%20Scale-out%20Load%20Balancing.mp4);
-   [Distributed DoS prevention](http://demo.ipspace.net/get/7%20-%20Distributed%20DoS%20Prevention.mp4);
-   [Policy enforcement](http://demo.ipspace.net/get/8%20-%20Edge%20Policy%20Enforcement.mp4) (read: ACLs) at the network edge.

OpenFlow has another advantage over BGP FlowSpec -- it has the *packet-in* and *packet-out* functionality that allows the controller to communicate with the devices outside of the OpenFlow network. You could use this functionality to implement [new control-plane protocols](https://blog.ipspace.net/2013/06/implementing-control-plane-protocols.html) or (for example) interesting layered authentication scheme that is not available in off-the-shelf switches.

**Summary**: OpenFlow is a low-level tool that can help you implement numerous interesting ideas, but I wouldn't spend my time reinventing the switching fabric (or [other things we already do well](http://networkheresy.com/2011/11/17/is-openflowsdn-good-at-forwarding/)).

For more information, watch the [ipSpace.net SDN webinars](http://www.ipspace.net/Roadmap/SDN_and_OpenFlow_webinars) (some of them are free).
