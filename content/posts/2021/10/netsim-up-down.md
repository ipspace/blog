---
title: "Start a Virtual Lab with a Single Command"
date: 2021-10-18 06:57:00
tags: [ automation ]
series: netlab
netlab_tag: overview
---
In mid-October I finally found time to add the icing to the *netlab* cake: **[netlab up](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html)** command takes a lab topology and does everything needed to have a running virtual lab:

* Create *Vagrantfile* or containerlab topology file
* Create Ansible inventory
* Start the lab with **vagrant up** or **containerlab deploy**
* Deploy device configurations, from LLDP and interface addressing to routing protocols and Segment Routing
<!--more-->
{{<note>}}Later releases added [creation or configuration of Linux bridges](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html#provider-specific-initialization), including the *vagrant-libvirt* management network, to the lab startup process.{{</note>}}

Similarly, **[netlab down](https://netsim-tools.readthedocs.io/en/latest/netlab/down.html)** destroys the virtual lab.

Two other features made it into this release:

* [Static node IDs](https://netsim-tools.readthedocs.io/en/latest/nodes.html#augmenting-node-data) in case you want to have very specific loopback IP addresses or router IDs.
* [Static interface addresses](https://netsim-tools.readthedocs.io/en/latest/links.html#static-interface-addressing) on multi-access links.

### Release History

2022-02-15
: Added information about Linux bridge setup
