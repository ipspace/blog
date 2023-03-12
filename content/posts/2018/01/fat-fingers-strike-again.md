---
cli_tag: fail
date: 2018-01-10 09:42:00+01:00
series:
- cli
series_weight: 1900
tags:
- automation
- Internet
- IP routing
title: Fat Fingers Strike Again…
url: /2018/01/fat-fingers-strike-again.html
---
Level3 had a pretty bad bad-hair-day just a day before [Pete Lumbis talked about Continuous Integration](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3A) on the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course (yes, it was a great lead-in for Pete).

According to [messages circulating on mailing lists](https://puck.nether.net/pipermail/outages-discussion/2017-November/001375.html) it was all caused by a fumbled configuration attempt. My wild guess: someone deleting the wrong route map, causing routes that should have been tagged with **no-export** escape into the wider Internet.
<!--more-->
{{<note>}}Please note I'm not picking on Level3. It [happens to everyone](http://www.bailis.org/papers/partitions-queue2014.pdf), including the [biggest players](https://aws.amazon.com/message/41926/).{{</note>}}

As you probably know by now, there's only one way to minimize the number of fat-finger incidents: deploy tools and implement processes that minimize or reduce time spent typing in a SSH session.

If you have to rely on an operator doing copy-paste into a production box all the ITIL magic and change control and maintenance windows won't help you much... apart from slowing you down and occasionally reducing the impact of the blunders. After all, when was the last time you've seen a rental car agent furiously typing in SQL statements to get you an upgrade?

Also, it might be a good idea to start thinking about the costs of doing exceptions. Either Level3 does everything by hand (hope not) or someone had to do a manual change because of a special customer. Straight from the report I quoted above:

> The issue was isolated to a policy change that was implemented to a single router in error while trying to configure an individual customer BGP.

That customer definitely costed them a lot...

Meanwhile in the [network automation online class](http://www.ipspace.net/Building_Network_Automation_Solutions): some students are [working on building automation solutions](https://www.ipspace.net/NetAutSol/Solutions) that deploy IP routing protocols, MPLS fabric, L2VPN and L3VPN from service definition files, while others are [already deploying new WAN sites using automatically-generated configurations](https://blog.ipspace.net/2017/12/automate-remote-site-hardware-refresh.html).
