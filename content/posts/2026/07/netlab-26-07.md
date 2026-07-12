---
title: "netlab 26.07: GRE, Wireguard, Graceful Restart, and Scale-Out Labs"
series_title: "GRE, Wireguard, Graceful Restart, and Scale-Out Labs (Release 26.07)"
date: 2026-07-13 08:23:00+02:00
tags: [ netlab ]
netlab_tag: release
---
The highlights of _netlab_ release 26.07 include:

- The [**multiserver** plugin](https://netlab.tools/plugins/multiserver/#plugin-multiserver) by [@muddyblack](https://github.com/Muddyblack) distributes containerlab devices across multiple servers.
- The [**GRE tunnel** plugin](https://netlab.tools/plugins/tunnel.gre/#plugin-tunnel-gre) supports GRE tunnels on Cisco IOS, FRR, VyOS, and Junos (vSRX and vJunos-router) (most device implementations done by [@ssasso](https://github.com/ssasso) and [@jbemmel](https://github.com/jbemmel)).
- The [**WireGuard tunnel** plugin](https://netlab.tools/plugins/tunnel.wireguard/#plugin-tunnel-wireguard) by @jbemmel supports WireGuard tunnels on FRR.
- The [**bgp.session** plugin](https://netlab.tools/plugins/bgp.session/#plugin-bgp-session) and the [OSPF module](https://netlab.tools/module/ospf/#module-ospf) support graceful restart on Arista EOS, BIRD, FortiOS, and FRR (by @jbemmel and [@a-v-popov](https://github.com/a-v-popov))
- The [**bgp.policy** plugin](https://netlab.tools/plugins/bgp.policy/#plugin-bgp-policy) supports the **bgp.role** attribute on FRR and BIRD (by @jbemmel).

But wait, there's more ;)
<!--more-->

* BIRD implementation got BGP confederations, VRFs, VXLAN, EVPN MAC VRFs, and [a few other features](https://netlab.tools/release/26.07/#new-device-features) (mostly by @jbemmel)
* FortiOS implementation got BGP support and several new OSPF features (by @a-v-popov)
* Mikrotik RouterOS 7 BGP configuration works with newer releases (by [@snuffy22](https://github.com/snuffy22))
* OpenBSD implementation supports VLANs (by @snuffy22)

Finally, we had to [break a few eggs](https://netlab.tools/release/26.07/#release-26-07-breaking):

- The VirtualBox provider has been removed.
- BIRD v3 is now the [default BIRD version](https://netlab.tools/labs/bird/#build-bird).
- Mikrotik RouterOS 7 BGP templates use the new(er) BGP configuration syntax.

Read the [release notes](https://netlab.tools/release/26.07/) for even more details.

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
