---
date: 2019-05-22 08:10:00+02:00
mlag_tag: design
series:
- mlag
tags:
- VXLAN
- data center
- WAN
- design
title: Don't Base Your Design on Vendor Marketing
url: /2019/05/dont-base-your-design-on-vendor/
---
Remember how Arista promoted VXLAN coupled with deep buffer switches as the perfect DCI solution a few years ago? Someone took Arista's marketing too literally, ran with the idea and combined VXLAN-based DCI with traditional MLAG+STP data center fabric.

While I love that they [wrote a blog post documenting their experience](http://www.wandynamics.com/blog/8-lessons-learned-arista-datacenter-interconnect-dci-with-vxlan-and-varp) (if only more people would do that), it doesn't change the fact that the design contains the worst of both worlds.

Here are just a few things that went wrong:
<!--more-->
I've seen tons of STP- or MLAG-induced data center meltdowns. The first thing I would want to do in a new data center design would be to **get rid of MLAG** as much as possible. Most hypervisors work just fine without MLAG, and bare-metal Linux or Windows servers need MLAG only if you want to fully utilize all server uplinks. WAN edge routers should use routing with the fabric, and in some cases you can use the same trick with network services appliances.

**End result**: you MIGHT need MLAG to connect network services boxes that use static routing. Connect all of them to a single pair of ToR switches and get rid of MLAG everywhere else.

Even worse, **MLAG-based design limits scalability**. Most data center switching vendors support at most two switches in an MLAG cluster, limiting a MLAG+STP fabric to two spine switches.

Regardless of how you implement them, **large layer-2 fabrics** are a disaster waiting to happen. With VXLAN-over-IP fabric you have at least a stable L3-only transport fabric, and keep the crazy bits at the network edge - the way Internet worked for ages.

Interestingly, most networking vendors have [seen the light](/2016/12/q-building-layer-2-data-center-fabric/), [dropped](/2016/09/replacing-fabricpath-with-vxlan-evpn-or/) their [proprietary or standard L2 fabrics](/2010/08/trill-and-8021aq-are-like-apples-and/) and replaced them with VXLAN+EVPN. Maybe it's time to start considering it.

When interconnecting fabrics, you should **connect leaf switches** not spines. I described the challenge in details in [Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) part of [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar and might write a blog post on the topic; in the meantime the proof is left as an exercise for the reader.

**Raw VXLAN is not the best DCI technology**. I [explained that in 2012](/2012/11/vxlan-is-not-data-center-interconnect/) and [again in October 2014](/2014/10/vxlan-and-otv-saga-continues/)... obviously with little impact.

Yet again, you can find more details in [Lukas Krattiger's presentation](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) in [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar (this part of the webinar is available with [free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free)).

**Deep buffers are not a panacea**. When Arista started promoting deep buffer switches (because they were the first vendor deploying Jericho chipset - now you can buy them from Cisco as well) I asked a number of people familiar with real-life data center designs, [ASIC internals](https://www.ipspace.net/Networks,_Buffers,_and_Drops), and [TCP behavior](/2017/03/tcp-in-data-center-and-beyond-on/) whether you really need deep buffer switches in data centers.

While the absolutely correct answer is always "it depends", in this particular case we got to "mostly NO". You need deep buffers when going from low latency/high bandwidth environment to high latency/low bandwidth one (data center WAN edge); in the core of a data center fabric they do more harm than good. Another reason to connect DCI links to fabric edge.

### What Should They Have Done?

The blog post I quoted at the beginning of this article is a few years old, and it's possible that Arista didn't have VXLAN-capable low-cost ToR switches at that time, but here's what I would do today:

-   Build two layer-3 leaf-and-spine fabrics;
-   Deploy VXLAN with EVPN or static ingress replication on top of them;
-   Connect DCI link to two deep-buffer leaf switches.

### Need more details? {#if-you-want-to-know-more}

-   Start with [Leaf-and-Spine Fabrics Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
-   Explore individual technologies with [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) and [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
-   [Data center interconnects](https://www.ipspace.net/Data_Center_Interconnects) are covered in yet another webinar
-   JR Rivers did a great job [discussing switch buffer sizes and the importance of drops versus delays](https://www.ipspace.net/Networks,_Buffers,_and_Drops)

All ipSpace.net webinars are included with [standard ipSpace.net subscription](https://www.ipspace.net/Subscription). For even more details check out [Building Next Generation Data Centers](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course available with [Expert ipSpace.net Subscription](https://www.ipspace.net/Subscription/Individual).
