---
date: 2010-08-03 07:10:00.003000+02:00
eigrp_tag: basic
tags:
- EIGRP
title: EIGRP Myths Debunked
url: /2010/08/eigrp-myths-debunked.html
---
[Matthew Norwood](http://twitter.com/matthewnorwood) performed a really thorough EIGRP research and [unearthed a lot of myths around it](http://networktherapy.wordpress.com/2010/07/29/how-much-do-you-really-know-about-technology-x), some of them coming from official documentation, Cisco Press books (hopefully not [mine](http://www.amazon.com/gp/product/1578701651?ie=UTF8&tag=cisioshinandt-20&linkCode=xm2&camp=1789&creativeASIN=1578701651)) and other sources. It's time to debunk a few of them (read the [comments to Matthew's post](#comment-7) to find the sources of the following "wisdoms").

{{<note info>}}To learn more about routing protocols, watch our [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar{{</note>}}

**EIGRP is a hybrid routing protocol**. If I remember correctly, this one comes straight from the first EIGRP presentations Dino had @ Networkers years ago and is usually interpreted as "EIGRP has the best features of Distance Vector and Link State routing protocols". Completely wrong, EIGRP has zero LS features. Correct classification would be "EIGRP is an advanced Distance Vector routing protocol" and the [Wikipedia entry on EIGRP](#EIGRP_classification_as_a_distance-vector) is almost spot-on.
<!--more-->
**EIGRP is a distance vector routing protocol**. Not bad, but not completely true either. Wikipedia has a nice wording: "EIGRP is not a naïve DV routing protocol". EIGRP differs from other DV routing protocols in the way it handles lost routes (or routes with increased metric). All other DV routing protocols passively wait to get potentially better information from their neighbors (some of them, including RIP, even lock down the path to prevent loops), while EIGRP takes a more active approach (now you see why a temporarily-lost route is *active*) and starts querying its neighbors.

**EIGRP is complex in implementation and maintenance.** Totally bogus. EIGRP in large networks with low-speed links was somewhat harder to design properly in the good old days before the stub routers were introduced. With stub routers (and numerous fixes to the DUAL algorithm), it's no worse than OSPF (not to mention BGP or IS-IS).

**Like a Link State protocol, EIGRP keeps a topology table of advertised routes**. It's amazing how totally wrong this is. EIGRP has no clue what's beyond the immediate neighbors, while LS protocols know the exact topology of the whole area in which they are.

The only thing an EIGRP router does is to keep track of what the neighbors told it (RIP forgets everything that's not immediately applicable). In that aspect, it's very similar to BGP that also stores everything in the BGP table and then selects the best path from the BGP table. The topology table (stored past information from EIGRP neighbors) gives EIGRP an edge over RIP (but not BGP) -- the topology table might already have an alternate (but currently not used) route to the destination.

**EIGRP is a Distance Vector protocol that acts like a Link State protocol**. Nice try, but still totally wrong. A Link State routing protocol builds the routing table using these steps:

-   Every router describes its local view of the network (links, subnets, neighbors) in a packet (or more of them) called LSA (in OSPF) or LSP (in IS-IS).
-   LSAs are flooded unmodified across the whole area, ensuring every router receives all LSAs generated within the area. Each router stores all received LSAs in its *topology database*.
-   Each router independently analyses its copy of the topology database and runs the SPF algorithm to compute its own best paths to every other router in the area.

EIGRP doesn\'t come even close to using a single one of these steps, so it's hard to understand why exactly it "acts like a Link State protocol".

**EIGRP is an Advanced Distance Vector protocol because of addition of several Link State features such as dynamic neighbor discovery**. This is grasping at straws. A protocol that is smarter than RIP (and can actually figure out who the neighbors are) is still infinitely far away from being a Link State protocol. Dynamic neighbor discovery is not a Link State feature (or we could start claiming that BGP with anonymous neighbors also has LS features). Every decent network-related protocol designed in the last decades has some dynamic neighbor discovery and/or verification of neighbor presence.

What's your take on EIGRP myths? Have I missed any of them? Share your opinions in the comments.
