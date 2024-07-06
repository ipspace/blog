---
date: 2008-07-03 06:50:00+02:00
tags:
- IP routing
title: What Is Anycast?
series_title: Overview
url: /2008/07/anycast.html
series: anycast
series_weight: 1000
anycast_tag: intro
lastmod: 2023-02-01 07:49:00
---
Whenever I start digging into technical details, I learn something new. A few days ago I've stumbled across the term [anycast](http://en.wikipedia.org/wiki/Anycast), which is a very interesting way to solve scalability issues:
<!--more-->
1.  Deploy geographically dispersed servers using the same IP address (obviously they would also need a unique IP address or you wouldn\'t be able to manage them);
2.  Advertise your service as residing on that IP address (for example, use the IP address in NS records for DNS zones you host)
3.  Advertise the IP address (or corresponding IP prefix) into the Internet from multiple locations.

Anycast works best with simple request-response UDP applications (for example, DNS) and has been used for ages to implement [large-scale DNS deployments](/2021/11/dns-anycast.html) (for example, root name servers).

Using anycast for TCP sessions is trickier. It works reasonably well in the global Internet where the anycast endpoints are far enough from each other and true equal-cost multipathing is rare.  [CloudFlare is using anycast globally](https://www.cloudflare.com/learning/cdn/glossary/anycast-network/) and managed to tweak their TCP/IP stack to use [anycast source IP addresses](/2022/12/worth-reading-cloudflare-egress-anycast.html). LinkedIn has fewer points-of-presence and [decided to use regional anycast](https://engineering.linkedin.com/network-performance/tcp-over-ip-anycast-pipe-dream-or-reality).

Using anycast TCP endpoints in data centers is harder and requires [fine-tuned interaction with network-layer multipathing](/2021/05/tcp-anycast-hard.html) as well as a [bag of intricate tricks](/2021/05/tcp-anycast-hard.html#making-local-tcp-anycast-work).

For more details, watch the [Load Balancing and Scale-Out Architectures](https://my.ipspace.net/bin/list?id=DC30#LOAD_BALANCING) part of the [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar and the [Global Accelerator](https://my.ipspace.net/bin/list?id=AWSNET#LB) video in the [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar.

### Revision History

2023-02-01
: Added links to UDP and TCP anycast use cases
