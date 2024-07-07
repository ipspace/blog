---
date: 2015-07-06 09:13:00+02:00
tags:
- SD-WAN
- traffic engineering
- IP routing
- QoS
- WAN
title: 'Routing Protocols and SD-WAN: Apples and Furbies'
url: /2015/07/routing-protocols-and-sd-wan-apples-and/
sd-wan_tag: myth
---
Ethan Banks recently wrote a [nice blog post](https://packetpushers.net/blog/sd-wan-gives-us-the-best-path-we-always-wanted/) detailing the benefits and drawbacks of traditional routing protocols and comparing them with their SD-WAN counterparts.

While I agree with everything he wrote, the comparison between the two isn't exactly fair -- it's a bit like trying to cut the cheese with a chainsaw and complaining about the resulting waste.
<!--more-->
### Traditional Routing Protocols 101

The traditional routing protocols were designed to solve endpoint reachability problem in a hop-by-hop destination-only forwarding environment of unknown topology.

{{<note info>}}The problem space was limited to destination-only forwarding for a good reason: that's the only forwarding mechanism that scales (assuming decent multi-level summarization).{{</note>}}

A typical routing protocol has to solve these challenges:

-   Create local topology information;
-   Discover adjacent routers (preferably automatically);
-   Exchange reachability and topology information with the adjacent routers;
-   Recreate the network topology based on the available topology information;
-   For every known destination, select a set of paths to reach that destination.

The *routing protocols choose only the best path based on cost* mantra is wrong. Some routing protocols could select suboptimal paths (EIGRP, BGP, potentially also OSPF with LFA), or take in account the network conditions (CSPF in MPLS-TE).

However, as long as we stick to the *hop-by-hop* forwarding behavior, we're severely limited in the set of paths a routing protocol can select -- a routing protocol can never select a path that could result in a forwarding loop (the proof is left as an exercise for the interested reader).

Finally, all routing protocols assume [*shared fate*](/2014/08/fate-sharing-in-ip-networks/) between routing protocol updates and the forwarding path. The moment this assumption is broken, we might experience interesting challenges (just ask anyone who had to configure OSPF on partially-meshed Frame Relay in the CCIE lab without using P2MP interfaces).

{{<note>}}The situation is particularly bad in IXP environments using BGP route servers, and while [people keep proposing solutions to that problem](https://ripe70.ripe.net/archives/video/11/), none of them is anywhere close to perfect.{{</note>}}

### Routing in SD-WAN environments

Routing in SD-WAN environment is almost trivial:

-   There is no need for auto-discovery (SD-WAN nodes register themselves with the central controller);
-   Network topology is trivial: N sets of flat overlay networks;
-   Network topology never changes (because it's an overlay network), the only thing that could change is the reachability of the next hop;
-   Reachability information is collected by the central controller and flooded to the end nodes.

{{<figure src="/2015/07/s1600-SD-WAN+Routing+Protocols.png" caption="SD-WAN routing protocols">}}

Using traditional routing protocols in such an environment is overkill; the only routing protocol that is simple enough for the task at hand is IBGP (and there is at least one SD-WAN vendor that uses BGP behind the scenes). Yes, you could also use RIPv2, but let's not go there.

The results of a routing protocol in SD-WAN environment (or DMVPN environment) are very simple: a set of destinations, and a set of potential underlay (transport) next-hops for each destination. What happens next is no longer a job of a routing protocol.

#### Don't Conflate Load Balancing with Routing

After the SD-WAN controller collects reachability information and distributes it to SD-WAN nodes, each SD-WAN node knows:

-   Which destinations are available;
-   Which transport next hops can be used to reach each destination.

{{<note info>}}Does that look like an ECMP routing/forwarding table? Sure it does ;) Also note that it doesn't matter whether you implement your SD-WAN (or hybrid WAN) network with secret sauce made by a startup or multiple DMVPN tunnels, the results are the same.{{</note>}}

{{<figure src="/2015/07/s1600-SD-WAN+IP+SLA.png" caption="Load balancing in SD-WAN environment">}}

{{<note warn>}}The above description is obviously slightly oversimplified. For example, smart SD-WAN solutions would allow you to configure transport zones ensuring (for example) the SD-WAN node on Site-A knows it cannot reach TB1 using TA2 source IP address.{{</note>}}

The true difference between SD-WAN solutions and traditional forwarding implementations lies in the *algorithm used to distribute packets across alternate paths*. Most networking devices use some variant of (un)equal cost multipathing, whereas SD-WAN devices typically:

-   Continuously measure end-to-end path quality between local node and transport next-hops (the trivial algorithm being *next-hop reachability tracking* -- if there's no response from the next hop, it's obviously down and should not be used);
-   Classify applications in groups (we used to call them *Differentiated Services Code Points*) and send the application traffic on one of the available paths based on path quality and application requirements.

{{<note info>}}Please note that you could have done that with multi-topology routing or DiffServ-aware MPLS-TE for years. It just took way too much effort to deploy.{{</note>}}

-   Some SD-WAN solutions might perform available bandwidth monitoring (based on increased end-to-end delay) and adjust the packet sending rate, similar to what TCP optimization solutions are doing. For more details, listen to [Episode 25](/2015/03/tcp-optimization-with-juho-snellman-on/) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild).

However, these operations have nothing to do with *routing protocols* -- they are (like Cisco's OER or PfR) *local decisions made on the device* based on current characteristics of transport paths.

In short, don't blame the routing protocols if you don't want to configure PfR/OER or if you think they suck.

#### Could We Do This With Routing Protocols?

We could, but that doesn't mean we should. There have been numerous attempts to include QoS-awareness in traditional routing protocols, from *load* parameter in IGRP to QoS-based metrics in OSPF, and Cisco's Multi-Topology Routing.

While I've seen some service providers using QoS-based MPLS TE (DiffServ-Aware TE), I haven't seen anyone using QoS-based routing protocols (if you have, please write a comment). Either the implementations really suck, or there's something fundamentally wrong with the whole picture... and I suspect it's the latter.

You see, shifting traffic across alternate paths works very well in SD-WAN world, because the amount of shifted traffic represents a minuscule part of the overall traffic in the ISP network, whereas shifting traffic based on routing protocol decisions results in significant traffic shifts, which can result in interesting feedback loops in oscillations.

For more details, listen to the [Episode 34](/2015/05/network-monitoring-in-sdn-era-on/) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild) in which we discussed network monitoring in the SDN era.

### More Details

* [Software-Defined WAN (SD-WAN) Overview](https://www.ipspace.net/SD-WAN_Overview) webinar ([free](https://www.ipspace.net/Subscription/Free)) describes the basics of SD-WAN and typical SD-WAN components and architectures.
* [Cisco SD-WAN Foundations and Design Aspects](https://www.ipspace.net/Cisco_SD-WAN_Foundations_and_Design_Aspects) webinar ([free](https://www.ipspace.net/Subscription/Free)) describes Cisco's SD-WAN solution (formerly known as Viptela)
* You'll find my [grumpy take on SD-WAN](https://my.ipspace.net/bin/list?id=SDNUseCases#WAN) in the [SDN Use Cases](http://www.ipspace.net/SDNUseCases) webinar ([subscriber-only](https://www.ipspace.net/Subscription)).
