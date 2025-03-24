---
title: "netlab 1.9.6: Static Routes to Default Gateways"
series_title: "Static Routes to Default Gateways (Release 1.9.6)"
date: 2025-03-25 08:25:00+01:00
tags: [ netlab ]
netlab_tag: release
---
Last week, I had to push out [_netlab_ release 1.9.6](https://netlab.tools/release/1.9/#release-1-9-6) to address a particularly nasty Python [dependency hell](https://xkcd.com/1987/) to make _netlab_ work (again) on Ubuntu 24.04 ([more details](/2025/03/netlab-1-9-6-gateway/#dep)). The release also brought these goodies (and a [bunch of bug fixes](https://netlab.tools/release/1.9/#bug-fixes-1-9-6)):

* Add default gateway (including anycast- and VRRP gateway )as a valid next-hop for [static routes](https://netlab.tools/module/routing/#generic-routing-static)
* Rewrite the default gateway processing and add IPv6 default gateways on links without anycast or VRRP gateways
* [Set libvirt MTU to 9500](https://netlab.tools/labs/libvirt/#libvirt-network) on bridge-based networks to avoid the "[transparent fragmentation](https://blog.ipspace.net/2025/03/linux-bridge-mtu-hell/)" on Linux bridges.
* Use device- or node variables to [specify the Juniper vMX license file](https://netlab.tools/caveats/#juniper-vmx).
<!--more-->
### About That Python Dependency {#dep}

Python documentation encourages virtual environments when installing packages[^AD]. That's all fine and dandy if you're running a gazillion different software packages on your laptop, but largely irrelevant if you're using a Linux server (or VM) as an appliance -- the recommended _netlab_ deployment model.

[^AD]: Sometimes Linux distros go as far as almost removing the ability to install packages into default user- or system Python directories.

Furthermore, some Linux distros love to include a random selection of Python packages as system packages. For example, Ubuntu 24.04 comes with preinstalled **rich** package. That's OK as long as every other package is happy with the vendor-selected version of the preinstalled packages, but that may change at any time when someone pushes a new version of their code (and its dependencies) to PyPi[^PIN].

[^PIN]: Yeah, I know we should be pinning the versions of every package used in _netlab_ and all tools used by _netlab_ (like Ansible). In other news, we usually find something better to do with our time.

The **rich** package was "forever" included in Ubuntu 24.04. We knew that, but every package we used was happy with the preinstalled **rich** package, so the _netlab_ installation scripts did not upgrade it.

A few days ago, one of the Python packages used (probably) by Ansible started requiring a newer version of the **rich** package. The upgrade process triggered by that new dependency failed because the original **rich** package was not installed with PyPi, and the _netlab_ Ansible installation script crashed. New _netlab_ users could not install it on Ubuntu 24.04.

**Workaround:** The *netlab* [Ansible installation script](https://github.com/ipspace/netlab/blob/dev/netsim/install/ansible.sh) in release 1.9.6 installs the latest version of the **rich** package (and a bunch of others) with the `--ignore-installed` flag.

### Upgrading or Starting from Scratch?

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
