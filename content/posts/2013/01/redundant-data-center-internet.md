---
date: 2013-01-14 06:56:00+01:00
high-availability_tag: infra
tags:
- firewall
- data center
- workshop
- IP routing
- high availability
title: Redundant Data Center Internet Connectivity – Problem Overview
url: /2013/01/redundant-data-center-internet.html
---
During one of my [ExpertExpress](http://www.ipspace.net/ExpertExpress) [consulting engagements](http://www.ipspace.net/Consulting) I encountered an interesting challenge:

> We have a network with two data centers (connected with a DCI link). How could we ensure the applications in a data center stay reachable even if all local Internet links fail?

On the face of it, the problem seems trivial; after all, you already have the DCI link in place, so what's the big deal \... but we quickly figured out the problem is trickier than it seems.
<!--more-->
In the following short video I'm trying to explain what the problem is, and what a potential solution might look like. You\'ll find [more details here](http://www.ipspace.net/Redundant_Data_Center_Internet_Connectivity).

[![](/2013/01/s400-Redundant+DC+Int+Conn+Snapshot.png)](http://demo.ipspace.net/get/X1%20Redundant%20Data%20Center%20Internet%20Connectivity.mp4)

### Related Blog Posts

Todd Hoff wrote a [great in-depth commentary of this video](http://highscalability.com/blog/2013/1/23/building-redundant-datacenter-networks-is-not-for-sissies-us.html) that you absolutely have to read.

And here are a few other relevant blog posts:

-   [High-level design document](http://www.ipspace.net/Redundant_Data_Center_Internet_Connectivity) in [ipSpace solutions corner](http://www.ipspace.net/Solutions_Corner)
-   [Distributed firewalls -- how badly do you want to fail?](/2011/04/distributed-firewalls-how-badly-do-you.html)
-   [Long-distance vMotion for disaster avoidance? Do the math first!](/2011/09/long-distance-vmotion-for-disaster.html)
-   [Is layer-3 DCI safe?](/2012/10/is-layer-3-dci-safe.html)
-   [Stretched layer-2 subnets -- the server engineer perspective](/2012/03/stretched-layer-2-subnets-server.html)
-   [Layer-2 DCI and the infinite wisdom of ACM Queue](/2012/08/layer-2-dci-and-infinite-wisdom-of.html)

### Related Webinars

-   [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers)
-   [Data Center Interconnects](http://www.ipspace.net/Data_Center_Interconnects)
