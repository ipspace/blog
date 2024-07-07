---
date: 2012-11-19 07:43:00+01:00
tags:
- VXLAN
- data center
- overlay networks
- virtualization
title: VXLAN Is Not a Data Center Interconnect Technology
url: /2012/11/vxlan-is-not-data-center-interconnect/
---
In [a comment](/2012/11/firewalls-in-small-private-cloud/#c8873447579367124924) to the [*Firewalls in a Small Private Cloud*](/2012/11/firewalls-in-small-private-cloud/) blog post I wrote "VXLAN is **NOT** a viable inter-DC solution" and [Jason wasn't exactly happy with my blanket response](/2012/11/firewalls-in-small-private-cloud/#c8490616425466768709). I hope Jason got a detailed answer in the [VXLAN Technical Deep Dive](http://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinar, here's a somewhat shorter explanation.
<!--more-->
**VXLAN is a layer-2 technology**. If you plan to use VXLAN to implement a data center interconnect, you'll be stretching a single L2 segment across two data centers.

You probably [know my opinion about the usability of L2 DCI](/2011/11/busting-layer-2-data-center/), but even [ignoring the obvious problems](/2011/06/stretched-clusters-almost-as-good-as/), current VXLAN implementations don't have the features one would want to see in a L2 DCI solution.

### What Should a L2 DCI Solution Have?

Assuming someone forced you to implement a L2 DCI, the technology you plan to use [SHOULD](https://tools.ietf.org/html/rfc2119) have these features:

- **Per-VLAN flooding control at data center edge**. Broadcasts/multicasts are usually not rate-limited within the data center, but should be tightly controlled at the data center edge (bandwidth between data centers is usually orders of magnitude lower than bandwidth within a data center). Ideally, you'd be able to control them per VLAN to reduce the noisy neighbor problems.
- **Broadcast reduction at data center edge**. Devices linking DC fabric to WAN core should implement features like ARP proxy.
- **Controlled unicast flooding**. It should be possible to disable flooding of unknown unicasts at DC-WAN boundary.

It's also nice to have the following features to reduce the [traffic trombones](/2011/02/traffic-trombone-what-it-is-and-how-you/) going [across the DCI link](/2010/09/long-distance-vmotion-and-traffic/):

- **First hop router localization**. Inter-subnet traffic should not traverse the DCI link to reach the first-hop router.
- **Ingress traffic optimization.** Traffic sent to a server in one data center should not arrive to the other data center first.

OTV in combination with FHRP localization and LISP (or load balancers with Route Health Injection) gives you an almost ideal (OK, make it the least dreadful) solution. VXLAN with hypervisor VTEPs has none of the above-mentioned features.

VXLAN gateway on Arista's 7150 is somewhat better, so you might be tempted to use it as solution that would connect two VLANs across an IP network, but don't forget that they haven't solved the redundancy issues yet -- you can have a single switch acting as a VXLAN gateway for a particular VLAN.

**Conclusion**: The current VXLAN implementations (as of November 2012) are a far cry from what I would like to see if being forced to implement a L2 DCI solution. Stick with OTV (it's now available on ASR 1K).
