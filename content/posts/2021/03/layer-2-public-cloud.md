---
title: "Implementing Layer-2 Networks in a Public Cloud"
date: 2021-03-08 07:46:00
tags: [ cloud, switching, virtualization ]
---
A few weeks ago I got an excited tweet from someone working at Oracle Cloud Infrastructure: they launched full-blown layer-2 virtual networks in their public cloud to support customers migrating existing enterprise spaghetti mess into the cloud.

Let's skip the usual *does everyone using the applications now have to pay for Oracle licenses* and *I wonder what the lock in might be when I migrate my workloads into an Oracle cloud* jokes and focus on the technical aspects of what they claim they implemented. Here's my [immediate reaction](https://twitter.com/ioshints/status/1359542608620646405) (limited to the usual 280 characters, because that's the absolute upper limit of consumable content these days):
<!--more-->
> I wouldn’t do it, but if it works for you, go for it. Would love to see what happens when a sysadmin bridges two networks together with two VMs because redundancy... and has 100s of other instances on the same networks because flat is the new black.

Before going into the technical details, please read the [pretty forthcoming blog post describing some of the technical details](https://blogs.oracle.com/cloud-infrastructure/first-principles-l2-network-virtualization-for-lift-and-shift) and focus on the few details that might matter when we get to the scaling aspects:

* Emulating flooding of multicasts (including broadcasts) and unknown unicasts;
* Dynamic learning of MAC addresses;
* Fast MAC moves, requiring very agile distributed control plane.

### Flooding

I hope Oracle is not "brave" enough to let virtual network flooding ride on top of IP multicast (VMware tried and gave up), which means they have to use *source node replication*, which is a great amplification mechanism. Imagine you have 100 VMs in a virtual L2 network, and each one of them happens to be on a different hypervisor host (not unusual in environments having tens of thousands of physical servers). Every flooded packet sent by every VM is replicated 100 times. 

Not a big deal if we're dealing with ARP (and they implemented ARP proxy anyway), but if someone happens to use [Microsoft NLB](/2012/02/microsoft-network-load-balancing-behind.html) or something similarly stupid (remember: it's all about migrating existing \*\*\*\* into the cloud), it's going to get nasty... or maybe Oracle charges extra for replicated traffic, in which case the worst offenders might decide it's cheaper to get rid of Microsoft NLB?

### Dynamic Learning of MAC addresses

Public cloud providers focused on fast delivery of scalable services make their orchestration systems as streamlined as possible, and as static as possible.

Prime example: AWS. You cannot change VM MAC addresses, and anything extra you want to have (like additional interfaces or IP addresses) has to be configured through the orchestration system.

This top-down architecture has wonderful scaling properties: 

* Flow of information is mostly unidirectional and driven by API calls;
* There's no communication between hypervisor hosts;
* If you do it right, user API calls get translated directly into API calls toward hypervisor hosts, resulting in real-time implementation of changes (as opposed to Azure which seems to be [riding on top of eventually-available message bus](/2019/06/how-microsoft-azure-orchestration.html)).
* It's relatively easy to scale out the orchestration system using an [eventually-consistent scalable back-end database](/2021/02/state-consistency-distributed-controllers.html), more so if you tie each user to a single orchestration system instance.

Compare that to a typical Layer-2 emulation using dynamic MAC address learning with distributed control plane. EVPN might be a perfect example. 

Edge devices have to collect MAC addresses, report them to some central authority (EVPN: route reflectors) which then distributes them to other edge devices. It's no longer a single API client making changes to the virtual network, it's potentially hundreds of clients (hypervisor hosts) making simultaneous changes (registering dynamic MAC addresses).

You could argue that the edge devices could use API calls to register new MAC addresses, effectively turning what seems like a monstrosity into another layer of abstraction on top of the orchestration system... but that brings us straight to the next problem: how fast can you move a MAC or IP address?

Alternatively, you could just forget the whole *orchestration system is king* architecture, give up and implement a layer-2 network that does nothing else but deliver frames to whoever is interested. I've heard that [worked really well for the last 50 years](/2012/05/layer-2-network-is-single-failure.html), but it seems Oracle might have gone (at least partially) down this path with their Real Virtual Router, which is probably similar to (and as resource intensive as) AWS Transit Gateway. 

You do know that AWS charges for transit gateway traffic, right? They do it for a reason: doing packet forwarding in a dedicated appliance sitting on top of a virtual network costs way more than doing it in the hypervisor. Just saying...

### Fast MAC Moves

One of the uses cases described in Oracle's blog post is implementation of traditional clustering mechanisms by IP or MAC address moves, which means that their solution better be *really fast*.

More conservative public cloud providers don't have that problem. IP and MAC addresses are assigned to virtual machines when they're started, and as it takes a while before a VM is ready to work, there's no rush -- it's perfectly OK to propagate MAC and IP addresses across all hypervisor hosts participating in a virtual network within 30 seconds (or a minute or so if you're using Azure public IP addresses). 

Could Oracle get to sub-second failover? Five seconds? We have no idea. However, as it looks like they implemented a dumb L2 virtual network, the failover time depends solely on how fast their hypervisor hosts can update MAC-to-host mappings, and how fast their Real Virtual Router can update its ARP cache.

### In a Nutshell

Remember the *fast, cheap, good* triangle? You could get two out of three, or as Russ White would generalize it: you could get to any point within that triangle (somewhat fast, not too expensive, and reasonably OK), but you can't implode the triangle into a single point. When talking about large-scale virtual networks, we're dealing with a similar triangle with vertices called *fast*, *dynamic* and *scalable*.

Just to give you two well-known data points: 

* VMware paid $1.26 billion dollars for a layer-2 virtualization solution that can (after years of polishing) scale to 1024 hypervisors.
* Cisco paid $860 million for a solution that can (after years of polishing) scale to 80 leaf switches, 1000 tenants, and 21.000 virtual networks.

Please tell me that Oracle cloud is much bigger than that, and that I got it all wrong.