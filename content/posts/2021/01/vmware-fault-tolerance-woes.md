---
date: 2021-01-19 07:55:00+00:00
dr_tag: vendor
high-availability_tag: dr
series:
- dr
tags:
- virtualization
- high availability
title: 'Repost: VMware Fault Tolerance Woes'
---
I [always claimed](https://blog.ipspace.net/2011/08/high-availability-fallacies.html) that VMware Fault Tolerance makes no sense. After all, the only thing it does is protect a VM against a server hardware failure... in the world where software crashes are way more common, and fat fingers cause most of the outages. 

But wait, it gets worse, the whole thing is incredibly complex -- you might like this description Minh Ha [left as a comment](https://blog.ipspace.net/2020/12/50-shades-high-availability.html#277) to my [Fifty Shades of High Availability](https://blog.ipspace.net/2020/12/50-shades-high-availability.html) blog post.
<!--more-->
---

In one of the linked posts you mentioned VMware FT Ivan. FT is a high-end feature of VMware's HA portfolios, and it also happens to be a resource hog. Due to the way it needs to log all input and non-deterministic events on the primary VM, send it over to and replay it on the backup VM, things that normally bypass the hypervisor like Rx/Tx now have to go through it for logging purpose and, get delayed until acknowledgement is received, so I/O-bound workloads will incur big performance hit. And multicore VM rubs salt to the wound, because the order of CPUs accessing shared memory needs to be tracked and retained for semantics preservation/correctness purpose. Basically the slowdown is superlinear with the increase in CPU cores. And that's why even though they claim [here](https://kb.vmware.com/s/article/1013428) -- at question 18 -- that FT doesn't cause degradation, looking at their [corresponding white paper](http://www.vmware.com/files/pdf/techpaper/VMware-vSphere6-FT-arch-perf.pdf), the slowdown is indeed superlinear:

And that's just with synthetic workloads. And yes, I/O-bound workloads -- Rx more so than Tx due to the different ways FT deals with each of them -- suffer non-trivial downgrade. Some of their customers also [reported similar issues with I/O](https://communities.vmware.com/t5/ESXi-Discussions/Fault-Tolerance-slow-network-performance/m-p/1770123).

Essentially, looks like HA solutions normally come with performance trade-offs, sometimes considerable ones, and they always cost a hell lot more.

Also, I remember earlier this year, you were blogging about some guy demonstrating a [lossless Vmotion failover](https://blog.ipspace.net/2020/03/the-myth-of-lossless-vmotion.html). Frankly, what does it prove anything? The Vmotion process is inherently lossy, due to the repeated iterations of memory copy and the freezing of the VM, esp. for memory-intensive workload, and that you can successfully execute a lossless migration, just means you're lucky, thanks to probabilities, or have a workload that doesn't stress Vmotion capability to its limit, or both. Or put it in a semi-formal way, just because you manage to achieve result-level correctness, doesn't mean you have process-level correctness :p. Think gambling. That's one classic example of (sometimes) great result, horrible process.

As to end-to-end HA, I agree 100% with you that the right way to do it is via the applications, as it goes along the same line of complexity belonging at the edge and simplicity at the core, smart edge dumb core :)) . DNS exemplifies that application-level-HA paradigm. It's simple and rock solid.

Another great example worth mentioning, is good ol Active Directory. MS did get it right with their DS. AD is a distributed DB application, and a multi-master replication one at that. Given it was designed with this specific model in mind from day one and it came to be more than 20 yrs ago, before this scale-out movement was even a thing, one has to give it to MS on this one.

AD is among the most mission-critical part of just about any company's infrastructure, and it's whole by itself, doesn't need any overpriced and overrated HA device to look after its heartbeat. AD's HA is completely built into its mechanics, with its eventually-consistent DB. Within a site, replication is super quick, and inter-site replication is done using distance-vector paradigm to ensure high scalability. On a side note, MS started Intersite replication in AD with their proprietary algorithm, most likely a link-state one because MS Exchange at that time used LS to route emails between its servers. That one made AD fall apart at 250 sites or so in windows 2000, so MS gave up on it and went with a simpler BGP-like replication model between sites.

in AD, if any server goes down, the client just locates another one using DNS SRV record, first within site and then globally if all servers within a site fail. It's scaled-out, simple, and effective, and it works so well people don't bothers talking about AD these days anymore, and actually haven't done so in a long time.
