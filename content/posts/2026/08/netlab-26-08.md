---
title: "netlab 26.08: ArcOS, VPP (FD.io), ACLs, and DNS"
series_title: "ArcOS, VPP (FD.io), ACLs, and DNS (Release 26.08)"
date: 2026-08-10 11:58:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.08 brings a few humongous additions:

- ArcOS support by [@roc-ops](https://github.com/roc-ops)
- VPP (FD.io) with FRR or BIRD control plane by [@jbemmel](https://github.com/jbemmel)
- SONiC containers (also by [@roc-ops](https://github.com/roc-ops))
- [IPv4/IPv6 access control lists](https://netlab.tools/module/routing/#generic-routing-acl) in the [**routing** module](https://netlab.tools/module/routing/#generic-routing) by [@DanPartelly](https://github.com/danpartelly)

But wait, there's more:
<!--more-->
- The new [**services** module](https://netlab.tools/module/services/#module-services) configures [DNS clients and servers](https://netlab.tools/module/services/#services-dns-platform)
- GRE tunnels on Arista EOS and GRE/WireGuard tunnels on Mikrotik RouterOS7 and OpenBSD (by [@snuffy22](https://github.com/snuffy22))
- *clab* provider supports the **podman** container runtime ([details](https://netlab.tools/labs/clab/#lab-clab))

Unfortunately, while [fixing device configuration templates](https://netlab.tools/release/26.08/#fixes-in-device-settings-and-configuration-templates) and [other bugs](https://netlab.tools/release/26.08/#bug-fixes), we also had to [break a few (hopefully mostly irrelevant) eggs](https://netlab.tools/release/26.08/#release-26-08-breaking)

Read the [release notes](https://netlab.tools/release/26.08/) for even more details.

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
