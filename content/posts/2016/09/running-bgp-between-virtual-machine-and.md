---
date: 2016-09-07 12:55:00+02:00
dcbgp_tag: server
series:
- dcbgp
series_weight: 850
tags:
- data center
- BGP
- virtualization
title: Running BGP between Virtual Machine and ToR Switch
url: /2016/09/running-bgp-between-virtual-machine-and.html
---
One of my readers left this question on the blog post [resurfacing the idea of running BGP between servers and ToR switches](https://blog.ipspace.net/2016/03/sysadmins-shouldnt-be-involved-with.html):

> When using BGP on a VM for mobility, what is the best way to establish a peer relationship with a new TOR switch after a live migration? The VM won\'t inherently know the peer address or the ASN.

As always, the correct answer is *[it depends](https://twitter.com/ThePracticalDev/status/770978423363829760)*.
<!--more-->
### Supporting Live VM Mobility

If you want to support live ([hot](https://blog.ipspace.net/2013/02/hot-and-cold-vm-mobility.html)) VM mobility across ToR switches, don't run BGP with the ToR switch. Regardless of how well you fine-tune the setup, it will take at least a few seconds before the BGP session with the new ToR switch is established, making your service inaccessible in the meantime.

As I explained in [another blog post](https://blog.ipspace.net/2013/08/virtual-appliance-routing-network.html) (yes, it's almost exactly three years old), you SHOULD run a BGP session with a route server somewhere in your network, preferably using IBGP to make things simpler.

To add redundancy to the design, peer the VM with two route servers.

### Supporting Physical Servers

If your servers don't move, but you still don't want to deal with neighbor IP addresses or AS numbers, use one or more of these tricks:

-   Configure the same loopback address on all ToR switches (I wouldn't advertise it into the network, and you definitely don't want it to become the ToR switch router ID);
-   Establish BGP session between the physical servers and the loopback address using either IBGP (so everyone is in the same AS number) or using **local-as** on the ToR switch to present the same AS number to all servers.

Deploying FRR on the servers is obviously a better option. For more details, watch the [Leaf-and-Spine Fabric Designs webinar](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs).

### Supporting Disaster Recovery

Running BGP between the virtual machines and the network [simplifies disaster recovery scenarios](https://blog.ipspace.net/2013/05/simplify-your-disaster-recovery-with.html) (and alleviates the need for crazy kludges like stretched VLANs). If this is your use case:

-   Run a set of route servers in each data center to support live VM mobility within each data center;
-   Use the same IP addresses and AS numbers across route servers in all data centers to enable VMs to connect to the route server in the local data center;
-   Don't advertise the shared IP addresses between data centers (you don't want the VMs to connect to a route server in another data center due to a crazy routing glitch).

### Need even more details?

We discussed them in the [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar and in the [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.