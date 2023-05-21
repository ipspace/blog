---
date: 2022-01-24 07:36:00+00:00
netlab_tag: use
tags:
- traffic engineering
- netlab
title: 'Sample Lab: RSVP TE on Junos'
---
It's amazing how creative networking engineers become once they have the basic tools to get the job done a bit quicker. Last week Pete Crocker [published the largest topology](https://github.com/ipspace/netlab-examples/tree/master/routing/rsvp-mpls-vsrx) I've seen built with *netlab* so far: a 13-router lab running RSVP TE to transport IP traffic between external autonomous systems[^1].

[^1]: I couldn't start it on my meager Intel NUC with 32 GB of RAM and 8 cores; maybe it's time to start labbing on AWS.

{{<figure src="https://raw.githubusercontent.com/ipspace/netlab-examples/master/routing/rsvp-mpls-vsrx/mpls.png" caption="Lab topology">}}
<!--more-->
I particularly like the simplicity of building and configuring this lab: 

* The [topology file](https://github.com/ipspace/netlab-examples/blob/master/routing/rsvp-mpls-vsrx/topology.yml) is as simple as it can get. *netlab* takes care of IP addressing, Vagrant configuration file and Ansible inventory.
* *netlab* configures interfaces, IP addresses, IS-IS, and BGP on [over a dozen platforms](https://netlab.tools/platforms/) (including Junos). All Pete had to create was a [simple configuration template](https://github.com/ipspace/netlab-examples/blob/master/routing/rsvp-mpls-vsrx/junos_mpls_rsvp.j2) containing just a few lines (increase MTU, enable MPLS, enable MPLS TE).

Interested? Read [Pete's instructions](https://github.com/ipspace/netlab-examples/blob/master/routing/rsvp-mpls-vsrx/README.md) or start with *netlab* [installation guide](https://netlab.tools/install/) and [tutorials](https://netlab.tools/tutorials/).
