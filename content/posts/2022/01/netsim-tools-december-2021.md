---
date: 2022-01-03 09:13:00+00:00
netlab_tag: archive
tags:
- netlab
title: 'netsim-tools: New in December 2021'
---
[Tons of new things](https://netsim-tools.readthedocs.io/en/latest/release/1.0.html) were added to *[netsim-tools](https://netsim-tools.readthedocs.io/en/latest/index.html)* in December 2021:

* [Pete Crocker](https://www.linkedin.com/in/petercrocker/) contributed support for Fortinet devices. You can configure IPv4, IPv6 and OSPF. [More details…](https://netsim-tools.readthedocs.io/en/latest/platforms.html)
* [Jeroen van Bemmel](https://github.com/jbemmel) contributed support for Nokia SR Linux and SR OS (including initial device configuration, OSPF, ISIS, BGP, and SR-MPLS).
* I added Vagrant box names for IOSv, CSR and vSRX on VirtualBox. You still have to build the boxes, but at least you won’t have to change the default settings.

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab.html).{{</note>}}
<!--more-->
But wait, there's more ;)

* [Hierarchical device groups](https://netsim-tools.readthedocs.io/en/latest/groups.html#hierarchical-groups)
* Device-specific module attributes ([more details](https://netsim-tools.readthedocs.io/en/latest/dev/module-attributes.html))
* You can apply [custom deployment templates](https://netsim-tools.readthedocs.io/en/latest/groups.html#custom-configuration-templates) to individual nodes. They are now deployed as part of [initial device configuration](https://netsim-tools.readthedocs.io/en/latest/netlab/initial.html), making them similar to configuration modules.
* **[netlab initial](https://netsim-tools.readthedocs.io/en/latest/netlab/initial.html)** command includes `--fast` option which uses **free** strategy in Ansible playbooks for faster configuration deployment.
* [Jeroen van Bemmel](https://github.com/jbemmel) added multi-access (LAN) links to *containerlab* deployments.
* **netlab up** creates *vagrant-libvirt* management network if needed further simplifying the installation process (contributed by [Stefano Sasso](https://github.com/ssasso))
* [Pete Crocker](https://github.com/petercrocker) fixed XML definition for *vagrant-libvirt* to support labs with more than 10 devices. Current limit is 20 devices, if you feel you need more keep adding static DHCP entries and submit a pull request.

More details in [release notes](https://netsim-tools.readthedocs.io/en/latest/release/1.0.html). To get started, read the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html) and [tutorials](https://netsim-tools.readthedocs.io/en/latest/tutorials.html). If you feel like contributing to the project, start with [contributor guidelines](https://netsim-tools.readthedocs.io/en/latest/dev/guidelines.html).
