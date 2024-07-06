---
date: 2019-10-17 08:22:00+02:00
dr_tag: fake
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- high availability
title: Disaster Recovery Faking, Take Two
url: /2019/10/disaster-recovery-faking-take-two.html
---
An anonymous (for reasons that will be obvious pretty soon) commenter left a gem on my [Disaster Recovery Test Faking](/2019/09/disaster-recovery-test-faking-another.html) blog post that is way too valuable to be left hidden and unannotated.

Here's what he did:

> Once I was tasked to do a DR test before handing over the solution to the customer. To simulate the loss of a data center I suggested to physically shutdown all core switches in the active data center.

That's the right first step: simulate the simplest scenario (total DC failure) in a way that is easy to recover (power on the switches). It worked...
<!--more-->
> A word and a blow. Spanning tree converged pretty fast. The stretched VLANs were all functional on the DR site.

... but it also exposed all the shortcomings of [PowerPoint-based designs](/2011/09/long-distance-irf-fabric-works-best-in.html) promoted by \$vendor engineers and copycat consultants:

> But there were split brain scenarios on firewalls all over the place.

Also, [nobody ever thinks about storage when talking about automated disaster recovery](/2013/01/long-distance-vmotion-stretched-ha.html) using stretched VLANs because "*we do synchronous replication so what could possibly go wrong*". Well, as expected:

> Even worse the storage (iSCSI) didn't survive because it couldn't build the quorum and so the storage wasn't accessible on the DR site.

Final result: total failure.

> After some minutes no machines (also virtual load balancers) were reachable. Also vCenter wasn't reachable any more and so they couldn't do anything. After bringing the core switches back online it took them hours to recover from the mess.

Let me recap: someone proposed a disaster recovery architecture (stretched VLANs) that is not only [totally broken from resilience perspective](/2012/05/layer-2-network-is-single-failure.html) and [is a potential ticking bomb](/2019/05/real-life-data-center-meltdown.html), it doesn't even work when needed.

Just in case you think that's an isolated incident: major networking and virtualization vendors are selling the same fairy tale to their customers every day without ever mentioning the drawbacks or caveats.

How do you think the story continued?

> They never fixed the broken architecture (firewall/load balancer cluster and iSCSI storage).
>
> On the second attempt they faked disaster recovery tests like you were describing by carefully moving some machines to the DR site but did not failover firewalls and load balancers.
>
> In the internal review discussion they had to admit that the network failed over as expected and in a reasonable amount of time.

As expected - [cognitive dissonance](https://en.wikipedia.org/wiki/Cognitive_dissonance) kicked in. It was easier to pretend there was no problem and faking the results while spending the minimum amount of work. Who cares that the house-of-cards would collapse the first time it's really needed.

He concluded with:

> Most everyone these days is relying on 100 % network availability. It's a fallacy. Sometimes they have to learn it the hard way.

The only problem is that some people never learn... sometimes because they don't want to, sometimes because they can't grasp the idea of external \"experts\" misleading them, sometimes because they don't understand the basics of reliability theory.

Don't be like that. If you want to discover [how networks really work](https://www.ipspace.net/How_Networks_Really_Work) including [the impact of fallacies of distributed computing](https://my.ipspace.net/bin/list?id=Net101#FALLACIES), [the basics of reliability theory](https://www.ipspace.net/Reliability_Theory:_Networking_through_a_Systems_Analysis_Lens), or [how to build disaster-recovery or active-active data centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) we have you covered.
