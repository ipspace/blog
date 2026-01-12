---
title: "netlab 26.01: EVPN for VXLAN-over-IPv6, Netscaler"
series_title: "EVPN for VXLAN-over-IPv6, Netscaler (Release 26.01)"
date: 2026-01-13 07:19:00+01:00
tags: [ netlab ]
netlab_tag: release
---
I completely rewrote netlab's device configuration file generation during the New Year break. _netlab_ Release 26.01 no longer uses Ansible Jinja2 functionality and works with Ansible releases 12/13, which are used solely for configuration deployment. I had to [break a few eggs](https://netlab.tools/release/26.01/#release-26-01-breaking) to get there; if you encounter any problems, please [open an issue](https://github.com/ipspace/netlab/issues/new/choose).

Other new features include:

-   EVPN for VXLAN-over-IPv6
-   The ‘skip\_config’ [node attribute](https://netlab.tools/nodes/#node-attributes) that can be used to deploy partially-provisioned labs
-   Lightweight [netlab API HTTP server](https://netlab.tools/netlab/api/#netlab-api) by [Craig Johnson](https://github.com/captainpacket)
-   Rudimentary support for Citrix Netscaler by [Seb d'Argoeuves](https://github.com/sdargoeuves)

You'll find more details (and goodies) in the [release notes](https://netlab.tools/release/26.01/).
<!--more-->
### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
