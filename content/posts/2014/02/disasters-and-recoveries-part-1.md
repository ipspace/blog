---
date: 2014-02-03 06:53:00+01:00
dr_tag: life
high-availability_tag: dr
series:
- dr
tags:
- data center
- high availability
title: Disasters and Recoveries, Part 1
url: /2014/02/disasters-and-recoveries-part-1/
---
You probably know the three steps to a disaster recovery plan: Disaster. Recovery. Plan. It's amazing how true that joke is, and how unprepared we tend to be for infrequent outages.
<!--more-->
### The Outage

After heavy snows on Thursday we got a hefty dose of sleet on Friday. The trees almost immediately got a wonderful ice coating ... and we lost electricity a few hours afterwards.

![](/2014/02/s320-IceAge.png)

**Lesson#1:** Things that look great might actually do more harm than good. Technologies that [look great in PowerPoint](/2011/09/long-distance-irf-fabric-works-best-in/) might bring down your network.

### The First Steps to Recovery

We live in a small village in Slovenian hills. Heavy snows are not unusual, and we were warned that prolonged power outages aren't exactly impossible, so I implemented all sorts of redundancy measures.

Being in the middle of a winter storm, I was most worried about us staying warm. Time to fire up our ceramic wood oven (a slightly less ancient version of [this thingy](https://sl.wikipedia.org/wiki/Slika:Pocarija_kru%C5%A1na_pe%C4%8D.jpg)). Half an hour later the fire was happily burning.

**Lesson#2:** Simple technologies work best. Find the simplest possible technology that will [meet your recovery time objectives](/2013/01/long-distance-vmotion-stretched-ha/) and stick with it.

**Lesson#3:** Go for easy wins that solve the most pressing problems. Establish connectivity, get the critical services up and running. Take a deep breath, relax, and continue.

However, it takes incredibly long for the warmth to propagate through the layers of bricks and ceramic (hint: 3-4 hours).

**Lesson#4:** Recovery isn't instantaneous. Even if you manage to get a backup data center up and running, it might take hours to recovery all storage volumes, databases, servers ... If you need faster recovery, you need a better plan (and no, live VM migration won't help if you're dealing with a data center failure).

As the oven was getting warm the seams between the ceramic tiles started leaking smoke (a regular annoyance when you use this type of oven after a while).

**Lesson#5:** Recovery procedures that haven't been used or tested for a long time might have a few glitches. You might discover out-of-date configurations and missing firewall/load balancer rules. There's a good reason you should start the diesel generators every few weeks.

### But Wait, It Gets Worse

We got power after \~6 hours, and our house has better insulation than I expected ;), but I was still bound to get a few more hard lessons. Electricity was gone after a few hours (in around 10% of Slovenia), and it took us two weeks to get it back.

### The True Heroes

Every emergency has its true heroes - in this case the servicemen from the power distribution companies that have been working days and nights to restore the power, and the firefighters (most of them volunteers) that removed hundreds of trees blocking the local roads. Thank you, guys - you\'re my heroes!
