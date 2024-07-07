---
title: "Duty Calls: Technologies that Didn't: CLNS"
date: 2020-09-27 07:03:00
tags: [ CLNP ]
---
Russ White [published an interesting story](https://rule11.tech/tech-clns/) explaining why we're using IP and not CLNS to build today's Internet.

Let's start with a few minor details he missed that I [feel obliged to point out](https://xkcd.com/386/) (apologies to Russ for being too pedantic, but you know me...):
<!--more-->
* CONP is not exactly X.25 as it used OSI (network layer) addresses instead of X.121 addresses. You could also run it over LAN media.
* CLNS host address was often derived from system MAC address, but you could easily configure it to anything you wanted. IPv6 SLAAC is probably a direct derivation of that idea.
* You could say that CLNS hosts participated in routing, but they did NOT participate in the IS-IS routing protocol.
* CLNS hosts were continuously sending End System Hellos (ESH), which would be equivalent to gratuitous ARPs or IPv6 DAD messages. For more details, watch the [addressing part](https://my.ipspace.net/bin/list?id=Net101#ADDR) of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.
* CLNS routers were continuously sending Intermediate System Hellos, and that's how end hosts found routers. IPv6 copied that concept almost verbatim with Router Advertisement messages.
* The biggest problem of CLNP addresses was the variable address length, which was considered to be a nightmare by anyone with hands-on experience of building network devices.

However, while Russ was trying to remain diplomatic, the real reason CLNS/CLNP failed (in my cynical blindsided opinion) was the protocol development process. TCP/IP folks focused on getting something done with the resources at hand; the OSI crowd preferred having academic discussions while attending standardization bodies meetings at exotic locations. 

Religious wars between the two camps didn't help either, and the bitter resentment they created in the TCP/IP camp (the rebel alliance of the day) sank the proposal to use a sane version of CLNP as the next-generation IP protocol.

Nonetheless, we're still using ideas first introduced in CLNP. I already mentioned host registration (DAD) and router advertisements; we also reinvented routing on host addresses, and often use unnumbered physical interfaces in combination with a loopback address. For more details, read my [CLNP-related blog posts](/tag/clnp/).
