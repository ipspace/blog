---
date: 2012-07-17 07:06:00+02:00
dr_tag: avoid
high-availability_tag: dr
series:
- dr
tags:
- data center
- vMotion
- virtualization
- high availability
title: Long-Distance Workload Mobility in Perspective
url: /2012/07/long-distance-workload-mobility-in/
---
Sometime in 2012, Chuck Hollis [described how some of EMC customers use long-distance workload mobility](https://web.archive.org/web/20141004114946/http://chucksblog.emc.com/chucks_blog/2012/07/workload-mobility-is-more-real-than-you-might-think.html). Not surprisingly, he focused on the VPLEX Metro part of the solution and didn't even mention the earth-flattening requirements this idea imposes on the network. I guess you already know [my views on that topic](/2011/11/busting-layer-2-data-center/), but regardless of my personal opinions, he got me curious.
<!--more-->
Here are a few interesting facts I gathered from his blog post:

> We were able to move a running virtual machine in about 15-20 seconds.

Sounds about right. [Data center interconnect link is the major bottleneck in the whole story](/2011/09/long-distance-vmotion-for-disaster/) and based on the numbers it appears they have a 10GE link or really small virtual machines.

> Four engineers moved 30 to 40 virtual machines the first weekend \...

Please read this sentence again. And again. And again. Now please tell me why I should be excited. At 20:1 virtualization ratio, that's two full vSphere servers. Over a weekend.

Also, since they worked on weekends, I don't understand the need for live VM mobility. They could have shut down the VMs, move them over, and start them in the other data center, maybe even combining that with the [regular monthly patching](/2011/08/high-availability-fallacies/).

> \... and then gradually moved over 250 systems during the next three weeks.

Here the [press release](http://www.emc.com/about/news/press/2012/20120709-01.htm) is getting imprecise. Is it 250 application stacks, 250 servers or 250 virtual machines? Assuming they moved 250 virtual machines, that's less than 15 physical servers, or two UCS chassis (= half a rack).

Anyhow, I hope they cleaned the network configuration afterwards -- having two data centers in a [single failure domain](/2012/05/layer-2-network-is-single-failure/) is usually a bad idea.

Finally, one must admire EMC's marketing. They managed to produce a revolutionary headline out of the above-mentioned facts: "*EMC VPLEX Enables Major Law Firm to Migrate 250 Live Systems and Data in 15 to 20 Seconds with Zero Downtime*" Congratulations, you just won the exaggeration-of-the-month award.
