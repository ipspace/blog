---
date: 2013-09-05 07:45:00+02:00
dr_tag: vendor
high-availability_tag: dr
series:
- dr
tags:
- bridging
- data center
- workshop
- WAN
- high availability
title: Sooner or Later, Someone Will Pay for the Complexity of the Kludges You Use
url: /2013/09/sooner-or-later-someone-will-pay-for/
---
I loved listening to [OTV/FabricPath/LISP](http://packetpushers.net/show-155-integrating-otv-fabricpath-lisp-sponsored/) Packet Pushers podcast. Ron Fuller and Russ White did a great job explaining the role of OTV, FabricPath and LISP in a stretched (inter-DC) subnet deployment scenario and how the three pieces fit together ... but I couldn\'t stop wondering whether there is a better method to solve the underlying business need than throwing three new pretty complex technologies and associated equipment (or VDC contexts or line cards) into the mix.
<!--more-->
You probably already know the answer. There is a better option - [use applications that use DNS](/2012/01/ip-renumbering-in-disaster-avoidance/) and can survive external IP address change when they move from one DC to another. That might sound like an academic argument considering the current state of [craplications](/2011/02/what-exactly-makes-something-mission/) in many enterprise environments, but do step back from the pressing networking problems and take a wider look from the business perspective.

Imagine two competitors both requiring multiple data centers for business continuity: business A, where the application developers do their own thing without considering the impact of their behavior on the IT infrastructure, and business B, where the applications are written so that they interoperate with the network (BTW, all you have to do in Windows environment is to [deploy your services on recent Windows cluster software](/2011/06/multisite-clusters-done-right-by-none/) and you get DNS integration for free).

In the long run, business A will indubitably have higher IT costs - they will inevitable get locked into a single-vendor solution, because no two vendors support the same set of (somewhat) standard protocols and proprietary extensions you need. They will also need high-end gear (LISP or OTV tends to run on reassuringly expensive boxes) and pay dearly for the hardware and the licenses.

At the same time, business B will be able to build simple layer-3 networks using components from almost any vendor ... because all they need to have a running network is the same minimal set of well-tested protocols that we\'re using in the global Internet.

I totally understand that networking vendors prefer to deal with business A. I also understand that some network architects and consultants prefer business A (they have just found a never-ending bonanza of ongoing challenges), but ask yourself: which approach makes more sense from the business perspective? Which one will result in lower IT costs and higher business agility (had to throw in the word adored by marketing departments)?

Think about this when considering the long-term networking strategy of your company ... and good luck!
