---
date: 2015-04-15 09:29:00+02:00
dr_tag: intro
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- WAN
- virtualization
- high availability
title: 'Design Challenge: Multiple Data Centers Connected with Slow Links'
url: /2015/04/design-challenge-multiple-data-centers/
---
One of my readers sent me this question:

> What is best practice to get a copy of the VM image from DC1 to DC2 for DR when you have subrate (155 Mbps in my case) Metro Ethernet services between DC1 and DC2?

The slow link between the data centers effectively rules out any ideas of [live VM migration](/2015/02/before-talking-about-vmotion-across/); to figure out what you should be doing, you have to [focus on business needs](/2013/01/long-distance-vmotion-stretched-ha/).
<!--more-->
In this particular case, you have to figure out what the [Recovery Point Objective](http://en.wikipedia.org/wiki/Recovery_point_objective) (RPO) is, or (to put it bluntly) how fresh the data should be. It's also nice to know what the [Recovery Time Objective](http://en.wikipedia.org/wiki/Recovery_time_objective) (RTO) is, or how long it can take to restore the services.

With well-designed applications that store data in the database and not on local disk, it's good enough to copy VM images every night or so, and have database replication enabled between data centers. Alternatively, you can use database log shipping and recover original data from backups if that's acceptable from RTO standpoint.

There are plenty of backup solutions that allow you to ship VM images to a standby location every night; you can also use [vSphere Replication](http://www.vmware.com/files/pdf/vsphere/VMW-vSPHR-Replication-6-0.pdf) to run continuous data synchronization in the background.

In any case, almost anything is way better (from bandwidth utilization or [goodput](http://en.wikipedia.org/wiki/Goodput) perspective) than dumb block-level disk replication promoted by storage vendors -- database replication or vSphere Replication is aware of the actual content, and can ship the modifications in optimized format, whereas disk replication transfers any change to the disk when it happens (including continuous updates to database indices as records are changed).

{{<note info>}}To learn more about these topics, watch the the [*Designing Active-Active and Disaster Recovery Data Centers*](http://www.ipspace.net/AADesign) webinar.{{</note>}}

The reply I got back from the reader made me sad because it's so typical of the state of the industry:

> As expected, it is just managing expectations. Our problem is probably more Sales and Marketing. Trying to engineer a solution after promises have been made is always going to be a challenge.

I've been [talking about that for years](https://www.youtube.com/watch?v=ClKEkCRvWTQ), but of course I'm always preaching to the choir, and nobody else seems to care.
