---
title: "netlab MPLS Support"
series_title: "MPLS Support (Release 1.2.0)"
date: 2022-04-04 06:52:00
tags: [ MPLS, MPLS VPN ]
series: netlab
netlab_tag: release
---
*netlab* release 1.2.0 adds full-blown MPLS and MPLS/VPN support:

-  [VRF definitions and layer-3 VRFs](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html)
-  [VRF-aware OSPF, IS-IS and BGP](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html#interaction-with-routing-protocols)
-  [Traditional MPLS with LDP](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#label-distribution-protocol-ldp) (SR-MPLS was already available)
-  [BGP Labeled Unicast](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#bgp-labeled-unicast-bgp-lu)
-  MPLS/VPN: [VPNv4 and VPNv6 address family](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#mpls-l3vpn-supported-platforms) support

It's never been easier to build full-blown MPLS/VPN labs ;)... if you're OK with [using Cisco IOS or Arista EOS](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#platform-support). Please feel free to [submit a PR](https://netsim-tools.readthedocs.io/en/latest/dev/guidelines.html) to add support for other platforms.

You might want to start with the [VRF tutorial](https://netsim-tools.readthedocs.io/en/latest/example/vrf-tutorial.html) to see how simple it is to define VRFs, and [follow the installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html) to set up your lab -- if you're semi-fluent in Linux (and don't care about [data plane quirks](https://blog.ipspace.net/2022/03/dataplane-quirks-virtual-devices.html)), the easiest option would be to run Arista cEOS.