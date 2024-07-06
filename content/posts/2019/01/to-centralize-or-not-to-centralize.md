---
date: 2019-01-16 08:33:00+01:00
ha-cluster_tag: sdn
high-availability_tag: ignore
series:
- ha-cluster
tags:
- data center
- fabric
- high availability
title: To Centralize or not to Centralize, That’s the Question
url: /2019/01/to-centralize-or-not-to-centralize.html
---
One of the attendees of the Building Next-Generation Data Center online course solved the *build small data center fabric* challenge with [Virtual Chassis Fabric (VCF)](https://my.ipspace.net/bin/get/DCFabric/M53%20-%20Virtual%20Chassis.mp4). I pointed out that I would prefer not to use VCF as it uses centralized control plane and is thus a single failure domain.

{{<note info>}}In case you're interested in data center fabric architecture options, check out [this section](https://my.ipspace.net/bin/list?id=DCFabric#ARCHITECTURES) in the [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinar.{{</note>}}

Here are his arguments for using VCF:
<!--more-->
> As for the architecture, VCF is a simple design for small to medium DC. It is a centralized architecture but has the L2 and L3 simplicity to provide scalability for legacy application while also using L3. There are redundant route engines to assist in failure of master route engine. Protocols like GRES ( graceful route engine switchover), NSR / NSB, non-stop routing/bridging also assist in quick RE fail-overs while also assisting protocols in convergence times.

They are all valid arguments, but in practice I dislike centralized control/management plane architectures because they're really hard to get right... and if you get byzantine control plane failure, you lose the whole fabric.

Also, there are occasional software upgrade challenges that you don't get with independent boxes, and everyone who's been in networking long enough has a scary horror story about a failed stackable switch upgrade.

An obvious alternative to VCF would be a traditional leaf-and-spine fabric with VXLAN using either EVPN control plane or [statically-configured ingress BUM replication with dynamic MAC learning](https://my.ipspace.net/bin/get/DCFabric/RQ0%20-%20Keep%20It%20Simple.mp4). More robust, less complex software, smaller blast radius... but harder to design and configure.

As always, it's the question of [explicit versus hidden complexity](/2018/02/how-self-sufficient-do-you-want-to-be.html), and you have to choose which one is better for you. I have no problem with that - it's just that the customers going for hidden complexity aren't always aware of the risks they're taking.

### Further Reading

-   [Should we use redundant supervisors?](/2014/04/should-we-use-redundant-supervisors.html)
-   [Do you need ISSU on your ToR switch?](/2015/06/so-you-need-issu-on-your-tor-switch.html)

### To Learn More about These Topics

Check out ipSpace.net [data center webinars](https://www.ipspace.net/Roadmap/Data_center_webinars), in particular

-   [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics)
-   [Designing Leaf-and-Spine Fabrics](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
-   [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
-   [VXLAN Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)

Need even more? How [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course?
