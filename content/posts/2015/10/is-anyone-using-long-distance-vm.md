---
date: 2015-10-26 09:50:00+01:00
dr_tag: avoid
high-availability_tag: dr
series:
- dr
tags:
- vMotion
- virtualization
- high availability
title: Is Anyone Using Long-Distance VM Mobility in Production?
url: /2015/10/is-anyone-using-long-distance-vm.html
---
I had fun times participating in a discussion focused on whether it makes sense to deploy OTV+LISP in a new data center deployment. Someone quickly pointed out the elephant in the room:

> How many LISP VM mobility installs has anyone on this list been involved with or heard of being successfully deployed? How many VM mobility installs in general, where the VMs go at least 1,000 miles? I\'m curious as to what the success rate for that stuff is.

I think we got one semi-qualifying response, so I made it even simpler ;)
<!--more-->
> Let's start with a way simpler target: \"How many VM mobility installs in general... that actually get used"

So far, I haven't seen a single one, apart from the case where a DC was split across two buildings 100 m apart with tons of dark fiber in between.

I see lots of people building stretched VLANs for all sorts of crazy reasons (most common: "Because the VMware consultants told us to do so") and think they [solved the disaster recovery use case](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html).

OTOH, I haven't seen anyone actually shifting workloads across the DCI link (excluding migrations) because performance tends to suck after you [increase latency by orders of magnitude](https://blog.ipspace.net/2015/01/latency-killer-of-spread-out.html).

In summary, a lot of people spend significant amount of money (OTV licenses), time and mental energy to [create a ticking bomb](https://blog.ipspace.net/2011/12/large-scale-l2-dci-true-story.html) (because [broadcast storm](http://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html) or [DCI failure](http://blog.ipspace.net/2011/06/stretched-clusters-almost-as-good-as.html)) that adds zero real-life value.

**Hot tip**: If you can't persuade your peers what a bad idea stretched VLANs are, tell them [Gartner said so](https://blog.ipspace.net/2015/09/blessed-by-gartner-stretched-vlans-make.html) ;)
