---
title: "netlab 26.05: BGP-free SRv6 Core, Junos Features"
series_title: "BGP-free SRv6 Core, Junos Features (Release 26.04)"
date: 2026-05-19 08:02:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.05 is out. Here are the highlights:

- Support for [global BGP routes with SRv6 next hops](https://netlab.tools/module/srv6/#module-srv6-services) (inspired by proof-of-concept by [@jvbemmel](https://github.com/jbemmel)) on FRR and IOS XR
- Junos OSPF/IS-IS [route redistribution](https://netlab.tools/module/routing_protocols/#routing-import), VRF [IS-IS instances](https://netlab.tools/module/isis/#isis-platform), and OSPF [interface parameters](https://netlab.tools/module/ospf/#ospf-interface-optional-support)
- Streamline and speed up the FortiOS initial device configuration by [@a-v-popov](https://github.com/a-v-popov)
- Support for Juniper cSRX container by [@leec-666](https://github.com/leec-666)

<!--more-->

Want more features? How about:

- You can [define scripts](https://netlab.tools/dev/cli-hooks/#dev-cli-hooks) (for example, device license management) that are executed at various points in the `netlab up` and `netlab down` processes.
- The **[netlab restart](https://netlab.tools/netlab/restart/#netlab-restart)** command has been rewritten and now identifies lab topology from the snapshot file
- _netlab_ identifies devices that cannot have their configurations collected/reloaded and generates warnings or errors during **netlab collect**, **netlab up –reload**, or **netlab config –reload**.
- The *configuration reload* feature is now part of the integration tests; the results are in the last column of the *Initial Configuration* [integration test results](https://release.netlab.tools/_html/coverage.initial).
- `graph.linkorder` and `graph.rank` are easier to use in topology graph definitions.
- The [multilab plugin](https://netlab.tools/plugins/multilab/#plugin-multilab) now [serializes](https://netlab.tools/plugins/multilab/#multilab-mutex) concurrent **up** and **down** operations with a mutex lock.

For more details, check the [release notes](https://netlab.tools/release/26.04/), particularly the [breaking changes](https://netlab.tools/release/26.05/#release-26-05-breaking).

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
