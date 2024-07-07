---
date: 2009-04-27 06:43:00+02:00
lastmod: 2020-12-29 09:23:00
ospf_tag: details
tags:
- IS-IS
- OSPF
title: SPF Events in OSPF and IS-IS
url: /2009/04/spf-events-in-ospf-and-is-is/
---
Link-state algorithms select the best routes through a two-step process:

1.  The topology of the area is analyzed using SPF algorithm, resulting in a shortest-path tree. This tree contains the shortest paths from the current router to any other node (router or transit LAN) in the current area. This step performed with the Shortest Path First (SPF) algorithm.
2.  The best routes are selected based on the advertisements from all routers in the area (including inter-area and external routes in case of OSPF). The route selection is a simple distance-vector operation where the router selects the minimum-cost IP prefixes from the set of all advertised IP prefixes.
<!--more-->
{{<ct3_rescue>}}

The SPF algorithm is CPU-intensive and is thus heavily throttled: the router will not execute the SPF algorithm until a predefined timeout has expired from the event triggering the SPF (goal: collect as many changes as possible in the topology database to prevent multiple SPF runs) and will not execute subsequent SPF run until the inter-SPF interval expires (goal: minimize CPU utilization in case of severe network instability).

{{<note>}}Use the **timers throttle spf** router configuration command to adjust OSPF SPF timers and the **spf-interval** router configuration command to adjust IS-IS SPF timers.{{</note>}}

The best route selection after the shortest path tree is built is not computationally complex and not as heavily throttled. The best route selection after the SPF tree has been built is called *partial SPF* in OSPF debugging printouts (although it has nothing to do with the SPF algorithm) and *partial route calculation* (PRC) in IS-IS. Partial SPF in OSPF is executed as soon as the change is noticed. Cisco IOS implementation of IS-IS supports PRC throttling with the **prc-interval** router configuration command.

To understand the impacts of a topology change (interface state change, router reload or configuration change) on the network and its individual areas, it’s of vital importance to understand which events trigger the SPF run (these events will cause high CPU utilization and delayed network convergence) and which events result in route selection process (partial SPF/PRC). The following table summarizes events that cause OSPF or IS-IS to run full SPF algorithm:

**OSPF SPF-triggering events**
* Transit interface change (P2P or LAN)
* Stub interface state change
* Stub interface IP address change

**IS-IS SPF-triggering events**
* Transit interface change

**Events triggering a partial SPF run**
* Stub interface state or IP address change (IS-IS only)
* Inter-area route loss/addition
* Inter-area cost change
* Redistributed route loss/addition
* Redistributed route cost change

**Notes:**

1.  Interfaces over which the link-state routers have established adjacencies are *transit* interfaces. Interfaces with no link-state neighbors are *stub* interface (a LAN interface with multiple routers but no link-state adjacency is still a stub interface).
2.  IP address change on a stub interface causes SPF run in OSPF only if the changed IP address belongs to a different IP subnet. For example, changing 10.0.0.1/24 to 10.0.0.2/24 on a stub interface will not cause an SPF run.
3.  Stub prefixes are advertised as part of type-1 LSA in OSPF, resulting in a full SPF run on every change.
4.  Stub prefixes are advertised like any other IP prefix in IS-IS, resulting in partial route calculation.
3.  Under certain circumstances, even changing an IP address on a transit interface does not trigger SPF event in IS-IS.
4.  When an OSPF area border router (ABR) experiences an interface state change, it floods new router LSA (and triggers SPF event) in all adjacent areas, regardless of the area in which the actual change has occurred.
5.  I wrote about the distance vector aspects of OSPF in 2008. You'll find the article somewhere in [this list](/kb/Internet/).

