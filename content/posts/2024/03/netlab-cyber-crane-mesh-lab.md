---
title: "Cyber Crane Mesh Topology Built with netlab"
date: 2024-03-11 08:57:00+01:00
tags: [ netlab ]
netlab_tag: use
---
[![](https://raw.githubusercontent.com/ipspace/netlab-examples/master/multi-platform/cyber-crane-mesh/img/cyber-crane-mesh.png)](https://github.com/ipspace/netlab-examples/blob/master/multi-platform/cyber-crane-mesh/img/cyber-crane-mesh.png)
{ .sideicon } 

[Milan Zapletal](https://www.linkedin.com/in/milanzapletal/) submitted the [source code](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/cyber-crane-mesh) for a huge lab topology they built with _[netlab](https://github.com/ipspace/netlab-examples/discussions)_. It has almost 50 routers and over 50 Linux nodes to emulate end-users and servers.

They used _netlab_ to configure VLANs, VRFs, IS-IS, OSPF, EIGRP, BGP, MPLS, VXLAN, and EVPN. Imagine how long it would take to configure all that by hand using a more traditional labbing tool.
<!--more-->
The lab uses devices from three different vendors, and some of those devices are known resource hogs. Consequently, they needed a server with 128GB of RAM and 32 CPU cores, and it still took 30 minutes to start the lab -- they had to start the routers in batches of eight to avoid timeouts due to CPU overloads.

Did you build an exciting lab with netlab? Write a comment, send me an email, create a pull request in the *[netlab-examples](https://github.com/ipspace/netlab-examples/)* repository, or describe your work in a [GitHub discussion](https://github.com/ipspace/netlab-examples/discussions).
