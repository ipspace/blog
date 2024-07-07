---
date: 2007-09-05 07:12:00+02:00
tags:
- IP routing
title: 'Get Creative: Static Routing with Catalyst 3750'
url: /2007/09/get-creative-static-routing-with/
---
Here\'s an interesting scenario:

> We have two sites, each using a Catalyst 3750 switch, and routing between them using static routes. There\'s a primary fiber link between them and we\'re using twisted-pair-to-fiber converters due to port limitations on Cat3750. These converters do not report *fiber link down* status correctly (the carrier is still present on twisted pair even if fiber is down), so the primary Ethernet interfaces do not go down if the fiber link breaks and the primary static route is not removed, requiring manual action to switch over to the backup link.

The setup is summarized in this diagram:
<!--more-->
{{<figure src="/2007/09/StaticCatalyst.jpg" caption="Network diagram">}}

My initial reaction was a polite answer explaining that the dynamic routing protocols were invented to handle scenarios like this one, but the poor guy responded that *"[his boss](http://www.dilbert.com/comics/dilbert/the_characters/index.html#boss) does not want to hear about a dynamic routing protocol."* 

I\'ve got a few other ideas in the meantime (at least one of them working perfectly), but let\'s hear it from you first... what would be your solution to this problem?
