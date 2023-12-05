---
title: "netlab 1.7.0: Lab Validation, Fabrics, BGP Nerd Knobs"
series_title: "Lab Validation, Fabrics, BGP Nerd Knobs (Release 1.7.0)"
date: 2023-12-07 05:50:00
tags: [ netlab ]
netlab_tag: release
---
It's been a while since the [last netlab release](https://blog.ipspace.net/2023/10/netlab-1-6-4-more-bgp-nerd-knobs.html). Most of that time was spent refactoring stuff that you don't care about, but you might like these features:

- You can run automated [lab validation tests](https://netlab.tools/release/#../topology/validate.md) with the  **[netlab validate](https://netlab.tools/release/#../netlab/validate.md)** command. I will explain how I use that in BGP labs in a few days.
- If you want to build large leaf-and-spine topologies, you'll love the [**fabric** plugin](https://netlab.tools/plugins/fabric/).
- The [**bgp.domain** plugin](https://netlab.tools/plugins/bgp.domain/) allows you to create topologies with multiple sites using the same BGP AS number.
- The [**bgp.policy** plugin](https://netlab.tools/plugins/bgp.policy/) got AS-path prepending.
- [**bgp.originate** plugin](https://netlab.tools/plugins/bgp.originate/) can be used to originate BGP IPv4 and IPv6 prefixes.

As always, we also improved the platform support:
<!--more-->
- The `--show` option of the **[netlab connect](https://netlab.tools/netlab/connect/)** command implements a consistent cross-device way of executing show commands. You might find it handy if you hate guessing whether to use **vtysh** or **sudo vtysh** with Cumulus and FRR containers.
- **vptx** device supports the vJunosEvolved release 23.2R1-S1.8. [Older vJunos Evolved releases no longer work](https://netlab.tools/release/1.7/#release-1-7-0-breaking)
- You can use **bgp.session** plugin to configure BFD, BGP timers, and passive BGP for Junos devices (vMX, vSRX, vPTX)
- **bgp.session** plugin got AS-path manipulation, default route origination, TTL security, passive BGP peers, MD5 passwords, and BGP timers on Cisco NexusOS
- MPLS LDP now works on Nokia SR Linux
- Aruba AOS-CX supports L3VNI (you'll need release 10.13 to make it work)
- Default FRR release is 9.1.0

### Upgrading

To get more details and learn about additional features included in release 1.7.0, [read the release notes](https://netlab.tools/release/1.7/#release-1-7-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
