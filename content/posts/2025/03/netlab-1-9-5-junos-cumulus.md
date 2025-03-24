---
title: "netlab 1.9.5: New Cumulus Linux(NVUE) and Junos Features"
series_title: "New Cumulus Linux(NVUE) and Junos Features (Release 1.9.5)"
date: 2025-03-07 07:52:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[Jeroen van Bemmel](https://github.com/jbemmel) and [Stefano Sasso](https://github.com/ssasso) contributed tons of new device features for the [_netlab_ release 1.9.5](https://netlab.tools/release/1.9/#release-1-9-5):

**Cumulus Linux (NVUE):**
* VXLAN and EVPN
* VLAN-aware router (VLAN subinterfaces) functionality
* VRF route leaking
* VRF-aware BGP and full RFC 8950 support (IPv4 BGP AF over regular IPv6 BGP session)
* BGP allowas_in and EBGP multihop
<!--more-->

**Junos:**
* VXLAN and EVPN support on vjunos-switch
* Anycast gateway on vjunos-switch and vjunos-router
* BGP local-as, allowas-in, EBGP multihop, and selective address family activation

We also had several first-time contributors (I love good PRs that appear out of the blue sky):

* [@melvync](https://github.com/melvync) submitted [FortiOS configuration tasks](https://github.com/ipspace/netlab/pull/1933) fixes. The [final fix](https://github.com/ipspace/netlab/commit/10768abcea00bc2e44712e682d270c4d1850abf8) is the merge of his ideas and the _transform data in Jinja2 template_ approach.
* [Steve Ulrich](https://github.com/sulrich) added ["collect configuration" functionality for SONiC](https://github.com/ipspace/netlab/pull/1984)
* [@jdpoland](https://github.com/jdpoland) [fixed](https://github.com/ipspace/netlab/pull/2000) my Edgeshark tool definition FUBAR.

But wait, there's more:

* LAG module support back-2-back dual MLAG use case [with any-to-any links](https://netlab.tools/module/lag/#lag-mlag)
* Jeroen also added a plugin to deploy [VXLAN anycast VTEP in MLAG deployments](https://netlab.tools/plugins/mlag.vtep/#plugin-mlag-vtep)
* If you configure management IPv4 and MAC addresses on individual nodes (they still have to be within the `mgmt` pool), _netlab_ uses them to configure the `vagrant-libvirt` DHCP pool.
* Many CLI commands take `--instance` parameter to run within the context of the specified lab instance.
* If you messed up your container environment, use the `netlab clab cleanup` command

For even more goodies, [read the release notes](https://netlab.tools/release/1.9/#release-1-9-5).

### Upgrading or Starting from Scratch?

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
