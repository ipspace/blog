---
date: 2025-10-20 09:45:00+02:00
netlab_tag: extend
pre_scroll: true
series_title: Embed Files in a Lab Topology
tags:
- netlab
title: "netlab: Embed Files in a Lab Topology"
---
Today, I'll focus on another feature of the new **[files](https://netlab.tools/plugins/files/)** plugin -- you can use it to embed any (hopefully small) file in a lab topology (**[configlets](/2025/10/netlab-configlets/)** are just a special case in which the plugin creates the relative file path from the **configlets** dictionary data).

You could use this functionality to include configuration files for Linux containers, custom reports, or even plugins in the lab topology, and share a complete solution as a single file that can be [downloaded from a GitHub repository](/2025/09/netlab-download-url/).
<!--more-->
To use this functionality, you have to

* Add the **[files](https://netlab.tools/plugins/files/)** plugin to the lab topology [`plugin`](https://netlab.tools/plugins/) list
* Add the **files** dictionary (or list) to the lab topology [specifying file paths and their contents](https://netlab.tools/plugins/files/#creating-extra-files).

The **files** plugin creates the specified files during the **netlab create** or **netlab up** process. The **netlab down** command removes them when used it is with the `--cleanup` flag.

I use the **files** plugin to create a *bash* script that can be used to create graphs in the sample [physical topology](https://github.com/ipspace/netlab/blob/master/tests/platform-integration/graph/topo.yml), [BGP](https://github.com/ipspace/netlab/blob/master/tests/platform-integration/graph/bgp.yml), [IS-IS](https://github.com/ipspace/netlab/blob/master/tests/platform-integration/graph/isis.yml) and [VLAN](https://github.com/ipspace/netlab/blob/master/tests/platform-integration/graph/vlan.yml) graphs lab topologies. For example, you could execute...

```
netlab create https://github.com/ipspace/netlab/blob/master/tests/platform-integration/graph/isis.yml
```

... in an empty directory to:

* Download the sample IS-IS topology from GitHub
* Transform the lab topology into a snapshot file
* Create the **make.sh** file which can then be executed with **bash make.sh** to create the sample IS-IS graphs.

{{<note warn>}}
The **files** plugin does not check the paths of the created files (yeah, [I know that's not a good idea](https://github.com/ipspace/netlab/issues/2750)). Check any third-party lab topology before using it, and thoroughly check scripts downloaded from the Internet before executing them.
{{</note>}}

Want another example? How about using the **files** dictionary to create a custom report? Let's keep it simple and create a report that will include device type and image for all nodes in the current lab topology:

```
files:
  reports/node-info.j2: |
    {{ "%-16s %-10s %s"|format('name','device','image') }}
    {{ "=" * 80 }}
    {% for name,data in nodes.items() %}
    {{ "%-16s %-10s %s"|format(name,data.device,data.box)}}
    {% endfor %}
```

With the above snippet in your topology file, you could use **netlab report node-info** after starting the lab with **netlab up** to get a simple report listing nodes, device types, and device images, for example:

```
% netlab report node-info
name             device     image
================================================================================
r1               iosv       cisco/iosv
r2               cumulus    CumulusCommunity/cumulus-vx:4.4.5
srv              eos        arista/veos
```

Finally, when you find an interesting use case for this functionality, do let me know (you could leave a comment or send me an email). I always love to hear how you're using _netlab_. Thank you!
