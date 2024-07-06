---
date: 2015-09-08 09:25:00+02:00
dr_tag: other
series:
- dr
tags:
- vMotion
- WAN
title: 'Blessed by Gartner: Stretched VLANs Make Little Sense'
url: /2015/09/blessed-by-gartner-stretched-vlans-make.html
---
One of my readers recently pointed me to a [blog post written by Andrew Lerner from Gartner](http://blogs.gartner.com/andrew-lerner/2015/04/23/stretchdontbreak/) describing the drawbacks of stretched VLANs.

**TL&DR**: He's saying more-or-less the same things I've been preaching for years. Now I can put *Blessed by Gartner* logo on my blog posts ;), and you can use the report to sway your CIO.
<!--more-->
Andrew starts by listing two misconceptions...

-   That we need stretched VLANs for VM migration ([check](/2013/01/long-distance-vmotion-stretched-ha.html));
-   That we need stretched VLANs for active-active data centers ([check](/2012/01/ip-renumbering-in-disaster-avoidance.html)).

... and lists four things to consider:

-   WAN latency in LAN environment ([check](/2015/01/latency-killer-of-spread-out.html));
-   L4-7 service architecture and resulting traffic trombones ([check](/2010/09/long-distance-vmotion-and-traffic.html));
-   Resiliency and split-brain ([check](/2011/06/stretched-clusters-almost-as-good-as.html));
-   Traffic symmetry ([check](/2014/10/vxlan-and-otv-saga-continues.html));

Finally, he concludes that "*While these approaches may appear as a simple fix, they often increase complexity, reduce performance and availability, and increase the overall cost of your network."* [Yep](/2013/09/sooner-or-later-someone-will-pay-for.html).

### Why Am I Writing about This?

While it's nice to see someone else coming to the same conclusions (particularly against strong headwind of vendor marketing), what matters most is that "*Gartner Said So*".

I've heard sad stories from dozens of engineers telling me how they tried (and failed) to use my arguments to persuade their bosses that we shouldn't [overcomplicate the network](/2013/04/this-is-what-makes-networking-so-complex.html) to solve other people's problems -- now they can point to a Gartner report saying exactly the same thing.

Unfortunately, for some of those engineers the report came years too late -- at least a few (that I know of) already got badly burned by a meltdown spreading across multiple data centers.
