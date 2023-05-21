---
date: 2022-01-03 09:13:00+00:00
netlab_tag: archive
tags:
- netlab
title: 'netsim-tools: New in December 2021'
---
[Tons of new things](https://netlab.tools/release/1.0/) were added to *[netsim-tools](https://netlab.tools/)* in December 2021:

* [Pete Crocker](https://www.linkedin.com/in/petercrocker/) contributed support for Fortinet devices. You can configure IPv4, IPv6 and OSPF. [More details…](https://netlab.tools/platforms/)
* [Jeroen van Bemmel](https://github.com/jbemmel) contributed support for Nokia SR Linux and SR OS (including initial device configuration, OSPF, ISIS, BGP, and SR-MPLS).
* I added Vagrant box names for IOSv, CSR and vSRX on VirtualBox. You still have to build the boxes, but at least you won’t have to change the default settings.

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab.html).{{</note>}}
<!--more-->
But wait, there's more ;)

* [Hierarchical device groups](https://netlab.tools/groups/#hierarchical-groups)
* Device-specific module attributes ([more details](https://netlab.tools/dev/module-attributes/))
* You can apply [custom deployment templates](https://netlab.tools/groups/#custom-configuration-templates) to individual nodes. They are now deployed as part of [initial device configuration](https://netlab.tools/netlab/initial/), making them similar to configuration modules.
* **[netlab initial](https://netlab.tools/netlab/initial/)** command includes `--fast` option which uses **free** strategy in Ansible playbooks for faster configuration deployment.
* [Jeroen van Bemmel](https://github.com/jbemmel) added multi-access (LAN) links to *containerlab* deployments.
* **netlab up** creates *vagrant-libvirt* management network if needed further simplifying the installation process (contributed by [Stefano Sasso](https://github.com/ssasso))
* [Pete Crocker](https://github.com/petercrocker) fixed XML definition for *vagrant-libvirt* to support labs with more than 10 devices. Current limit is 20 devices, if you feel you need more keep adding static DHCP entries and submit a pull request.

More details in [release notes](https://netlab.tools/release/1.0/). To get started, read the [installation guide](https://netlab.tools/install/) and [tutorials](https://netlab.tools/tutorials/). If you feel like contributing to the project, start with [contributor guidelines](https://netlab.tools/dev/guidelines/).
