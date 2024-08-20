---
title: "Multivendor EVPN Just Works"
date: 2024-08-27 08:07:00+0200
tags: [ EVPN ]
evpn_tag: intro
---
Shipping [_netlab_ release 1.9.0](/2024/08/netlab-1-9-0-routing-policies/) included running 36 hours of [integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration), including [fifteen VXLAN/EVPN tests](https://github.com/ipspace/netlab/tree/dev/tests/integration/evpn) covering:

* Bridging multiple VLANs
* Asymmetric IRB, symmetric IRB, central routing, and running OSPF within an IRB VRF.
* Layer-3 only VPN, including routing protocols (OSPF and BGP) between PE-router and CE-routers
* All designs evangelized by the vendors: IBGP+OSPF, EBGP-only (including reusing BGP AS number on leaves), EBGP over the interface (unnumbered) BGP sessions, IBGP-over-EBGP, and EBGP-over-EBGP.

All tests included one or two *devices under test* and one or more FRR containers[^NRE], and [the results](https://release.netlab.tools/_html/coverage.evpn) were phenomenal. Apart from a few exceptions (probably caused by mistakes in configuration templates), everything Just Worked™️.
<!--more-->
[^NRE]: because I'm not rich enough to buy enough RAM to run multiple instances of some vendors' bloatware. I also don't have enough time left to wait for all of them to boot.

{{<figure src="/2024/08/evpn-test-results.png">}}

The only caveats[^FNH] we identified in the process[^ICE] were:

* An [ArubaCX quirk](https://github.com/ipspace/netlab/pull/1278#issuecomment-2293365108) (probably an artifact of software-based packet forwarding) that prevented it from working as a VXLAN-to-VXLAN router.
* A weird bug in FRRouting OSPF daemon that resulted in OSPF hello packets with incorrect MTU being sent over the VXLAN segment.

[^FNH]: After fixing BGP next hop handling on EBGP EVPN address family on numerous platforms and [figuring out where to apply the **allowas-in** keyword](/2024/08/bgp-session-af-parameters/).

[^ICE]: Ignoring SR Linux configuration problems I had no chance of fixing, or Dell OS10 boot failures due to the [random inaccessibility of their SSH server](https://blog.ipspace.net/2024/05/too-stupid-to-make-it-work/).

I know vendors have made interoperability claims for years, but we all know what intellectual capital they bring to the interoperability tests. This time, we were running publicly available images (sometimes not even the newest ones[^NXR]) using the configurations we were able to scramble together from vendor documentation.

Admittedly, we did not do any-to-any tests but used FRRouting and Linux VXLAN driver as the baseline, and we couldn't test the quality of hardware programming, but even considering all that, I was amazed at how well it all worked.

Want to repeat the tests? Everything is open-source ;) All you have to do is [install the necessary software](https://netlab.tools/install/) and [jump over the hurdles](https://netlab.tools/labs/libvirt/#vagrant-boxes) created by vendors' image download process.

Want to see the device configurations we used? You can find them in the test logs:

* Open the [test results](https://release.netlab.tools/_html/coverage.evpn)
* Click on the device name
* Click on the checkmark in the **Devices Configured** column in the relevant test results row.

[^NXR]: I'm not going to waste 12GB of RAM for a single switch instance.