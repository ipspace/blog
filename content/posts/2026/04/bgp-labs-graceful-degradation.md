---
title: "BGP Labs: Graceful Degradation for Unsupported Devices"
series_title: "Graceful Degradation for Unsupported Devices"
date: 2026-04-15 07:59:00+02:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
BGP_tag: lab
---
A few weeks ago, I [described the changes](/2026/03/bgp-labs-device-flexibility/) in the [online BGP labs](https://bgplabs.net/) that allow you to use most of the common network operating systems as "external" routers[^XR]. However, while we keep improving it, _netlab_ still can't configure all BGP features on all supported devices (PRs from Nokia and Mikrotik fans would be highly appreciated 😎), which means that it's possible to configure your environment in a way where some of the more complex labs would simply fail to start.

The limited choice of devices for external routers was always well-documented ([example](https://github.com/bgplab/bgplab/blob/fff0ac67f9622d01cccda58e075b0bfd6930fa0a/docs/policy/8-community-attach.md#device-requirements-req)), but if you insisted on using unsupported devices, the lab would fail to start with an error message, and you'd have to tweak the lab topology ([example](https://github.com/bgplab/bgplab/blob/fff0ac67f9622d01cccda58e075b0bfd6930fa0a/docs/basic/2-multihomed.md#device-requirements-req)). Wouldn't it be better to start the lab with a warning?
<!--more-->
### There's Always a Story Behind a Feature

I was facing a similar dilemma in the _netlab_ integration testing: 

* I wanted to use the minimum number of tests. Each test can easily take a half-hour to complete across all tested devices.
* We have to test many features in multiple scenarios. For example, we test BGP default route origination in the global routing table and in a VRF.
* Sometimes, we don't implement the prerequisite feature (example: VRFs) on all devices that support the tested feature (example: BIRD), which would result in a test failure, although the feature itself is properly implemented.

[^XR]: External as in "you don't need to configure them". They are obviously still part of the lab.

VRFs were the major pain. The first solution was thus a [plugin that adjusted the lab topology](https://github.com/ipspace/netlab/blob/dev/netsim/extra/test.vrf_check/plugin.py) based on whether the tested device supports VRFs. A [slightly more refined solution](https://github.com/ipspace/netlab/blob/dev/netsim/extra/test.fixup/plugin.py) would do fixups based on device type ([example](https://github.com/ipspace/netlab/blob/771eeee6b5b3193ced892beb713e0ef1de6eb61b/tests/integration/vxlan/05-vxlan-router-stick.yml#L71)), turning test failures into warnings.

As the number of exceptions grew, I decided to go for a [generic plugin](https://github.com/ipspace/netlab/blob/dev/tests/integration/plugin/adjust_test.py) that adjusts the lab topology and the validation tests based on the available features of the tested device. For example, the BGP aggregation test [removes routing policies](https://github.com/ipspace/netlab/blob/771eeee6b5b3193ced892beb713e0ef1de6eb61b/tests/integration/bgp.policy/60-aggregate.yml#L26) used in *suppress maps* and the related validation tests if the device we're testing supports BGP route aggregation but not routing policies.

### Back to BGP Labs

That plugin (with a [few adjustments](https://github.com/bgplab/bgplab/blob/cfd4b28251afe48ec4843cbe5b528b44ec50455d/plugin/adjust.py#L81)) turned out to be a perfect fit for the BGP labs ([example](https://github.com/bgplab/bgplab/blob/cfd4b28251afe48ec4843cbe5b528b44ec50455d/policy/3-prefix/topology.yml#L39)). Instead of a hard error, the lab starts, but generates a warning and an explanation, hopefully prompting the user to reread the documentation.

{{<figure src="/2026/04/bgp-gd-hard-error.png" caption="Before: Error generated when trying to start a BGP policy lab with Mikrotik external routers">}}

{{<figure src="/2026/04/bgp-gd-warning.png" caption="After: Using an unsupported device results in a warning and a help message">}}

Want to know the details? The source code is online; follow the "example" links in this blog and explore. Want even more details? [Open a discussion](https://github.com/ipspace/netlab/discussions/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).

I hope I got the adjustments right in all lab exercises; if you experience any problems, please report them by opening a [GitHub issue](https://github.com/bgplab/bgplab/issues/new/choose).