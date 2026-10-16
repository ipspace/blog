---
title: "Testing OpenEIGRP with netlab"
date: 2026-10-20 07:21:00+0200
tags: [ EIGRP ]
eigrp_tag: deploy
---
When [Donnie Savage](https://www.linkedin.com/in/diivious/) announced the [open beta](https://www.linkedin.com/posts/diivious_openeigrp-eigrp-routing-share-7513434052499062784-HD7G/?highlightedUpdateUrn=urn%3Ali%3Aactivity%3A7516520255838371840&highlightedUpdateType=SOCIAL_SHARE&origin=SOCIAL_SHARE&utm_source=share&utm_medium=member_desktop&rcm=ACoAAAF0NisBME_cExE6SWQqx9fCT6lHPXgRxA4) of [OpenEIGRP](https://github.com/diivious/eigrp),  I quickly asked him whether it would be possible to get an easy-to-use container with OpenEIGRP integrated with other FRR daemons (and its CLI).

Donnie delivered ;) -- you can download a [ready-to-use container](https://github.com/diivious/eigrp/pkgs/container/openeigrp-frr) and try its EIGRP features. Let's see how you can make that process even simpler with netlab:
<!--more-->
{{<note warning>}}
OpenEIGRP is still in beta, and Donnie created the container repository a few days ago. Things might change (please write a comment if you notice a change), and if they do, I plan to update this blog post.
{{</note>}}

Here's a simple topology (also [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/EIGRP/OpenEIGRP)) to get two OpenEIGRP containers (pretending to be FRRouting containers) up and running:

{{<printout>}}
provider: clab

defaults:
  device: frr
  devices.frr.clab.image: ghcr.io/diivious/openeigrp-frr:0.2.0

nodes:
  r1:
    frr.daemons: [ eigrpd ]
  r2:
    frr.daemons: [ eigrpd ]

links: [ r1-r2 ]
{{</printout>}}

**Notes:**

* We're using containers (line 1)
* FRRouting is the default device (line 4)
* The default FRRouting container has to be changed to the OpenEIGRP container (line 5)
* The lab has two nodes (line 8 and 10) and a single link between them (line 13)
* The OpenEIGRP container crashes unless the EIGRP daemon is enabled, so we have to hack the **frr.daemons** list to include **eigrpd** (line 9 and 11)

{{<note warning>}}
Donnie hadn't published the `:latest` containers (yet) when I was writing this blog post. You might want to look into his [container registry](https://ghcr.io/diivious/openeigrp-frr) and change the container tag in the lab topology to the latest published release.
{{</note>}}

When you start the lab and connect to R1 or R2, you can configure their EIGRP processes:

```bash
$ netlab connect r1
Connecting to container clab-OpenEIGRP-r1, starting bash

Use vtysh to connect to FRR daemon

r1(bash)# vtysh

Hello, this is FRRouting (version 10.8.0-dev-dVs-EIGRP-v0-gUNKNOWN).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

This is a git build of ebfd886-dirty
Associated branch(es):
	local:(no branch)

r1# conf t
r1(config)# router eigrp 1
r1(config-router)# network 10.0.0.0/8
```

Once you have EIGRP configured on both nodes, you can (almost) immediately see the EIGRP routes in the routing tables:

```
r2# show ip route
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF default:
E[1]>* 10.0.0.1/32 [90/61440] via 10.1.0.1, eth1, weight 1, 00:00:03
E[1]   10.0.0.2/32 [90/33554431] is directly connected, lo, weight 1, 00:00:03
L * 10.0.0.2/32 is directly connected, lo, weight 1, 00:04:50
C>* 10.0.0.2/32 is directly connected, lo, weight 1, 00:04:50
E[1]   10.1.0.0/30 [90/33554431] is directly connected, eth1, weight 1, 00:00:03
C>* 10.1.0.0/30 is directly connected, eth1, weight 1, 00:04:50
L>* 10.1.0.2/32 is directly connected, eth1, weight 1, 00:04:50
```

Does OpenEIGRP interoperate with Cisco IOS/XE? Let's change the device types in our lab topology and enable the EIGRP module on the Cisco IOL node (so we don't have to configure it):

{{<printout>}}
provider: clab

defaults:
  devices.frr.clab.image: ghcr.io/diivious/openeigrp-frr:0.2.0

nodes:
  r1:
    frr.daemons: [ eigrpd ]
    device: frr
  r2:
    device: iol
    module: [ eigrp ]

links: [ r1-r2 ]
{{</printout>}}

**Notes:**

* The device type is set on individual nodes (lines 9 and 11)
* We have to enable the EIGRP daemon on the FRRouting node (line 8) and the EIGRP module on the Cisco IOL node (line 12)

When I started the lab with the 0.2.0 OpenEIGRP release, I immediately got an EIGRP adjacency, but no routes were exchanged. My EIGRP is too rusty to figure out what's going on 🤷🏻‍♂️.
