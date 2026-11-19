---
title: "netlab 26.11: More Platforms, Less Ansible"
series_title: "More Platforms, Less Ansible (Release 26.11)"
date: 2026-11-23 08:22:00+01:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.11 adds two new platforms:

- IP Infusion OcNOS by [@victorkhgith](https://github.com/victorkhgith), partially based on previous work by [@roc-ops](https://github.com/roc-ops)
- Extreme VOSS by [@sdargoeuves](https://github.com/sdargoeuves)

Other major features include:

- The new **[netlab node](https://netlab.tools/netlab/node/#netlab-node)** command to start, stop, pause, or restart containers (by [@Muddyblack](https://github.com/Muddyblack))
- Ansible-free operations for FRRouting, Linux containers, and Arista, Cisco, and Extreme devices. Yes, you can use *netlab* without installing Ansible ;)

But wait, there's more:
<!--more-->
- **netlab validate** can print [JSON results](https://netlab.tools/netlab/validate/#netlab-validate-json) in case you want to analyze them with your own tool
- The [JSON schema of lab topologies](https://netlab.tools/topology-overview/#topology-schema) by [@kiangribi](https://github.com/kiangribi) enables attribute completion and validation in YAML editors
- [@sdargoeuves](https://github.com/sdargoeuves) added OSPFv3, IBGP, static routes, and route redistribution on Cisco ASAv.
- New **[netlab show plugins](https://netlab.tools/netlab/show/#netlab-show-plugins)** and **[netlab show tools](https://netlab.tools/netlab/show/#netlab-show-tools)** commands
- FRR containers use the new *containerlab* **frr** kind.

Alas, we also had to [break some eggs](https://netlab.tools/release/26.11/#breaking-changes) 🤷🏻‍♂️, including:

- Ubuntu 22.04 and Python 3.10 are [deprecated](https://netlab.tools/install/#install-netlab) and will not be supported in the next release (26.12 or 27.01). **netlab up** and **netlab version** display a warning when running on Python 3.10. Please upgrade to Python 3.11 or later (for example, Ubuntu 24.04 or later).
- FRR containers use the *containerlab* **frr** kind instead of the **linux** kind. *netlab* no longer maps the generated `daemons` file into `/etc/frr/daemons`; *containerlab* generates it from the **daemons** node attribute.
- Ansible core 2.21 dropped the **paramiko\_ssh** connection plugin. *netlab* uses the **ssh** Ansible connection (instead of **paramiko**) for all SSH-based devices. Password-based SSH logins need *sshpass* on the *netlab* host (installed by the Ubuntu and *libvirt* installation scripts).
- The Nokia SR OS and SR-SIM configuration deployment, configuration collection, and readiness checks use the official `nokia.openconfig` Ansible Galaxy collection instead of the archived `nokia.grpc` collection. Rerun **netlab install grpc** to install it (see [Nokia SR OS](https://netlab.tools/caveats/#caveats-sros)).
- Older *vrnetlab* containers might fail to become healthy when running with the *containerlab* version 0.83.0 (required by this release). If you experience this, rebuild those containers using the latest *vrnetlab* code.

Read the [release notes](https://netlab.tools/release/26.11/) for more details, new [device features](https://netlab.tools/release/26.11/#release-26-11-device-features), and [breaking changes](https://netlab.tools/release/26.11/#release-26-11-breaking)

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
