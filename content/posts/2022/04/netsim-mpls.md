---
date: 2022-04-04 06:52:00+00:00
netlab_tag: archive
series_title: MPLS Support (Release 1.2.0)
tags:
- MPLS
- MPLS VPN
- netlab
title: netlab MPLS Support
---
*netlab* release 1.2.0 adds full-blown MPLS and MPLS/VPN support:

-  [VRF definitions and layer-3 VRFs](https://netlab.tools/module/vrf/)
-  [VRF-aware OSPF, IS-IS and BGP](https://netlab.tools/module/vrf/#interaction-with-routing-protocols)
-  [Traditional MPLS with LDP](https://netlab.tools/module/mpls/#label-distribution-protocol-ldp) (SR-MPLS was already available)
-  [BGP Labeled Unicast](https://netlab.tools/module/mpls/#bgp-labeled-unicast-bgp-lu)
-  MPLS/VPN: [VPNv4 and VPNv6 address family](https://netlab.tools/module/mpls/#mpls-l3vpn-supported-platforms) support

It's never been easier to build full-blown MPLS/VPN labs ;)... if you're OK with [using Cisco IOS or Arista EOS](https://netlab.tools/module/mpls/#platform-support). Please feel free to [submit a PR](https://netlab.tools/dev/guidelines/) to add support for other platforms.

You might want to start with the [VRF tutorial](https://netlab.tools/example/vrf-tutorial/) to see how simple it is to define VRFs, and [follow the installation guide](https://netlab.tools/install/) to set up your lab -- if you're semi-fluent in Linux (and don't care about [data plane quirks](/2022/03/dataplane-quirks-virtual-devices.html)), the easiest option would be to run Arista cEOS.