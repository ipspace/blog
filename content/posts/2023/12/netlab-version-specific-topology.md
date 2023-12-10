---
title: "netlab: Version-Specific Topology Files"
date: 2023-12-14 08:18:00+0100
tags: [ netlab ]
pre_scroll: True
---
**TL&DR**: If you're using *[netlab](https://netlab.tools/)* to build labs for your personal use, you can skip this one, but if you plan to use it to create training labs (like my [BGP labs](https://bgplabs.net/) project), you might want to keep reading.

Like any complex enough tool, _netlab_ eventually had to deal with inconsistent version-specific functionality and configuration syntax (OK, topology attributes). I stumbled upon this challenge when I wanted to make labs that use two types of configurable devices.
<!--more-->
When [customizing the BGP labs](https://bgplabs.net/1-setup/#setting-up-the-labs), you can specify the default device type. It can be any of the 20 or so platforms for which we implemented [baseline BGP functionality](https://netlab.tools/platforms/#supported-configuration-modules). The labs also contain devices (external routers) that must be preconfigured, and I decided to use Cumulus Linux on them. Not a problem; I created a group, put all external routers into that group, and specified the device type for the group. This is the relevant part of the original lab topology for the *‌[Configure Multiple EBGP Sessions](https://bgplabs.net/basic/2-multihomed/)* lab exercise:

```
groups:
  external:
    members: [ x1, x2 ]
    module: [ bgp ]
    device: cumulus
```

A few months later, we implemented most of the additional functionality needed on the external routers in **[bgp.session](https://netlab.tools/plugins/bgp.session/)** and **[bgp.policy](https://netlab.tools/plugins/bgp.policy/)** plugins, making it possible to use devices other than Cumulus Linux for external routers ([more details](https://bgplabs.net/1-setup/#selecting-the-network-devices)). Still, you had to change the lab topology files if you wanted to use those devices as external routers. Time for another nerd knob: [default group settings](https://netlab.tools/groups/#default-groups) introduced in *netlab* release 1.6.4.

With the default group settings, you can specify the desired device type for the **external** group in lab defaults, for example:

```
device: eos             # Change to your preferred network device
provider: clab          # Change to virtualbox or libvirt if needed

groups:
  external:
    device: cumulus     # Change to your preferred external router. Needs 1.6.4 to work
```

However, the lab topology settings override the default ones, so I was in a Catch-22 situation:

* If I set the device type for the *external* group in lab topology, then the default group settings don't apply.
* If I don't set the *external* group device type in lab topology, the lab won't work as expected if the user running it uses a _netlab_ release older than 1.6.4.

How about yet another nerd knob: [version-specific topology files](https://netlab.tools/dev/versioning/). If a directory contains `topology.yml` (default filename for the lab topology file) and `topology.1.6.4.yml`, _netlab_ versions lower than 1.6.4 use `topology.yml` while newer versions use `topology.1.6.4.yml`. You can use the same trick multiple times and have (for example) yet another topology file named `topology.1.7.3.yml` that will be used only if you're running _netlab_ release 1.7.3 or later.

Tiny differences due to *default group settings* are just one reason I'm using this approach in BGP labs, for example, in the [Multiple EBGP Sessions](https://github.com/bgplab/bgplab/tree/master/basic/2-multihomed) lab. I'm also using version-specific topology files whenever I can benefit from the new BGP plugin functionality, for example, in the [Filter Transit Routes](https://github.com/bgplab/bgplab/tree/master/policy/2-stop-transit) lab, where I use the **bgp.policy** plugin to change the BGP local preference of the customer routes.
