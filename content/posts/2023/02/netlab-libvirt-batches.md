---
date: 2023-02-13 07:08:00+00:00
netlab_tag: guidelines
tags:
- netlab
title: Start Large netlab Topologies in Smaller Batches
---
It's incredible how little CPU resources some network devices consume in a steady state -- a *netlab* user managed to run almost 100 Mikrotik routers on a 24-core server. Starting them simultaneously (like **vagrant up** tries to do when used with the *vagrant-libvirt* plugin) is a different story. The router virtual machines are configured with two CPU cores for a good reason, and if they don't get enough CPU cycles during the boot time, they get sluggish, Vagrant gives up, and the lab start procedure fails.

One could use a nasty workaround:
<!--more-->
-   Start the lab with **netlab up**.
-   Expect the Vagrant initialization process to fail.
-   Rerun **vagrant up** (which skips already-active virtual machines) as often as needed.
-   Optionally: write a Bash script that executes **vagrant up** until it returns a successful exit status.

[*netlab* release 1.5](https://netlab.tools/release/1.5/) includes a better solution: you can [start virtual machines in *libvirt*-based topologies in batches](https://netlab.tools/labs/libvirt/#starting-virtual-machines-in-batches) and set the batch size to any value that works for the CPU resources of your server and your choice of networking devices. All you have to do is to set the **defaults.providers.libvirt.batch\_size** parameter in lab topology or as a CLI parameter in the **netlab up** command.

The initial batching implementation is as simple as it gets: it takes network devices in the order they are listed in the **nodes** dictionary in lab topology, splits them into equal-sized batches, and passes lists of virtual machines to **vagrant up** commands. Let me know if you have an interesting use case where you'd need a different approach.

### Getting Started

To get more details and learn about additional features included in release 1.5.0, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
