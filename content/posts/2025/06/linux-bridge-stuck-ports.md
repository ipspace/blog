---
title: "Weird: Ports on Linux Bridge Are Stuck"
date: 2025-06-05 07:23:00+0200
tags: [ netlab, virtualization ]
netlab_tag: quirks
---
_Just when you thought you got used to the [weirdnesses in the networking implementations](/tag/netlab#quirks), you get a curveball like this one. Life is never dull if you test network devices._

Before releasing _netlab_ release 2.0, I ran the [full suite of integration tests](https://release.netlab.tools/) for all devices for which I have the images. Interestingly, [most VXLAN tests failed for Cumulus Linux 4.x](https://github.com/ipspace/netlab/issues/2254) even though we haven't touched that code for ages.

Next step: trying to figure out what changed. The [configuration changes were minimal](https://github.com/ipspace/netlab/issues/2254#issuecomment-2866376707). Even worse, [the failure was non-deterministic](https://github.com/ipspace/netlab/issues/2254#issuecomment-2866739975). Somehow, we managed to transform a Cumulus Linux 4.x VM into a [Heisenberg switch](https://en.wikipedia.org/wiki/Uncertainty_principle).
<!--more-->
I did the obvious thing: I rolled back the changes. VXLAN started working most of the time[^ET6], but there were still failures.

[^ET6]: It worked every time 80% of the time ;)

After wasting a few more hours trying random things[^SOCH], I calmed down enough to start thinking. Instead of making configuration changes, I restarted the lab until it failed, and then tried to look under the hood... and there it was: the interfaces connected to a Linux bridge that we use in Cumulus VM to build a VLAN were stuck in **learning** state. I don't know whether they would ever move to **forwarding**; I gave up after a few minutes.

[^SOCH]: Admittedly skipping Stack Overflow and ChatGPT

Comparing our configuration of that Linux bridge with the recommended Cumulus configuration, I found a major discrepancy: while the documentation [recommends using](https://github.com/ipspace/netlab/blob/7f468393f2c78be01801acff33a19c9b790dfb90/netsim/ansible/templates/vxlan/cumulus.j2#L18) `mstpctl-portbpdufilter` on the VXLAN interface[^NSV], I [disabled STP on the Linux bridge with VXLAN interfaces](https://github.com/ipspace/netlab/commit/82ef4ad1f2555cea000e7687e812fd1b47951a48) because the recommended solution didn't work with Cumulus containers.

[^NSV]: Running STP over VXLAN shuts down random VXLAN interfaces on Linux bridges, resulting in partial connectivity. The proof is left as an exercise for the reader.

It appears that the version of the Linux bridge used in Cumulus Linux 4.x had an interesting bug: if you disabled STP, the ports remained in the state they were in at the time. That must have been fixed in the meantime; we [use the same hack on FRR](https://github.com/ipspace/netlab/blob/7f468393f2c78be01801acff33a19c9b790dfb90/netsim/ansible/templates/vxlan/frr.j2#L20) and never had any problems.

Anyway, there's still the question of the root cause. Why did VXLAN work for years with the brute-force approach? It turns out that we [changed the order of module configuration](https://github.com/ipspace/netlab/commit/b02bc24b7310471c143484c08e7d6fa551ca62dd) to [accommodate a Junos quirk](https://github.com/ipspace/netlab/issues/2138). Previously, VXLAN would be configured at any random point after VRFs; now we want it configured after BGP (which is configured after generic routing, which is configured after VLANs).

In most cases, VXLAN configuration on Cumulus Linux disabled STP before the interfaces were added to the Linux bridge (part of the VLAN configuration), and therefore, the ports would never transition through STP states. With the change in configuration sequence, the interfaces were attached to the Linux bridge, and STP was disabled a second or two later -- late enough to trigger the bug, but fast enough that it was not triggered consistently.