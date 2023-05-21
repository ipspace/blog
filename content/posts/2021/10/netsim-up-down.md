---
date: 2021-10-18 06:57:00+00:00
netlab_tag: overview
tags:
- netlab
title: Start a Virtual Lab with a Single Command
---
In mid-October I finally found time to add the icing to the *netlab* cake: **[netlab up](https://netlab.tools/netlab/up/)** command takes a lab topology and does everything needed to have a running virtual lab:

* Create *Vagrantfile* or containerlab topology file
* Create Ansible inventory
* Start the lab with **vagrant up** or **containerlab deploy**
* Deploy device configurations, from LLDP and interface addressing to routing protocols and Segment Routing
<!--more-->
{{<note>}}Later releases added [creation or configuration of Linux bridges](https://netlab.tools/netlab/up/#provider-specific-initialization), including the *vagrant-libvirt* management network, to the lab startup process.{{</note>}}

Similarly, **[netlab down](https://netlab.tools/netlab/down/)** destroys the virtual lab.

Two other features made it into this release:

* [Static node IDs](https://netlab.tools/nodes/#augmenting-node-data) in case you want to have very specific loopback IP addresses or router IDs.
* [Static interface addresses](https://netlab.tools/links/#static-interface-addressing) on multi-access links.

### Release History

2022-02-15
: Added information about Linux bridge setup
