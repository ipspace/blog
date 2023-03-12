---
date: 2015-03-25 13:05:00+01:00
dr_tag: fail_fix
high-availability_tag: dr
series:
- dr
tags:
- SDN
- overlay networks
- high availability
title: Availability Zones in Overlay Virtual Networks
url: /2015/03/availability-zones-in-overlay-virtual.html
---
Amazon Web Services was (AFAIK) one of the first products that introduced [*availability zones*](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) -- islands of infrastructure that are isolated enough from each other to stop the propagation of failure or outage across their boundaries.

Not surprisingly, multiple availability zones shouldn't rely on a [central controller](https://blog.ipspace.net/2014/09/controller-cluster-is-single-failure.html) (as Amazon [found out a few years back](http://aws.amazon.com/message/67457/)), and there are only few SDN controller vendors that are flexible enough to meet this requirement. For more details, watch the free [Availability Zones](https://my.ipspace.net/bin/get/OverlayScale/4%20-%20Availability%20Zones.mp4?doccode=OverlayScale) video on my web site (part of [*Scaling Overlay Virtual Networking*](https://www.ipspace.net/Scaling_Overlay_Virtual_Networks) webinar).

{{<jump>}}
[Watch the video](https://my.ipspace.net/bin/get/OverlayScale/4%20-%20Availability%20Zones.mp4?doccode=OverlayScale)
{{</jump>}}
