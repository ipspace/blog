---
date: 2009-08-26 07:02:00.001000+02:00
ospf_tag: trust
tags:
- IS-IS
- security
- OSPF
title: Do Not EVER Run OSPF or IS-IS With Your Internet Customers
url: /2009/08/do-not-ever-run-ospf-or-is-is-with-your.html
---
Someone started an [interesting discussion on the NANOG mailing list](http://www.merit.edu/mail.archives/nanog/msg20171.html). He inherited a network that extended its internal OSPF to its multihomed customers and wondered whether he should leave the network, change OSPF to IS-IS, or deploy BGP. Here are a few thoughts from [my reply](http://www.merit.edu/mail.archives/nanog/msg20189.html).

{{<note>}}Please remember that we were discussing running global OSPF with the customer routers. Running OSPF in a VRF is a different story, as the customer cannot impact another customer's routing (they can only burn your CPU cycles).{{</note>}}
<!--more-->
Do not **ever** run an SPF routing protocol (OSPF or IS-IS) with your customer. They can insert anything they want into it, be it due to configuration mistakes, malicious intent, or third-party hijacking, and your whole network (or at least the other customers) will be affected.

Just to give you a few examples:

-   They could hijack the host route to your DNS server and spoof every other customer that uses your DNS (I haven't seen this one yet, but it's feasible).
-   They could hijack the host route to your POP3 server and collect the usernames and passwords of your residential users (I've seen this in a production network, but the attack vector was not OSPF but another routing protocol).
-   Company A could hijack the host route to Company B's web server.
-   They could insert a better default route than you do, and at least some of your routers will listen to them (I've seen this done with OSPF).
-   If they ever make a total mess and start flapping their LSAs, your whole network will be affected, and all your routers will burn the CPU cycles running the SPF algorithm.

If you absolutely insist on not using BGP (but then BGP is the only currently available routing protocol designed to handle routing in scenarios where the two parties don't necessarily trust each other), use RIP. It's safer than OSPF; at least you can filter the incoming updates.

{{<note>}}I've also seen a Service Provider running RIP with their customer ... but they were not using any filters when redistributing RIP routes into their IGP.{{</note>}}

Numerous other respondents shared my feelings, and [Steve Bertrand provided the best summary](http://www.merit.edu/mail.archives/nanog/msg20205.html): "If in the same sentence you read 'my network' and 'customer network,' use BGP."
