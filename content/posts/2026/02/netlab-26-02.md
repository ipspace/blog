---
title: "netlab 26.02: KinD support, more EVPN/VXLAN"
series_title: "KinD support, more EVPN/VXLAN (Release 26.02)"
date: 2026-02-11 10:15:00+01:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.02 is out, including the usual potpourri of goodies:

-   Support for [Kubernetes (KinD) clusters](https://netlab.tools/plugins/kind/#plugin-kind) based on work by [@wnagele](https://github.com/wnagele)
-   Layer-2 EVPN/VXLAN support on Cat8000v, IOL, and IOLL2
-   **[netlab graph](https://netlab.tools/netlab/graph/#netlab-graph)** command can create graphs from a subset of nodes or links
-   You can specify the parameters of core links in the **[fabric](https://netlab.tools/plugins/fabric/#plugin-fabric)** plugin
-   OSPFv3 reports

The fun part, however, are the new container configuration methods:
<!--more-->
* Some containers were always configured with Linux scripts (FRRouting, Linux, Bird, dnsmasq). These scripts are now [executed directly](/2026/01/netlab-faster-without-ansible/) instead of wasting time with an Ansible playbook.
* netlab also [converts FRRouting *vtysh* configuration into Linux scripts](/2026/02/netlab-frr-configuration/), making FRRouting/Linux deployments completely Ansible-independent.
* I found a way to [deploy Arista EOS configurations with Linux scripts](/2026/02/netlab-eos-configuration/)
* Many devices can be configured with *containerlab* startup configurations (more about that later)

Most of these configuration methods have the inevitable caveats attached to them, so you have to [explicitly enable them](https://netlab.tools/platforms/#platform-config-mode) with topology defaults.

While implementing that change, I found I had to wait for the SSH server on the Arista cEOS containers before I could start the script-based configuration. Running an Ansible playbook to check that and then continue running **docker exec** commands seemed too much like a Rube Goldberg solution to me, so I implemented the *wait for SSH servers to be ready* check[^clo] directly in **netlab initial** (also part of **netlab up**). 

[^clo]: That check is only required for network devices running in containers (either natively or as VM-in-container). Vagrant checks the SSH servers before claiming the VMs are ready.

That enabled me to add another detail I've always wanted: a *we've been waiting this long for the devices to boot* timer, which tells you exactly how long it takes the vendor bloatware to become configurable.

For even more details, check the [release notes](https://netlab.tools/release/26.02/).
<!--more-->
### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
