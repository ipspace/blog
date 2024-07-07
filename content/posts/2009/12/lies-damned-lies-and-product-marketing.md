---
date: 2009-12-07 06:38:00.004000+01:00
tags:
- switching
- LAN
title: Lies, damned lies and product marketing
url: /2009/12/lies-damned-lies-and-product-marketing/
---
Greg Ferro's "[Layer-3 routing](http://etherealmind.com/network-dictionary-layer-3-routing/)" post successfully kicked my huge sore spot: the numerous ways technical terminology is abused by product marketing gurus.

Twenty years ago, before networking became a multi-billion dollar industry, things were clear, simple and consistent: layer-2 ([data-link layer](http://en.wikipedia.org/wiki/Data_Link_Layer)) frame forwarding was bridging and layer-3 ([network layer](http://en.wikipedia.org/wiki/Network_Layer)) packet forwarding was routing. Everything was crystal clear until some overly smart people tried to turn bridges into something they were not: WAN extension devices. A few large WAN networks were built with bridges ... and failed spectacularly. Router vendors quickly used the opportunity to push the "routing is good, bridging is bad" mantra.
<!--more-->
Fast-forward a few years. Routers were everywhere, "bridge" was a [four-letter word](http://en.wikipedia.org/wiki/Four-letter_word) and another group of smart people was trying to push large-scale LAN bridges. Obviously they couldn't call them "bridges" anymore, so they appropriated a word from the WAN industry and started calling them "switches". Thus "switching" (as in "LAN switching" formerly known as "bridging") was born. The repainting of the old concept didn't help much; they had to lure the customers with [something sweeter](http://www.eastoftheweb.com/short-stories/UBooks/HanGre.shtml). The cost difference between a simple layer-2 forwarding device and a complex layer-3 forwarding device looked promising, so the new mantra was "routers are too expensive, use switches".

Fast-forward to late 1990's. ASICs were getting powerful enough to implement decently fast and cheap basic routing functionality. It was possible to build simple cost-effective high-speed routers ... only "router" was now a four-letter word. What could the product marketing people do? They invented "layer-3 switches", which were really routers, but the new invention sounded so much better.

By then, everyone was thoroughly confused (primarily the customers ... but that was also the goal of the whole exercise, wasn't it) and extra verbs were being thrown into the soup, including "forwarding" which meant something very similar to what "switching" was supposed to mean before it's been abused.

Today, you might see various interpretations of the same terms. I'm close enough to dinosaurs that I'd prefer to see "bridging" and "routing " being used in their original context, but I guess we're far beyond the [point of no return](http://en.wikipedia.org/wiki/Point_of_no_return). Failing that, using "routing" to mean the [control-plane](/2013/08/management-control-and-data-planes-in/) function (collecting, distributing and evaluating the reachability information) and "switching" or "forwarding" to describe the data-plane function is not a bad idea. But please try to stay honest: you always have to specify the OSI (or TCP/IP) layer on which the switching/forwarding activity is taking place.

For more details, please watch *[The Importance of Network Layers](https://my.ipspace.net/bin/list?id=Net101#LAYERS)* and *[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)* parts of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.