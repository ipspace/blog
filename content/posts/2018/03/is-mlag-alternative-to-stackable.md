---
date: 2018-03-22 08:22:00+01:00
mlag_tag: design
series:
- mlag
tags:
- link aggregation
- data center
title: Is MLAG an Alternative to Stackable Switches?
url: /2018/03/is-mlag-alternative-to-stackable/
---
Alex was trying to figure out how to use Catalyst 3850 switches and sent me this question:

> Is MLAG an alternative to use rather than physically creating a switch stack?

Let's start with some terminology.

**Link Aggregation Group (LAG)** is the ability to bond multiple Ethernet links into a single virtual link. LAG (as defined in 802.1ax standard) can be used between a pair of adjacent nodes. While that's good enough if you need more bandwidth it doesn't help if you want to increase redundancy of your solution by connecting your edge device to two switches while using all uplinks and avoiding the shortcomings of STP. Sounds a bit like trying to keep the cake while eating it.
<!--more-->
Enter the magical world of [MLAG](/series/mlag/) (Multichassis LAG) -- the ability to present two or more physical boxes (members of MLAG cluster) as a single logical device from LACP perspective.

Most MLAG implementations (apart from those based on ICCP or EVPN) are totally proprietary, and vendors use numerous tricks to get the job done. Some use central control plane with all other devices acting as stupid packet forwarders (aka SDN or stackable switches), in which case they\'re sort-of still running traditional LAG/LACP. Others use traditional distributed control plane with additional control-plane protocols between MLAG cluster members.

**Long story short**: stackable switches implement MLAG with centralized control plane.

To make matters even more confusing, vendors use different names for their MLAG implementations. Cisco vPC, Cisco VSS, HP IRF, Arista MLAG... do more-or-less the same thing from the perspective of an edge device.

To further confuse the innocent, some vendors call centralized control plane *stacking*, while getting the same results with the distributed control plane is called *MLAG*. Go figure.

#### Want to know more?

MLAG is covered in numerous webinars:

-   Some basics are covered in [Data Center 3.0 webinar](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers);
-   You'll find more details in [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) where you'll also find a discussion of control plane architectures;
-   Standard way of implementing MLAG with EVPN is described in [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.
-   I think I have the "SDN = stackable switches" pun in the [SDN 101](http://www.ipspace.net/Introduction_to_Software_Defined_Networking_(SDN)) webinar.

All these webinars are available with [standard ipSpace.net webinar subscription](http://www.ipspace.net/Subscription). SDN101 webinar is also available with [free subscription](http://www.ipspace.net/Subscription/Free).

#### Need more than just technology discussion?

-   Want to get fluent with data center fabrics? Check out the [Designing and Building Data Center Fabrics](http://www.ipspace.net/Designing_and_Building_Data_Center_Fabrics) online course.
-   Want to master all aspects of data center infrastructure while still remaining focused on networking infrastructure? It's time for [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
