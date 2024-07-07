---
date: 2015-04-29 15:35:00+02:00
distributed-systems_tag: sdn
series:
- distributed-systems
series_weight: 1900
tags:
- SDN
title: Going Back to the Mainframes?
url: /2015/04/going-back-to-mainframes/
---
25 years ago when I started my networking career, mainframes were all the rage, and we were doing some crazy stuff with small distributed systems that quickly adapted to topology changes, and survived link, port, and node failures. We called them *routers.*

Yes, we were crazy and weird, but our stuff worked. We won and we built the Internet, proving that we can build networks bigger than any mainframe-based solution could ever hope to be.
<!--more-->
A few years later, following the explosions of minicomputers, x86-based servers and server virtualization, everyone started using the same architectural concepts and design paradigms. Look at any large modern application -- you'll find a scale-out architecture of distributed systems designed for failure of any individual component, and powered by orchestration tools (because that's the only way to improve the engineer-to-component ratio).

{{<note info>}}Massimo Re Ferre wrote a great high-level overview of how [native cloud applications should look like](http://it20.info/2014/12/cloud-native-applications-for-dummies/). It's a must-read, as is the [Twelve-Factor App](http://12factor.net/) web site.{{</note>}}

Unfortunately most of the networking world got stuck in a box-at-a-time mentality (with a few notable exceptions), and some people think the solution to that problem is to go back to the mainframe world and deploy centralized controllers with dumb forwarding components. I wonder whether they ever bothered to look at what we've learned in the last 30 years, and where everyone else in the IT is going based on that experience.

{{<note>}}The best comment I heard from an old networking engineer while explaining how OpenFlow works: "*That's SNA. We've seen it fail. We don't have to repeat the experiment.*"{{</note>}}
