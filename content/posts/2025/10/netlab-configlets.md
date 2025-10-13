---
date: 2025-10-13 08:30:00+02:00
netlab_tag: extend
pre_scroll: true
series_title: Embed Configuration Templates in a Lab Topology File
tags:
- netlab
title: "netlab: Embed Configuration Templates in a Lab Topology File"
---
A few days ago, I [described how you can use the new **config.inline** functionality](/2025/10/netlab-simple-configuration-changes/) to apply additional configuration commands to individual devices in a *netlab*-powered lab. 

However, sometimes you have to apply the same set of commands to several devices. Although you could use device **groups** to do that, *netlab* release 25.09 offers a much better mechanism: you can embed [custom configuration templates](https://netlab.tools/custom-config-templates/) in the lab topology file.
<!--more-->
The **[files](https://netlab.tools/plugins/files/)** plugin (used to implement the *[inline config](https://netlab.tools/plugins/files/#inline-node-group-configuration-templates)* functionality) also recognizes the [**configlets** dictionary](https://netlab.tools/plugins/files/#creating-custom-configuration-templates) that can be used to create custom configuration templates when starting the lab.

For example, if you want to have **ifup** and **ifdown** templates you could use with **[netlab config](https://netlab.tools/netlab/config/)** command to enable or shut down an interface, you could add these lines to the lab topology file:

```
configlets:
  ifup: |
    #!/bin/bash
    ip link set eth1 up
  ifdown: |
    #!/bin/bash
    ip link set eth1 down
```

Based on the above definition, the **files** plugin creates **ifup.j2** and **ifdown.j2** files in the lab directory whenever you execute the **[netlab up](https://netlab.tools/netlab/up/)** or **[netlab create](https://netlab.tools/netlab/create/)** commands[^RF].

[^RF]: The **[netlab down --cleanup](https://netlab.tools/netlab/down/)** command removes all files created by the **files** plugin as part of the cleanup process.

These commands would work on Linux, FRRouting, BIRD, or dnsmasq nodes (because they all use pure Linux with no custom CLI), but what if you'd like to have [multi-vendor templates](/2022/04/multi-platform-custom-netsim-config/)? No worries, the value of a **configlets** dictionary entry could be another dictionary, for example:

```
configlets:
  ifup:
    eos: |
      interface Ethernet1
        no shutdown
    frr: |
      #!/bin/bash
      ip link set eth1 up
```

The above dictionary would result in two files in the **ifup** subdirectory of the lab directory: `ifup/eos.j2` and `ifup/frr.j2`.

This nicely solves the *shut down an interface on Arista EOS or FRR* challenge, but now we can't use the same configuration template on Linux or BIRD devices unless we add more entries to the **configlets.ifup** dictionary. Even worse, those entries would be identical to the **frr** entry, and you know I hate [data duplication](/kb/DataModels/).

Unfortunately, there's not much we can do *today*. While I implemented a special **base** entry that would allow you to implement the *use this other template for all other devices* functionality, it doesn't work well in this particular scenario (but does work for the more specific templates [described in the documentation](https://netlab.tools/plugins/files/#creating-custom-configuration-templates)). [The fix](https://github.com/ipspace/netlab/pull/2738) is coming in release 25.11 (at which point I'll also update this blog post)
