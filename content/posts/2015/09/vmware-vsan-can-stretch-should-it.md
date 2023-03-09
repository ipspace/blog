---
date: 2015-09-17 08:40:00+02:00
dr_tag: vendor
ha-cluster_tag: overview
high-availability_tag: dr
series:
- ha-cluster
- dr
tags:
- data center
- SAN
- virtualization
- high availability
title: VMware VSAN Can Stretch – Should It?
url: /2015/09/vmware-vsan-can-stretch-should-it.html
---
[Pirmin Sidler](https://www.linkedin.com/pub/pirmin-sidler/56/2aa/445) read the stretched VSAN blog posts by Duncan Epping ([intro](http://www.yellow-bricks.com/2015/08/31/what-is-new-for-virtual-san-6-1/), [HA/DRS considerations](http://www.yellow-bricks.com/2015/09/09/hadrs-configuration-with-virtual-san-stretched-cluster-environment/), [demo](http://www.yellow-bricks.com/2015/09/10/virtual-san-stretched-clustering-demo/)) and asked me what I think about stretched VSAN considering my [opinions on long-distance vMotion](http://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html).

TL&DR answer: it makes way more sense than long-distance vMotion. However...
<!--more-->
{{<note update>}}2015-09-17: VSAN is similar to synchronous, not asynchronous replication. Added the explanation from Duncan Epping.{{</note>}}

### Does It Need Stretched VLANs?

VSAN is storage replication technology that runs on top of TCP, so it can run over any L3 network. It does need IP multicast between the VSAN nodes, but not between VSAN nodes and the witness node(s).

Stretched vSphere HA cluster running VSAN thus doesn't require stretched VLANs (unless, of course, you plan to move VMs willy-nilly across the WAN links -- most often a [bad idea](http://blog.ipspace.net/2015/01/latency-killer-of-spread-out.html)).

### Can You Use It for Disaster Recovery?

VSAN data replication is almost identical (at least conceptually) to ~~asynchronous~~ synchronous storage replication -- every write is immediately queued for mirroring, and acknowledged to the writer only when the other VSAN nodes acknowledge it.

{{<note>}}Additional explanation by Duncan Epping: VSAN in a stretched configuration is similar to \"sync replication\". It uses an object based model where IOs are split to each of the components of an object tree. Only when each of the components have received the IO will it be acknowledged to the OS/Application. Note that the IO is split before it is written to a device, so this is the purest form of sync IO if you ask me :){{</note>}}

Do keep in mind that VSAN runs on top of vSphere HA cluster, and if you don't want to move VMs between data centers, you MUST use affinity rules to keep them contained (for more details, read [Duncan's blog post](http://www.yellow-bricks.com/2015/09/09/hadrs-configuration-with-virtual-san-stretched-cluster-environment/)).

As you'd be relying on vSphere HA mechanisms for disaster recovery, you won't get any of the goodies SRM brings to the table: each VM will be restarted automatically in whatever order, or not (if the remaining part of the cluster doesn't have enough resources). This might be good enough for small independent workloads, but maybe not for complex application stacks.

Finally, you'll have to solve network connectivity challenges, unless you plan to deploy stretched VLANs (and even [Gartner agrees](http://blog.ipspace.net/2015/09/blessed-by-gartner-stretched-vlans-make.html) they're not a good idea) and [stretched firewall clusters](http://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html) (even worse idea).

All things considered, it might be best to write an orchestration solution (it would be even better if VMware would do that) that would:

-   Create lost subnets in the new data center;
-   Configure any other network services that may be required (unless you're [using virtual appliances](http://blog.ipspace.net/2013/05/simplify-your-disaster-recovery-with.html));
-   Restart VMs in proper startup order.

{{<note>}}Many thanks to Duncan Epping for confirming my understanding of VSAN principles and caveats in an extremely short timeframe.{{</note>}}
