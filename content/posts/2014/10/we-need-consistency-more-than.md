---
date: 2014-10-07 07:25:00+02:00
distributed-systems_tag: sdn
series:
- distributed-systems
series_weight: 1100
tags:
- SDN
title: We Need Consistency more than Controllers
url: /2014/10/we-need-consistency-more-than.html
---
I was listening to the [I2RS Packet Pushers podcast](http://packetpushers.net/show-181-intro-to-i2rs-with-joel-halpern-russ-white/) a while ago and was more than glad that when Greg Ferro yet again mentioned the complexity of OSPF, someone simply pointed out that controllers would not reduce the complexity; if anything they would increase it.
<!--more-->
While the controllers might give you the appearance that things are simple (particularly when you're looking at a glitzy GUI that looks amazingly good on PowerPoint slides), you're effectively trading the explicit complexity for implicit complexity that you're not aware of that will eventually haunt you (more so when you start dealing with [leaky abstractions](http://en.wikipedia.org/wiki/Leaky_abstraction) -- see also [The Law of Leaky Abstractions](http://www.joelonsoftware.com/articles/LeakyAbstractions.html)).

How about doing a proper network design, standardizing configurations that are deployed in consistent manner across all devices, and then you know (if you need to know) what's going on -- the moment you deploy an SDN controller (particularly one with centralized control plane), you won't know at all what's going on behind the scenes... and I have yet to see a commercial OpenFlow controller documentation that describes in sufficient details what happens between the controlled network devices and what flows are installed in each device.

### Coming Back to Real Life

Wondering how real engineers solve real-life problems with network automation and SDN? Listen to the [Software Gone Wild podcast](http://www.ipspace.net/Podcast/Software_Gone_Wild) and check out [SDN resources on ipSpace.net](http://ipSpace.net/SDN).
