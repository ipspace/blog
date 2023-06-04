---
title: "Are LACP Fast Timers Any Good?"
date: 2023-06-08 06:19:00
tags: [ switching ]
---
Got this question from a networking engineer attending the [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course:

> Has anyone an advice on LACP fast rate? When and why should you use it instead of normal LACP?

Apart from forming link aggregation groups, you can use LACP to detect link- and node failures ([more details](https://blog.ipspace.net/2023/05/failure-detection-server-dual-homing.html)). However:
<!--more-->
* While you can use [LACP (or UDLD)](https://blog.ipspace.net/2012/09/do-we-need-lacp-and-udld.html) to detect bizarre link failures unidirectional links, [Gigabit Ethernet Link Fault Signaling](https://blog.ipspace.net/2020/11/detecting-network-failure.html) probably does a decent job detecting that.
* Gigabit Ethernet link fault signaling will not detect Byzantine failures, including ASIC wedgies or control-plane lockups. You need a control-plane protocol running between the CPUs of adjacent nodes for that.

BFD would be an ideal candidate for such a control-plane protocol, but it cannot be used when someone insists on building layer-2-only fabrics, or when the hosts attached to the fabric do not support BFD[^VMW]. LACP fast timers might be the only option in that case, but sometimes they come with a bunch of caveats:

[^VMW]: Hi there, ESXi, we're talking about you (again)

> I still doubt if we really need LACP fast rate on 1Gbit UTP links. In my opinion, it's overkill and on our N9K switches, using LACP fast-rate makes ISSU upgrades impossible.

Let's get the snarky elephant out of the room first: now we know how _in-service_ the software upgrades on Nexus switches really are -- they cannot cope with a protocol that has 3-second timeouts.

As always, life is full of tradeoffs. In this case, you have to decide how fast you want to detect non-trivial errors that are not detected by the physical layer (example: MLAG cluster partitioning, control-plane bugs). That obviously depends on how critical your workload is and how often the errors happen, but most environments can probably defer to manual recovery for [once-in-a-blue-moon](https://blog.ipspace.net/2019/06/know-thy-environment-before-redesigning.html) events[^ATC].

Also: It's easy to claim your application is mission critical as long as you can [delegate the hard work to the infrastructure team](https://blog.ipspace.net/2011/08/high-availability-fallacies.html). It's amazing how few things turn out to be [critical enough](https://blog.ipspace.net/2016/04/high-availability-planning-identify.html) to be deployed in two regions after the management succumbs to the siren song of public clouds.

[^ATC]: Air traffic control, nuclear power plants and high-frequency trading are definitely not in this category.


