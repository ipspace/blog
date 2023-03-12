---
date: 2016-03-21 11:58:00+01:00
high-availability_tag: fail
series_weight: 500
tags:
- data center
- IP routing
- virtualization
- high availability
title: How Hard Is It to Think about Failures?
url: /2016/03/how-hard-is-it-to-think-about-failures.html
---
Mr. A. Anonymous, frequent contributor to my blog posts left this ~~bit of wisdom~~ comment on the VMware NSX Update blog post:

> I don\'t understand the statement that \"whole NSX domain remains a single failure domain\" because the 3 NSX controllers are deployed in the site with primary NSX manager.

I admit I was a bit imprecise (wasn't the first time), but is it really that hard to ask oneself "*what happens if the DCI link fails?*"
<!--more-->
{{<note>}}It's amazing how many people continue to believe in infallibility of redundant architectures years after they stop believing in Santa Claus or Tooth Fairy.{{</note>}}

Having redundant links (or routers or switches) [doesn't mean that your setup cannot fail](https://blog.ipspace.net/2012/10/if-something-can-fail-it-will.html), it only means that *you might have reduced* the probability of the failure. In practice, you might have *reduced the reliability* of your system because you made it more complex and thus harder to understand, configure and monitor.

{{<note info>}}Terry Slattery is an unending source of war stories about people who thought they had a redundant system but didn't... like [running HSRP on only one of the redundant routers](http://www.netcraftsmen.com/what-are-critical-network-problems/).{{</note>}}

Anyway, assuming that we agree there's a non-zero chance of a DCI link failure, let's consider the next question: what happens in the distributed NSX deployment described above when the DCI link fails? The ESXi hosts in the remote data center lose connectivity to the controller cluster, which means that they can no longer adapt to any topology change, VM adds or moves being the most trivial ones.

### Behind the Scenes

If you still want to move forward with this design, it makes sense to understand the particulars (keeping in mind they might change across software releases, potentially making your design implodable-on-failure).

This is the feedback I got from [Dmitri Kalintsev](https://telecomoccasionally.wordpress.com/about/):

In a **single vCenter deployment**, all DRS and VM start operations for the isolated DC would also cease (but the existing VMs would continue to run), so you should be fine from the overlay network connectivity perspective. You\'re still exposed in case of host failures with subsequent HA restarts.

ARP suppression should not be factor, since connections from ESXi hosts to NSX controllers are TCP, and hosts would not be trying to consult controller for ARP suppression if TCP connection is down.

With **site-local vCenter**, DRS / VM start operations are possible, and if executed will likely lead to problems with connectivity in case when link to site with Controllers is down.

This could be taken care of (by setting DRS to something other than full auto, and starting VMs only via something like vRealize Automation which lives in the primary DC), but it\'s something that will need to be thought out beforehand.

Distributed logical routers (DLR) may experience problems at the site disconnected from the Controller Cluster. In some cases DLR-originated (ARP) and DLR-routed traffic may fail to reach destinations due to DLR\'s VNI join failure caused by loss of Controller connectivity.

{{<note info>}}DLR instance on an ESXi host has to join the VNI (VXLAN segment) of the target VM if it wants to forward the traffic to the destination IP address, and that process is traffic- and not topology-driven. If you want to understand the underlying problems, read [this blog post](https://blog.ipspace.net/2013/06/arista-eos-virtual-arp-varp-behind.html) (and follow all the links); packet walks from the [Overlay Virtual Networking webinar](http://www.ipspace.net/Overlay_Virtual_Networking) would also be useful.{{</note>}}

Also, any routing topology changes learned by isolated site\'s DLR\'s Control VM dynamically via BGP or OSPF won\'t be sent to DLR kernel module on hosts, since this process relies on Controllers
