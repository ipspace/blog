---
date: 2021-11-01 06:27:00+00:00
netlab_tag: archive
tags:
- netlab
title: netsim-tools Release 1.0
---
It looks like *netsim-tools* reached a somewhat stable state, so it was time to do a cleanup and [publish release 1.0](https://github.com/ipspace/netlab) (also available on PyPi, use **pip3 install --upgrade netsim-tools** to fetch it).

During the cleanup, I removed all references to the obsolete scripts, leaving only the **[netlab](https://netlab.tools/netlab/cli/)** command. I also found an old bash script that [enabled LLDP passthrough on Linux bridges](https://blog.ipspace.net/2020/12/linux-bridge-lldp.html) and made it part of **netlab up** process; your *libvirt*-based labs will have LLDP enabled by default.

Interested? [Install the tools](https://netlab.tools/install/) and [follow the tutorials](https://netlab.tools/tutorials/) to get started.
