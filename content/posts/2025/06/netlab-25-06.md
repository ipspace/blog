---
title: "netlab 25.06: Fixing Nokia SR-OS Configuration Templates"
series_title: "Fixing Nokia SR-OS Configuration Templates (Release 25.06)"
date: 2025-06-16 08:23:00+01:00
tags: [ netlab ]
netlab_tag: release
---
**TL&DR**: [*netlab* release 25.06](https://netlab.tools/release/25.06/) was published last week.

Before discussing the new features, let's walk the elephant out of the room: I changed the release versions to YY.MM scheme, so I will never again have to waste my time on the existential question of which number in the release specification to increase.

Now for the new features:
<!--more-->
* Blackhole/discard [static routes](https://netlab.tools/module/routing/#generic-routing-static) (routes point to *null* interface)
* [Redistribution](https://netlab.tools/module/routing_protocols/#routing-import) of [static routes](https://netlab.tools/module/routing/#generic-routing-static) into OSPF, IS-IS, RIPv2, RIPng, and BGP
* Link aggregation on Junos.

Unfortunately, instead of creating other cool features, I had to spend 90% of my time fixing the ancient ruins of Nokia SR-OS configuration templates. This is how the integration test report for Nokia SR-OS looked on May 25th:

{{<figure src="/2025/06/sros-report-initial.png">}}

And this is the result of testing the configuration templates from release 25.06 after fixing ["a few" bugs](https://netlab.tools/release/25.06/#release-25-06-sros-bug-fixes)[^RD]:

[^RD]: I won't bore you with the details; you can find them in [commit messages](https://github.com/search?q=repo%3Aipspace%2Fnetlab+SR-OS&type=commits) and [pull requests](https://github.com/ipspace/netlab/pulls?q=is%3Apr+is%3Aclosed+SR-OS).

{{<figure src="/2025/06/sros-report-2506.png">}}

While fixing old stuff, I also added a [few features](https://netlab.tools/release/25.06/#release-25-06-sros-features) to the SR-OS configuration templates:

* Static ingress replication for VXLAN
* EVPN transit VNI within VPRN service (previous implementation created a separate VPLS service for the transit VNI)
* Propagation of MPLS/VPN and EVPN routes to CE-routers
* VRF-aware EBGP multihop, IS-IS, OSPFv3
* Inter-VRF route leaking in MPLS/VPN deployments (next step: I have to figure out how to do that on a standalone device)
* Route import into BGP, OSPFv2, OSPFv3, and IS-IS

I must admit that I kind of liked working with SR-OS. Apart from a few conceptual quirks[^CQ], it's pretty fast, quite neat, and easy to work with (once you figure out configuration changes won't be applied until you do a **commit**). If only there were an easy way to get the VM image...

[^CQ]: For example, global routing protocols are configured in _base **Router**_ instance while the user-facing interfaces these protocols are using are defined in Internet Edge Services instance.

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
