---
date: 2012-08-03 09:36:00+02:00
eigrp_tag: basic
tags:
- EIGRP
title: 'EIGRP: an MBA-Like Perspective'
url: /2012/08/eigrp-mba-like-perspective.html
---
Ahmed was reading [my EIGRP book](http://www.amazon.com/gp/product/1578701651/ref=as_li_tf_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1578701651&linkCode=as2&tag=cisioshinandt-20) (I know it's hard to get, but fortunately he found a well-marked copy) and wanted to check his understanding of how EIGRP works. The first question was as good a summary as I've ever seen:

> Does it just simply boil down to the fact that a router will choose not to have anything to do with a reported distance higher than its own cost to that route (feasible distance) for the (paranoid) fear that it could be a loop?

Next, he started wondering why a router would behave that way:
<!--more-->
> Is that just a strict protocol design decision that may lead to cases where a good (non-loop) may not be considered as a feasible successor but the design choice had to be made to ensure we avoid loops?

Actually, that was the best EIGRP designers could do with a distance vector routing protocol. The router, lacking the information on other routers\' link costs, has no way of figuring out what next hop the neighbor reporting higher distance is using (contrary to [Loop-Free Alternate feature in OSPF](/2012/01/loop-free-alternate-ospf-meets-eigrp.html) where the router *knows* its neighbor has a third-party next hop because it has full visibility into neighbor's view of the area topology).

However, it was the follow-up e-mail I got from Ahmed that made my day -- he explained EIGRP's operation in business terms:

> Would the EIGRP thought process be the business equivalent decision of never buying a commodity (accepting an RD) for more than you\'re selling it (feasible distance) because you may just be buying back your own product at a markup (loop condition)? But if your cheapest supplier goes away you immediately switch to the next cheapest one (feasible successor) provided you\'re not losing money (feasibility condition) while the customer (packet flow) sees no supply interruption. I imagine you would advertise the higher distance (price change) to your upstream neighbors right?

Yes you would. You want to operate at a fixed markup.

> \...and if supply dries up (route loss) and you don\'t have a feasible backup supplier on the books you abandon your existing (distance) price structure and have to \"query\" for a way to get a new price since you didn\'t have a backup supplier that could have let you continue supplying to the market (routing packets).

Is he good or is he good? He'd make a great teacher.
