---
title: "Candidate and Active Configuration on IOS XR"
date: 2026-11-04 08:37:00+0100
tags: [ automation ]
---
Traditional network devices used a single (active or running) configuration, with a snapshot of it stored in permanent memory (startup configuration). The active configuration was modified with every configuration command, making it a perfect recipe for disaster in the days of in-band configuration[^RIF].

[^RIF]: There's a reason we have **reload in 5** in Cisco IOS

The situation improved drastically when Juniper [introduced](/2017/12/how-did-netconf-start-on-software-gone/) the *candidate configuration*. You could make changes to a copy of the configuration, and then commit them as a single all-or-nothing transaction. While you could still cut yourself off from the device, at least it was harder to do with a single misordered command.
<!--more-->
Over the years, more and more operating systems got the *candidate configuration* and *transactional (all-or-nothing) commit*, including the initial [lipstick-on-a-pig](https://blog.ipspace.net/2017/03/netconf-transactional-consistency-on/) implementation on Cisco IOS/XE (I hope it got better in the meantime).

And then there's IOS XR. Most other *candidate configuration* implementations create a separate copy (snapshot) of the configuration that you can work on (exactly like a database transaction). When you enter configuration mode on IOS XR, it starts with **an empty configuration**. When you enter configuration commands, they're syntax-checked and added to the empty configuration. You could inspect those commands with **show configuration**, or what would happen after commit with **show configuration merge** or **show configuration replace**. You can also (sort of) see the changes that would be made to the actual configuration with the **show commit changes diff**[^NOO].

[^NOO]: The whole command has no other options (on the IOS XRd I was testing), and yet you have to type the whole thing. I'm positive adding at least three more mandatory keywords would make it even better, but somehow they missed that opportunity.

Anyway, when you're done, you do **commit** (merge) or **commit replace** (hoping you got the changes right), and if you do **commit replace** by accident just after entering the **configure** mode, you've effectively wiped out the active configuration. What could possibly go wrong?
