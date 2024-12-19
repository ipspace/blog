---
kb_section: EventDampening
minimal_sidebar: true
title: Increase the Stability of your Network
toc_title: Introduction
tags: [ IP routing ]
date: 2025-01-08 08:18:00+0100
alt_section: posts
index: true
url: /kb/Internet/EventDampening/
---
The introduction of real-time mission-critical applications into data networks has prompted many network designers to tune their routing protocols for faster convergence. While the resulting network can quickly detect failures and reroute around them, it usually becomes highly susceptible to repetitive failures (for example, a flapping interface), which can cause recurring instabilities in large parts of the network. A flapping interface can also cause significant data loss, as the data streams are constantly rerouted across the network following a routing protocol adjacency establishment and subsequent loss.
<!--more-->
To address this issue, Cisco introduced *IP Event Dampening*, an interface-level mechanism similar to BGP route dampening to Cisco IOS, IOS/XE, IOS-XR, and Nexus OS (Arista introduced a similar feature in EOS release 4.32.0F). In this article, you’ll see how you can use the IP Event Dampening on Cisco IOS to increase the stability of your network, as well as how you can cope with scenarios beyond this feature's scope.

{{<note migrated>}}
This article was written in 2007 and has been updated and republished on ipSpace.net in January 2025. The printouts were taken on an old release of Cisco IOS using serial interfaces, but I don't expect to see much change in the recent IOS or IOS/XE releases.
{{</note>}}

## Introduction to IP Event Dampening

The mathematical background used in the IP Event Dampening is identical to the one used in the BGP route dampening (described in RFC 2439):

* Whenever an interface changes its state from *up* to *down*, a penalty is applied to the interface. In Cisco IOS, the per-flap penalty is fixed at 1000 points and cannot be changed.

{{<note>}}You could also apply a penalty to interface restarts (for interfaces that differentiate restarts from carrier transitions).{{</note>}}

* The accumulated penalty decays exponentially with a configurable *half-time period* (the period in which the penalty is halved). The default half-time period for IP event dampening is five seconds.

{{<note info>}}The half-time period of 10 seconds would mean that the accumulated penalty of 1200 points would be 600 points after 10 seconds, 300 points after 20 seconds, and 150 points after 30 seconds.{{</note>}}

* If the accumulated penalty exceeds the *suppress threshold*, the interface is dampened (declared unreachable for routing protocol purposes, regardless of the actual interface state). The default value in Cisco IOS is 2000 points.
* A dampened interface becomes available when the accumulated penalty decays below the *reuse threshold.* Its default value is 1000 points.

{{<note>}}The *reuse threshold* should be several times lower than the *suppress threshold* to ensure that the sporadic interface flaps don’t cause flaps in the dampening algorithm.{{</note>}}

* As a large number of interface flaps could cause the interface to be dampened for an exceedingly long time, there is an upper limit on the penalty an interface can accrue. In Cisco IOS, the upper limit is fixed at 20000 points but could also be lower depending on the maximum suppression time you configure.

An example best illustrates these concepts. The following graph displays the results of IP event dampening using the Cisco IOS default values.

{{<figure caption="Sample IP event dampening scenario" src="Graph.jpg">}}

The interface state (the green line at the bottom of the graph) changed every half second for four seconds, accumulating 4000 penalty points. As the penalty started to decay immediately, the second flap did not bring the interface into the suppressed state (as the accumulated penalty had decayed to approximately 850 points at the time of the second flap), but the third one did. The interface remained suppressed (for routing protocol purposes) until the accumulated penalty (close to 3300 after the fourth flap) decayed to 1000 points (almost nine seconds after the last flap).
