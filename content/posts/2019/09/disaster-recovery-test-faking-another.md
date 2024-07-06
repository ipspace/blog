---
date: 2019-09-12 09:37:00+02:00
dr_tag: fake
high-availability_tag: dr
series:
- dr
tags:
- design
- bridging
- data center
- high availability
title: 'Disaster Recovery Test Faking: Another Use Case for Stretched VLANs'
url: /2019/09/disaster-recovery-test-faking-another.html
---
The March 2019 Packet Pushers Virtual Design Clinic had to deal with an interesting question:

> Our server team is nervous about full-scale DR testing. So they have asked us to stretch L2 between sites. Is this a good idea?

The design clinic participants were a bit more diplomatic ([watch the video](https://packetpushers.net/should-we-stretch-l2-between-our-primary-and-dr-sites-video/)) than my TL&DR answer which would be: \*\*\*\* NO!

Let's step back and try to understand what's really going on:
<!--more-->
In the ideal world, **you'd just shut down a data center and see what happens**. Companies that realized you cannot fake it forever and pretend to solve application availability with infrastructure tricks have [no qualms doing exactly that](https://queue.acm.org/detail.cfm?id=2371297). They know [everything eventually fails](/2012/10/if-something-can-fail-it-will.html) and focus on making their services as failure-resilient as possible. Once you embrace that mindset, killing parts of your infrastructure to see what happens becomes business-as-usual.

**Meanwhile on Planet Enterprise**: operations teams have to deal with applications that were never [tested beyond loopback interface](https://my.ipspace.net/bin/list?id=Net101#FALLACIES), or [single-instance applications](/2011/08/high-availability-fallacies.html) tested with a database residing in the same LAN segment, and try to increase the availability of these impending disasters by introducing infrastructure tricks.

At the same time, management and auditors require disaster recovery functionality... and some server teams, knowing that they would never be allowed to do the right thing, try to fake disaster recovery tests with a charade that would make Potemkin proud:

-   Move a few running VMs to another site;
-   Ignore all dependencies of the application stack (connectivity to common services, prerequisite network- and security services)
-   Perform the test during a maintenance window
-   Leave the VMs running at the other site for a few minutes, carefully bring them back and declare success.

Mission accomplished. See you next year!

Have they proven that the disaster recovery procedure works? Absolutely not, their carefully-planned choreography has nothing to do with what they'd have to face when the primary data center dies. In the meantime, they need stretched VLANs to make the fake test work, turning both data centers into a ticking bomb that will eventually explode (or as Terry Slattery pointed out in the Design Clinic discussion "*do you want to have [one failure domain or two](/2012/05/layer-2-network-is-single-failure.html)?*").

**Summary**: Disaster recovery is a tough challenge. Proper disaster recovery testing is hard, and as long as you're trying to fake it with careful VM moves, you're bound to have the well-known three-step process to disaster recovery planning:

-   Wait for disaster to happen;
-   Improvise to recover;
-   Plan for the next disaster.

Needless to say, the next time you'll experience a disaster your *post factum* disaster recovery plan will be useless because IT infrastructure and application stacks tend to change over time.

#### What Others Have to Say on the Topic

I asked Daniel Dib for his opinion on the topic. Here's what he sent me:

> This is the first time I've heard people stretching L2 to their DR site though. The entire purpose of the DR site is to not have any dependencies to the main DCs, which is why you put them in different geographical areas etc.
>
> I doubt many organisations have a proper DR plan including RPO, RTO and testing instructions. As you both know, distributed data is always challenging, especially when you try to solve the problem in the network layer.
>
> The ironic thing is that people don't understand L2 is bad until things explode. It could take some time, some get lucky and don't experience it, but that doesn't mean you had a good design.

### More Information

The webinars covering the [sane and less-sane ways of building active-active and disaster recovery data centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) and [all recent variants of data center interconnects](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) are available with [standard ipSpace.net subscription](https://www.ipspace.net/Subscription).
