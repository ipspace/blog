---
title: "netlab: Testing Network Protocol Implementations"
series_title: "Testing Network Protocol Implementations"
date: 2026-11-02 08:18:00+0100
tags: [ netlab ]
netlab_tag: testing
---
Donnie Savage [decided](https://www.linkedin.com/posts/diivious_openeigrp-beta-050-released-first-real-share-7521891637250134016-dz1i/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAF0NisBME_cExE6SWQqx9fCT6lHPXgRxA4) to use [netlab](https://netlab.tools/) to test [OpenEIGRP](https://github.com/diivious/openeigrp)-Cisco IOS [interoperability](https://github.com/diivious/openeigrp/tree/master/netlabs) (TL&DR: [it works](/2026/10/openeigrp-netlab/) and the [source code](https://github.com/diivious/openeigrp/tree/master/netlabs) is in Donnie's EIGRP repository).

He asked me for a few hints before setting up his test server. This is what I sent him; you might find it useful if you ever decide to use _netlab_ to test a new network device/protocol implementation.
<!--more-->
**Infrastructure:**

* [Use containers](https://netlab.tools/labs/clab/) (provider: `clab`). They often start way faster than virtual machines, and we're [moving away from Vagrant anyway](https://blog.ipspace.net/2026/09/sunsetting-vagrant-libvirt/).
* IOL is the best image for IOS/XE (actually, it's IOLL2 because it starts faster, but I wouldn't count on it having all features).
* If you want to test against Nexus OS, download the latest version (free, requires registration) and [use vrnetlab to turn it into a container](https://containerlab.dev/manual/kinds/vr-n9kv/)

**Directory structure:**

* You could have one lab topology per directory, in which case use `topology.yml` as the topology file name
* It's also perfectly possible to have numerous topology files in the same directory. In that case, you have to supply the topology file name to the **[netlab create](https://netlab.tools/netlab/create/)** or **[netlab up](https://netlab.tools/netlab/up/)** commands.
* It's easier to have [project-wide defaults](https://netlab.tools/defaults/#changing-defaults-in-user-defaults-files) with a single directory (in which case the defaults file name is `topology-defaults.yml`), but it's also possible to have [project-wide defaults](https://netlab.tools/defaults/#alternate-defaults-files-locations) with a more complex directory structure (see [BGP labs](https://github.com/bgplab/bgplab) for an example).

**Defaults:**

* I would change all FRR settings (image name, modules...) in the directory/project/user [defaults](https://netlab.tools/defaults/).
* You could use [wildcard groups](https://netlab.tools/groups/#creating-custom-object-groups) defined in [defaults](https://netlab.tools/groups/#default-groups) to set device type and other attributes. For example, you could say "everything starting with C is device `iol`, and everything starting with N is device `nxos`, while the default device type is `frr`.

**Using existing netlab functionality:**

* netlab has minimal EIGRP support. You'll probably find it useless, but of course feel free to enhance it and submit a PR.
* I would rely on netlab to deal with the rest of device configuration, for example, [addressing](https://netlab.tools/example/addressing-tutorial/), [OSPF](https://netlab.tools/module/ospf/), [BGP](https://netlab.tools/module/bgp/), and [static route configuration](https://netlab.tools/module/routing/#static-routes).

**Configuring EIGRP:**

* The easiest way to start would be [custom configuration templates](https://netlab.tools/custom-config-templates/), which can be Jinja2 templates, so you can make them reusable across labs, plus potentially avoid dealing with stuff like interface name details.
* After you get the initial quirks out of the way, I could help you set up a more generic system, or add OpenEIGRP support to netlab (a PR is [always appreciated](https://netlab.tools/dev/guidelines/)).
