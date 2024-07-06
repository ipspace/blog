---
date: 2012-08-21 07:07:00+02:00
tags:
- VXLAN
- cloud
- overlay networks
title: PVLAN, VXLAN and Cloud Application Architectures
url: /2012/08/pvlan-vxlan-and-cloud-application.html
---
Aldrin Isaac [made a great comment](/2012/07/could-mpls-over-ip-replace-vxlan-or.html?showComment=1344218766617#c3812932304135234188) to my [*Could MPLS-over-IP replace VXLAN?*](/2012/07/could-mpls-over-ip-replace-vxlan-or.html) article:

> As far as I understand, VXLAN, NVGRE and any tunneling protocol that use global ID in the data plane cannot support PVLAN functionality.

He's absolutely right, but you shouldn't try to shoehorn VXLAN into existing deployment models. To understand why that doesn't make sense, we have to focus on the typical cloud application architectures.
<!--more-->
To be more precise, *any tunneling protocol that uses global ID in the data plane [**and uses flooding to compensate for lack of control plane**](/2011/12/vxlan-ip-multicast-openflow-and-control.html) cannot support PVLAN*. [Nicira's NVP](/2012/02/nicira-uncloaked.html) has port isolation (which is equivalent to a simple PVLAN); they could do it because the NVP controller(s) [download all MAC-to-IP mappings and MAC forwarding entries into the hypervisor switches](/2011/10/what-is-nicira-really-up-to.html).

### SMB LAMP stack

Numerous service providers that were previously offering simple web hosting are now selling cloudwashed VM-based services (example: the hosting company I use for one of my private web sites is now offering [Virtual Private Servers](http://myhosting.com/virtual-private-server/)). The deployment model is simple: you get a single Linux (or Windows) server with Internet connectivity (hopefully firewalled to stop the script kiddies), and you'd usually install the [LAMP stack](http://en.wikipedia.org/wiki/LAMP_(software_bundle)) or [something similar](http://en.wikipedia.org/wiki/List_of_AMP_packages) on that server (LAMP = Linux, Apache, MySQL, PHP/Perl/Python). Sometimes the service provider offers hosted database service promising redundancy and backup.

{{<figure src="/2012/08/s400-LAMP_stack.png" caption="Typical LAMP stack">}}

In this environment, each tenant gets a single VM that has Internet connectivity and (optionally) access to some central services. VMs are not supposed to communicate with each other (even though you might buy more than one).

PVLAN is the perfect infrastructure solution for this environment -- deploy a PVLAN in each compute pod (whatever that might be -- usually a few racks), and use IP routing between pods. You can still use vMotion and HA/DRS within a pod, so you can move the customer VMs when you want to perform maintenance on individual pod components.

Evacuating a whole pod is bit more complex, but then (hopefully) you won't be doing that every other day. If you really want to have this capability (because restarting customer VMs every now and then is not an option), develop a migration process where you temporarily provision a PVLAN between two pods, move the VMs and shut down the temporary inter-pod L2 connection, thus minimizing the risk of having a large-scale VLAN across multiple pods.

**Summary:** you don't need VXLAN if you're selling individual VMs. PVLANs work just fine.

### Scale-out Application Architecture

Modern scale-out application architectures are way more complex than a simple non-redundant LAMP stack. You'd have numerous web servers sitting behind a load balancer, you might be using web caches (example: Varnish) or offload servers (example: FastCGI), message queues, batch worker processes, cache daemons, and a bunch of database servers. As [\@devops_borat wrote](https://twitter.com/DEVOPS_BORAT/status/222837225921060864):

{{<figure src="/2012/08/s400-HelloWorld_cloud.png">}}

The servers you'd use in a scale-out application usually belong to different security zones, so you'd want to use firewalls between them. You might also need load balancing between tiers (some programmers don't grasp the importance of having redundant database connections \... or the stupidity of having hard-coded database connection information), and the servers within a tier might have to communicate with each other (example: database servers or web caches and web servers).

In short -- you need multiple isolated virtual network segments with firewalls and load balancers sitting between the segments and between the web server(s) and the outside world.

{{<figure src="/2012/08/s1600-Scale_Out.png" caption="Simplified scale-out application architecture">}}

[VXLAN](/2011/09/vxlan-otv-and-lisp.html), [NVGRE](/2011/09/nvgre-because-one-standard-just-wouldnt.html) or [NVP](/2012/02/nicira-uncloaked.html), combined with virtual appliances, are an ideal solution for this type of application architectures. Trying to implement these architectures with PVLANs would result in a total spaghetti mess of isolated and community VLANs with multiple secondary VLANs per tenant.

### Summary

MAC-over-IP virtual networking solutions are not a panacea. They cannot replace some of the traditional isolation constructs (PVLAN), but then they were not designed to do that. Their primary use case is an Amazon VPC-like environment with numerous isolated virtual networks *per tenant*.

### More Information

If you're new to virtualized networking and would like to understand what this is all about, start with the [*Introduction to virtualized networking*](http://www.ipspace.net/Introduction_to_Virtualized_Networking) webinar. Various virtual networking technologies are described in _[Networking in Private and Public Clouds](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds)_
webinar.