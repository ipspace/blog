---
date: 2019-01-23 08:43:00+01:00
evpn_tag: mpls
tags:
- design
- VXLAN
- EVPN
title: Q-in-Q Support in Multi-Site EVPN
url: /2019/01/q-in-q-support-in-multi-site-evpn/
---
One of my subscribers sent me a question along these lines (heavily abridged):

> My customer runs a colocation business and has to provide L2 connectivity between racks, sometimes even across multiple data centers. They were using Q-in-Q to deliver that in a traditional fabric and would like to replace that with multi-site EVPN fabric with \~100 ToR switches in each data center. However, Cisco doesn't support Q-in-Q with multi-site EVPN. Any ideas?

As Lukas Krattiger explained in his part of [Multi-Site Leaf-and-Spine Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) section of [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar, multi-site EVPN (VXLAN-to-VXLAN bridging) is hard. Don't expect miracles like Q-in-Q over VNI any time soon ;)
<!--more-->
Also, very few chipsets support VXLAN-to-VXLAN bridging. Most recent merchant silicon can do VXLAN routing, including VXLAN-to-VXLAN routing, but you [need high-end ASICs to do VXLAN-to-VXLAN bridging](/2022/06/vxlan-bridging-dci/) or intra-VXLAN split-horizon flooding.

However, you might not need multi-site VXLAN bridging and/or IP multicast (or even EVPN). Figure out:

-   **What services the customer plans to offer**. Are they looking for P2P pseudowires over VXLAN (E-line in Carrier Ethernet terminology) or any-to-any connectivity (E-LAN)? Can your preferred \$vendor provide Q-in-Q with P2P VXLAN? If not, can any other vendor do that?
-   **What are the hardware limitations** (number of VTEPs in the ingress node replication list and total number of remote VTEPs per switch)? Have some serious discussions with the vendor engineers and get the answers in writing (and change vendors if they can't/won't provide them). Make your RFP contingent on meeting or exceeding these limitations.
-   **Is there a scenario where these hardware limitations could be exceeded?** For my subscriber, we're not talking about any-to-any networking over a generic virtualized compute/networking infrastructure but about implementing Carrier Ethernet functionality with VXLAN.

{{<note info>}}Check out the [podcast we did with PacketFabric](/2017/06/packet-fabric-on-software-gone-wild/) -- they went through this same process and deployed a large-scale VXLAN-based solution in production without the complexities of multi-site EVPN.{{</note>}}

If you determine that the hardware limitations will not be exceeded, stop cramming complex technologies into places where they're not needed. You might not need EVPN; an automated flood list configuration based on a customer/services database might be good enough (and more reliable/secure than a dynamic routing protocol).

{{<note info>}}INEX did exactly this. Instead of using EVPN, they automated flood list management with [IXP Manager](https://www.ixpmanager.org/) (an open-source IXP orchestration tool).{{</note>}}

In any case, building a multi-site fabric with hundreds of edge switches is a complex problem, and like I said in the [introduction](https://my.ipspace.net/bin/list?id=DCFabric#INTRO) to [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinar: if you're building a fabric of this size, find someone who did something similar in the past (and we have a few people like that in [ExpertExpress team](https://www.ipspace.net/ExpertExpress)). Relying solely on information provided on the Internet (including my webinars) is probably not good enough, as we can never cover the specifics of your particular deployment.
