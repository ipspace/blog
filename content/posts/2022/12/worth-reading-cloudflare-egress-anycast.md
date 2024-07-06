---
anycast_tag: reading
date: 2022-12-03 10:36:00+00:00
series:
- anycast
series_title: Egress Anycast in Cloudflare Network
tags:
- worth reading
title: 'Worth Reading: Egress Anycast in Cloudflare Network'
---
Cloudflare has been using [ingress anycast](/2021/11/anycast-principles.html) (advertising the same set of prefixes from all data centers) for ages. Now they did a giant leap forward and implemented another "_this thing can never work_" technology: egress anycast. Servers from multiple data centers use source addresses from the prefix that's advertised by all data centers.

Not only that, in the long-established tradition they [described their implementation](https://blog.cloudflare.com/cloudflare-servers-dont-own-ips-anymore/) in enough details that someone determined enough could go and implement it (as opposed to the typical _[look how awesome our secret sauce is](/2020/11/worth-reading-ai-replication-self-promotion.html)_ approach from Google).
