---
date: 2021-08-08 16:43:00+00:00
netlab_tag: archive
series_title: Cumulus VX and Nokia SR Linux Containers
tags:
- netlab
title: 'netsim-tools Release 0.8.1: Cumulus VX and Nokia SR Linux Containers'
---
Two interesting container images were released in June/July 2021:

* Michael Kashin managed to package Cumulus VX into a container image ([more details](https://networkop.co.uk/post/2021-05-cumulus-ignite/)).
* Roman Dodin managed to persuade Nokia to [release SR Linux as a container](https://mobile.twitter.com/ntdvps/status/1420786138009190404?s=21).

Both images can be downloaded with no strings attached (two major wins for the good guys) and are [supported with the latest release of netsim-tools](https://netlab.tools/platforms/):
<!--more-->
* Cumulus VX container is fully supported. You can run it in Docker mode or micro-VM mode (needed for MLAG testing) and configure it using the [usual **netlab initial** or **netlab config** commands](https://netlab.tools/netlab/cli/#configuring-and-controlling-the-lab).
* Nokia SR Linux can be used as a device type in network topology, but cannot be configured with **netlab** CLI (**[netlab connect](https://netlab.tools/netlab/connect/)** works). Someone would need to develop Ansible playbooks and configuration templates for SR Linux, and I'm feeling too old to tackle yet-another CLI. Junos is bad enough ;)

Other goodies you'll find in release 0.8.1:

* Now that we have a full-blown no-strings-attached container image (Cumulus VX), I could write automated test of your *containerlab* deployment. Execute **netlab test clab**, sit back and enjoy the show.
* I added the ability to set virtualization provider, device type, and individual topology attributes from the command line. With this functionality you could create container-based or VM-based lab using the same topology file, or change parameters like OSPF area number on-the-fly.
