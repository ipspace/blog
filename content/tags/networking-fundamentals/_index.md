---
title: Networking Fundamentals
minimal_sidebar: true
layout: custom
---
I firmly believe that you cannot be a good networking engineer[^CLI] without a firm grasp of the networking fundamentals, and I couldn't resist pointing that out a few times (see also [certifications-related posts](/tag/certifications/)):

{{<series-listing tag="important" weight="yes">}}

Regardless of how far down this page you'll get, these blog posts are a must-read:

{{<series-listing tag="must" weight="yes">}}

{{<plushy magic>}}I would also suggest exploring these series of blog posts as well as [textbooks](https://my.ipspace.net/bin/list?id=Net101#TEXTBOOK) and [other resources I collected](https://my.ipspace.net/bin/list?id=Net101#MORE):
{#series}

* [Interfaces and Ports](/series/if_port/)
* [Packet Forwarding Basics](/series/forwarding/)
* [Integrated Routing and Bridging (IRB) Designs](/series/irb/)
* [IP Anycast and Anycast Gateways](/series/anycast/)
* [Site and Host Multihoming](/series/multihoming/)
* [High Availability Switching](/series/ha-switching/)
* [Fast Failover](/series/fast-failover/)
* [Unnumbered IPv4 Interfaces](/series/unnumbered-interfaces/)
* [CLI versus API](/series/cli/)
* [Network State Consistency](/series/consistent-state/)

The rest of the fundamentals-related blog posts are collected on this page.

[^CLI]: In the stricter sense, not in the "every CLI jockey is called an engineer these days" one

### {{<plushy idea>}}Network Addressing

Addresses and routes are the basic concepts anyone dealing with a network must (eventually) grasp. These blog posts describe how we got a hierarchy of addresses:

{{<series-listing tag="addr">}}

### {{<plushy master>}}Deep Dives

These blog posts dive deeper into interesting topics:

{{<series-listing tag="deep">}}

If you like them, it's probably time you start exploring the [deep-dive series](#series) I already mentioned.

### A Bit of a History

These blog posts might help you figure out some less obvious details or give you a historical perspective on why networking technologies evolved to where we are right now:

{{<series-listing tag="history">}}

If you want to dive deeper into historical technologies, you might enjoy the comparison of TCP/IP and OSI (CLNP) protocol stacks:

{{<series-listing tag="osi">}}

### {{<plushy angry>}}There Be Rants

Long-time readers know I can't resist a good rant:

{{<series-listing tag="rant">}}

### Everything Is a Graph

You can represent every network as a graph of network devices (nodes) and links[^MAC]. Rachel Traylor covered the graph theory  in the (free) [Network Connectivity, Graph Theory, and Reliable Network Design](https://my.ipspace.net/bin/list?id=Graph) and [Graph Algorithms in Networks](https://my.ipspace.net/bin/list?id=Algorithms) webinars; these blog posts might provide some extra details:

{{<series-listing tag="graph">}}

[^MAC]: Multi-access networks are represented as pseudo-nodes

### {{<plushy happy>}}Networking Fundamentals Videos

Finally, I published [dozens of videos describing the networking concepts](/2019/08/the-first-networking-fundamentals/) as part of the [How Networks Really Work webinar](https://my.ipspace.net/bin/list?id=Net101) that got at least [some minor positive feedback](/2020/05/feedback-how-networks-really-work/). The videos describe:

**Business aspects of networking technologies**

Some people [liked](/2021/11/feedback-business-aspects-networking/) the [non-technical take on networking](https://my.ipspace.net/bin/list?id=NetBiz) I recorded in 2019 and 2020:

{{<series-listing tag="v_b">}}

{{<jump>}}[More videos](https://my.ipspace.net/bin/list?id=NetBiz#BF){{</jump>}}

**Fallacies of distributed computing**
{{<series-listing tag="v_f">}}

{{<jump>}}[More videos](https://my.ipspace.net/bin/list?id=Net101#FALLACIES){{</jump>}}

**Networking challenges and the importance of a layered approach**
{{<series-listing tag="v_c">}}

**Network Addressing**
{{<series-listing tag="v_a">}}

**Switching, Routing, and Bridging**
{{<series-listing tag="v_s">}}

**Routing Protocols**
{{<series-listing tag="v_r">}}

{{<jump>}}[More videos](https://my.ipspace.net/bin/list?id=Net101#ROUTING){{</jump>}}

**Lessons Learned from 35 Years of Networking**
{{<series-listing tag="v_l">}}

{{<jump>}}[More videos](https://my.ipspace.net/bin/list?id=NetBiz#LL){{</jump>}}

{{<series-untagged noseries="yes">}}