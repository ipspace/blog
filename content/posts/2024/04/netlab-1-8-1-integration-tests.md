---
title: "netlab 1.8.1: VRF OSPFv3, Integration Tests"
series_title: "VRF OSPFv3, Integration Tests (Release 1.8.1)"
date: 2024-04-08 11:25:00+02:00
tags: [ netlab ]
netlab_tag: release
---
[_netlab_ release 1.8.1](https://netlab.tools/release/1.8/#release-1-8-1) added a interesting few features, including:

- [OSPFv3 in VRFs](https://netlab.tools/module/vrf/#module-vrf-platform-routing-support), implemented on Arista EOS, Cisco IOS, Cisco IOS-XE, FRR, and Junos (vMX, vPTX, vSRX).
- [EBGP sessions over IPv4 unnumbered and IPv6 LLA interfaces](https://netlab.tools/module/bgp/#bgp-platform) on Arista EOS
- Cisco IOS XRd container support  
- [Retry tests until the timeout](https://netlab.tools/topology/validate/#validate-retry) functionality in **[netlab validate](https://netlab.tools/netlab/validate/#netlab-validate)**.

This time, most of the work was done behind the scenes[^BDS].

[^BDS]: And it resulted in weeks of hair-pulling as I struggled with bizarre restrictions and bugs; more about that in another blog post.
<!--more-->
I wrote [numerous integration test scenarios](https://github.com/ipspace/netlab/tree/dev/tests/integration) for initial device configurations, OSPFv2, OSPFv3, BGP, VLANs, VRFs, and VXLAN for a total of over 70 scenarios. These tests were run, and the results were validated on all the boxes/containers I have installed, resulting in [dozens of minor adjustments of configuration templates](https://netlab.tools/release/1.8/#release-1-8-1) and [tons of bug fixes](https://netlab.tools/release/1.8/#bug-fixes-in-release-1-8-1).

You can [view the test results online](https://netlab-cicd.pages.dev/); clicking on various icons will open a log file documenting that particular step in the process. Some of the platforms are almost perfect, others require a bit more work[^TM], but at least now we know what we have to fix ;)

[^TM]: Or I have to increase timeouts even more; some boxes are ridiculously slow.

### Upgrading or Starting from Scratch

* For more details, [read the release notes](https://netlab.tools/release/1.8/#release-1-8-1).
* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
