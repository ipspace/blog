---
date: 2008-04-10 08:50:00.002000+02:00
tags:
- NTP
- training
title: Technology Is Supposed to Be Simple, Right?
url: /2008/04/technology-is-supposed-to-be-simple/
---
In his comment to the one of my NTP articles, Joe said:

> This is part of the problem with NTP. It\'s way more complicated then it needs to be. You shouldn\'t have to understand so much of it to use it on your routers. Take a look at openntpd. It\'s free and runs on bsd or linux.

I have to disagree with him on several counts:
<!--more-->
-   NTP is supposed to solve a pretty hard problem of synchronizing multiple independent time sources over communication paths with unpredictable delay and jitter. Considering the limitations it\'s faced with, it does an amazingly good job.
-   NTP configuration on IOS is no more complex than the [openntpd configuration](http://www.openbsd.org/cgi-bin/man.cgi?query=ntpd.conf) if the only thing you want is to do is to configure an upstream NTP server. The only commands you need are **ntp server** and **ntp master**.

However, the most important point, in my opinion, is the difference between \"aiming for a short recipe\" and \"understanding the technology\". If the only task you ever need to perform is to configure upstream NTP servers, don\'t even bother to read the IOS documentation or my article, you don\'t need more than a single configuration command ... but then, when things really break, you\'ll be in trouble.

Likewise, the only thing some people want to know about OSPF are the following two commands:

``` {.code}
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0
```

There are others, however, that might need a slightly more in-depth understanding of OSPF principles, operations, design, configuration and troubleshooting... and if you ignore those fundamentals you'll have fun time when things go south.