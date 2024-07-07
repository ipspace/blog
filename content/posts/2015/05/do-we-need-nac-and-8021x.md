---
date: 2015-05-20 10:48:00+02:00
tags:
- security
- access control
- OpenFlow
title: Do We Need NAC and 802.1x?
url: /2015/05/do-we-need-nac-and-8021x/
---
Another question I got in my Inbox:

> What is your opinion on NAC and 802.1x for wired networks? Is there a better way to solve user access control at layer 2? Or is this a poor man\'s way to avoid network segmentation and internal network firewalls.

Unless you can trust all users (fat chance) or run a network with no access control (unlikely, unless you're a coffee shop), you need to authenticate the users anyway.
<!--more-->
You could use a captive portal (and modern operating systems are pretty good in handling them) or you could use 802.1x. The beauty of 802.1x is that it allows you to authenticate the users or hosts (and use something else but MAC addresses to authenticate the hosts), whereas a captive portal usually requires user intervention.

Yes, 802.1x could be a nightmare to set up and might not be supported on all BYOD platforms, but it's the least intrusive authentication option.

After authenticating the users, you have to decide how you want to handle their traffic. You could allow them to do anything they want ([good luck with that](/2013/04/compromised-security-zone-game-over-or/)) or you might want to be more specific and control their traffic.

You could use a private VLAN (or any other [microsegmentation solution](http://www.ipspace.net/IPv6_Microsegmentation)) and [send all traffic through a firewall](/2015/05/replacing-central-router-with-next/) or another security appliance, which might be the best solution for small sites where almost all traffic exits the site anyway.

In larger environments with lots of intra-site traffic you might decide to do the basic traffic scrubbing at the network edge, in which case you have to deploy per-user ACLs on the network edge. Whether you call that NAC or not is a marketing challenge.

Last question: how do you deploy per-user ACLs on the network edge? RADIUS is one of the popular options (assuming your device supports RADIUS and downloadable per-user ACLs), or you could use [OpenFlow the way HP uses it in their campus solutions](/2015/05/openflow-in-hp-campus-solutions-on/).

## Want to know more?

-   Watch my [Troopers 15 IPv6 Microsegmentation](/2015/04/video-ipv6-microsegmentation/) presentation;
-   Want even more details? You'll find them in the [IPv6 Microsegmentation](http://www.ipspace.net/IPv6_Microsegmentation) webinar.
-   Want to know how HP implemented ACLs with OpenFlow? You'll find all the underlying details in the [OpenFlow Deep Dive](http://www.ipspace.net/OpenFlow_Deep_Dive) webinar.
