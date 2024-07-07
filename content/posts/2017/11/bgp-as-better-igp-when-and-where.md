---
date: 2017-11-29 09:13:00+01:00
dcbgp_tag: newrp
series:
- dcbgp
tags:
- design
- data center
- fabric
- BGP
title: BGP as a Better IGP? When and Where?
url: /2017/11/bgp-as-better-igp-when-and-where/
---
A while ago I helped a large enterprise redesign their data center fabric. They did a wonderful job [optimizing their infrastructure](http://www.ipspace.net/Optimize_Data_Center_Infrastructure), so all they really needed were two switches in each location.

Some vendors couldn't fathom that. One of them proposed to build a "future-proof" (and twice as expensive) leaf-and-spine fabric with two leaves and two spines. On top of that they proposed to use EBGP as the only routing protocol because [draft-lapukhov-bgp-routing-large-dc](https://tools.ietf.org/html/rfc7938) -- a clear case of missing the customer needs.
<!--more-->
Since then I started wondering whether we're overselling the benefits of BGP. It's clearly the right choice if you have a huge fabric, or if you want to run IPv4, IPv6 and EVPN at the same time... but if all you need is IP transport across a half-dozen switches to run VMware NSX on top of that BGP is clearly an overkill.

I tried to summarize my thoughts on whether it makes sense to use BGP in a data center fabric in a [short overview document](http://www.ipspace.net/Data_Center_BGP), starting with [how would you decide whether it makes sense to use BGP as the only routing protocol in your data center fabric](http://www.ipspace.net/Data_Center_BGP/BGP_Fabric_Routing_Protocol).

Keep in mind that this is just an overview document. You'll find more details in the [leaf-and-spine fabric architectures webinar](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures), and master data center design in [building next-generation data center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
