---
title: "Worth Reading: Protocol Options Rusted Shut"
date: 2020-11-12 07:15:00
tags: [ Internet ]
---
A long while ago I found a great article [explaining TLS 1.3 and its migration woes](https://blog.cloudflare.com/why-tls-1-3-isnt-in-browsers-yet/) on CloudFlare blog. While I would strongly recommend you read it just to get familiar with TLS 1.3, the real fun starts when the author discusses migration problems, kludges you have to use trying to fix them, less-than-compliant implementations breaking those kludges, and options that were supposed to be dynamic, but turn out to be static (rusted shut) due to middleboxes that implemented protocols as-seen-in-the-wild not as-described-in-RFCs.

Change a few TLAs and you could be reading about TCP, IP stack, IPv6, BGP… I addressed those aspects in the [ossification and centralization](https://my.ipspace.net/bin/get/InetProbs/6%20-%20Ossification%20and%20Centralization.mp4?doccode=InetProbs) part of [Upcoming Internet Challenges webinar](https://www.ipspace.net/Upcoming_Internet_Challenges).
