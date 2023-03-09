---
date: 2020-09-10 08:25:00+00:00
dr_tag: vendor
high-availability_tag: dr
series:
- dr
tags:
- virtualization
- data center
- vMotion
- high availability
title: 'Disaster Recovery: a Vendor Marketing Tale'
---
Several engineers formerly working for a large virtualization vendor were pretty upset with me when I claimed that the [virtualization consultants promote](https://blog.ipspace.net/2019/10/disaster-recovery-faking-take-two.html) "_disaster recovery using stretched VLANs_" designs instead of alternatives that would implement proper separation of failure domains.

Guess what... it's even worse than I thought.

Here's a sequence of comments I received after reposting one of my "_disaster recovery doesn't need stretched VLANs_" blog posts on LinkedIn sometime in late 2019:
<!--more-->
> It's just simpler to stretch layer 2 and failover edge routing for most customers I work with. There are different ways to skin a cat, but stretching layer 2 is a great way to solve DR.

Stretching layer-2 is also a great way to [bring down two data centers](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html), and I've seen more people getting that result than a working disaster recovery solution (because in many cases [the solution proposed by the consultants doesn't work anyway](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html)).

> You don't NEED stretched layer 2, but it is the right solution for some. Particularly in the sector where I work. Customers want DR, but don't have the processes/operators to do anything more involved.

OK, I understand that some customers want [tick-in-the-audit fake](https://blog.ipspace.net/2019/09/disaster-recovery-test-faking-another.html) that's best implemented using stretched VLANs, but that was not the case here...

> They generally are using SRM or some other sort of VM replication to re-instantiate then following a runbook process to bring other systems back online, which includes migration of edge. But we're talking about orgs who are small enough to accept RTO of 24-48 hours. Recovery time is a little more flexible when you're not losing money each moment you're down!

Now read the above paragraph twice, brew a coffee, and allow it to sink in.

* They are using VMware Site Recovery Manager (a decent recovery orchestration tool) that has the capability to add external hooks. It would be trivial to enable networking in the recovery site as the first step of the SRM recovery process (see [this blog post](https://blog.ipspace.net/2019/12/you-dont-need-ip-renumbering-for.html) for a few ideas);
* Recovery Time Objective (RTO) is 24 - 48 hours, and yet they'd risk [having a ticking bomb](https://blog.ipspace.net/2019/05/real-life-data-center-meltdown.html) instead of a stable network just so the server/virtualization team wouldn't have to work together with the networking team during the recovery process?

I'm positive the engineer writing those comments had the best intentions and did his best to help his customers. It's just that he based his design on white papers from a major virtualization and a major networking vendor... both of them having a vested interest in peddling more-and-more complex solutions instead of robust time-proven designs (that could be implemented with boxes from any networking vendor).

Long story short: If you base your design on vendor whitepaper, you get the results you deserve. Step back, [figure out what you really need](https://blog.ipspace.net/2019/12/figure-out-what-problem-youre-trying-to.html), and what's the simplest way (across the whole application stack) to implement it instead of [pushing the problems down the stack](https://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html).
