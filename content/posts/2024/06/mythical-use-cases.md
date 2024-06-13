---
title: "The Mythical Use Cases: Traffic Engineering for Data Center Backups"
date: 2024-06-11 12:41:00+0200
lastmod: 2024-06-13 11:02:00+0200
tags: [ data center, fabric, traffic engineering ]
---
Vendor product managers love discussing mythical use cases to warrant complex functionality in their gear. [Long-distance VM mobility](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html) was one of those (using it for disaster avoidance was [Mission Impossible under any real-world assumptions](https://blog.ipspace.net/2011/09/long-distance-vmotion-for-disaster.html)), and *high-volume network-based backups* seems to be another. Here's what someone had to say about that particular unicorn in a LinkedIn comment when discussing whether we need traffic engineering in a data center fabric.

> When you're dealing with a large cluster on a fabric, you will see things like inband backup. The most common one I've seen is VEEAM. Those inband backups can flood a single link, and no amount of link scheduling really solves that; depending on the source, they can saturate 100G. There are a couple of solutions; IPv6 or eBGP SID has been used to avoid these links or schedule avoidance for other traffic.

It is true that (A) in-band backups can be bandwidth intensive and that (B) well-written applications can saturate 100G server links. However:
<!--more-->
* Backup traffic is usually sent from *many clients* to *a few servers*, which must save the received data onto *reasonably priced storage*.

{{<note info>}}Replication traffic in a scale-out cluster is a different story, as the traffic does not converge onto a few nodes, but the comment mentioned backups and VEEAM in particular.{{</note>}}

* The total amount of the backup traffic in a fabric is thus limited by the performance of backup servers- and storage.
* It's somewhat challenging to push 100G through a single TCP session, and the moment the backup system uses more than one TCP session, there's a chance that the affected switches will spread the load across multiple links.
* The most likely network bottleneck of a backup system is the link between the backup server and the adjacent switch, not the uplinks of that switch or the other links in the system.
* Assuming you're using the pretty standard 1:4 speed ratio between server links and fabric links, all traffic to a single backup server could saturate 25% *of a single uplink* of the adjacent switch, and the saturation of other links in the data center fabric would usually be even lower.
* Many data center switches use ASICs that support [dynamic load balancing](https://blog.ipspace.net/2021/03/topology-congestion-driven-load-balancing.html). [Reshuffling the ECMP load distribution](https://blog.ipspace.net/2015/01/improving-ecmp-load-balancing-with.html) to avoid a congested uplink is thus just a question of having properly written software. For example, Cisco ACI (supposedly) does that automatically.
* Even if you were experiencing congestion issues when using a large cluster of backup servers connected to the same set of switches, you could use traditional routing tricks to spread the load across the uplinks.

**Long story short**: while I'm positive there must be data center fabrics that experience network-wide congestion due to backup traffic, the "*we need traffic engineering in data center fabrics to deal with backups*" is a myth for most well-designed mainstream environments. That does not mean you don't have to take backup traffic into account when designing your network, though ;)

### Keep It Simple and Separate (KISS)

Bela Varkonyi described an old-style solution in [his comment](https://blog.ipspace.net/2024/06/mythical-use-cases.html#2288):

{{<long-quote>}}
I have an old-style, robust solution if you have a central backup server.

It is based on my experience that many of such servers to be backed up have unused ethernet ports.

Just connect the backup server to a simple front-end switch (maybe some leftover) and connect to the unused port of each server to be backed up using a direct optical cable from this front-end switch to the target server.

No complexity, no race conditions with the primary traffic. Keep it simple...
{{</long-quote>}}

This approach has just one drawback: the separate network has to be a layer-2 network or at least look like a single subnet to the servers[^PA].

Most servers don't use VRFs or don't have the means of making generic applications VRF-aware, so you can't have two default routes, one for backup and another for the rest of the traffic. That's why VMware mandated a layer-2 vMotion network[^CU] until they figured out how to spell VRF.

[^PA]: Hint: Proxy ARP is your friend

[^CU]: Their claim that a layer-3 network with proxy-ARP was unsupported was a pure _reduce my support costs by ignoring valid customer needs_ decision.