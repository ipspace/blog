---
date: 2020-06-18 07:01:00+00:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- data center
- design
- high availability
title: Bridging Loops in Disaster Recovery Designs
---
One of the readers commenting the ideas in my *[Disaster Recovery and Failure Domains](/2019/12/disaster-recover-and-failure-domains.html)* blog post effectively said "*In an active/passive DR scenario, having L3 DCI separation doesn't protect you from STP loop/flood in your active DC, so why do you care?*"

He's absolutely right - if you have a cold disaster recovery site, it doesn't matter if it's bombarded by a gazillion flooded packets per second... but how often do you have a cold recovery site?
<!--more-->
Most organizations big enough to have more than one data center site are not willing to treat the second site as a pure insurance policy. Sometimes they run development or test workloads in the second site, sometimes they split the workloads into two groups and run them primarily in one of the sites, using the second site as DR site *for that particular workload*.

Do I have to mention how safe it is to have development environment *bridged* into production site? I know someone who tried to configure link bonding on Windows server and ended up bridging the two uplinks (and bringing down the whole data center). Or how a bridging loop in one data center kills not only everything running there but also all the workload in the healthy site? Unfortunately I know a customer who tested this concept in real life with expected results...

The situation is even worse when someone gets the wonderful idea of stretching the same VLANs across more than two sites (no surprise: some data center vendors are very keen to tell you how to do that with their gear)... now a bridging loop anywhere in your environment brings down multiple sites.

Long story short: as someone once said "*friends don't let friends stretch layer-2 across data centers.*"
