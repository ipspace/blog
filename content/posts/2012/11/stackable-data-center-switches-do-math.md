---
date: 2012-11-29 07:14:00+01:00
mlag_tag: design
series:
- mlag
tags:
- data center
- fabric
- load balancing
title: Stackable Data Center Switches? Do the Math!
url: /2012/11/stackable-data-center-switches-do-math.html
---
Imagine you have a typical 2-tier data center network (because 3-tier is so last millennium): layer-2 top-of-rack switches redundantly connected to a pair of core switches running MLAG (to get around spanning tree limitations) and IP forwarding between VLANs.

Next thing you know, a rep from your favorite vendor comes along and says: "_did you know you could connect all ToR switches into a virtual fabric and manage them as a single entity?_" Is that a good idea?
<!--more-->
---

This blog post was written in the days when the data center switching vendors loved proprietary approaches to layer-2 fabrics. Those same vendors now admire EVPN and VXLAN, but you might still get exposed to "interesting" ideas, so it's better to be prepared.

---

{{<figure src="/2012/11/s400-MLAG_Leaf_Spine.png" caption="Typical layer-2 leaf-and-spine design">}}

Assuming you have [typical 64-port 10GE ToR switches](http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/) and use pretty safe 3:1 oversubscription ratios, you have 48 10GE server-facing ports and 16 10GE (or 4 40GE) uplinks. If the core switch is non-blocking (please kick yourself if you bought an oversubscribed core switch in the last year or two), every server has *equidistant bandwidth* to every other server (servers connected to the same ToR switch are an obvious exception).

Unless you experience some [nasty load balancing issues](http://packetpushers.net/the-scaling-limitations-of-etherchannel-or-why-11-does-not-equal-2/) where numerous elephant flows hash onto the same physical link, every server gets \~3.33 Gbps of bandwidth toward any other server.

{{<note info>}}The problem of elephant flows hashing onto the same link in a bundle or the same path across the network can be [solved with multipath TCP](http://www.youtube.com/watch?v=02nBaaIoFWU).{{</note>}}

Now let's connect the top-of-rack switches into a stack. Some vendors (example: Juniper) use special cables to connect them; others (HP, but also Juniper) connect them via regular 10GE links. In most scenarios I've seen so far you connect the switches in a ring or a daisy chain.

{{<figure caption="Introducing stackable leaf switches" src="/2012/11/s400-MLAG_Stackable.png">}}

What happens next depends on the traffic profile in your data center. If most of your server traffic is northbound (example: VDI, simple web hosting), you probably won't notice a difference, but if most of your traffic is going between servers (east-west traffic), the stacking penalty will be huge.

The moment you merge the ToR switches into a stack (regardless of whether it's called Virtual Chassis or Intelligent Resilient Framework) the traffic between servers connected to the same stack stays within the stack, and the only paths it can use are the links connecting the ToR switches.

{{<note warn>}}Remember that we're usually talking about a ring/daisy chain here -- a packet might have to traverse multiple hops across the ring to get to the destination ToR switch.{{</note>}}

Now do the math. Let's assume we have four HP 5900 ToR switches in a stack, each switch with 48 server-facing 10GE ports and 4 40GE uplinks. The total uplink bandwidth is 640 Gbps (160 Gbps per switch times four ToR switches) and if half of your traffic is server-to-server traffic (it could be more, particularly if you use Ethernet for storage or backup connectivity), the total amount of server-to-server bandwidth in your network is 320 Gbps (which means you can push 640 Gbps between the servers using [marketing math](http://etherealmind.com/network-dictionary-marketing-math/)).

Figuring out the available bandwidth between ToR switches is a bit trickier. Juniper's stacking cables work @ 128 Gbps. HP's 5900s can use up to four physical ports in an IRF link; that would be 40Gbps if you use 10GE ports and 80Gbps if you use all four 40GE ports on an HP5900 for two IRF links.

{{<note>}}I'm not picking on HP in particular; they just happen to have a handy switch model. Doing the math with Juniper's EX4500 which has 48 10GE ports is more cumbersome.{{</note>}}

You might get lucky with traffic distribution and utilize multiple segments in the ring/chain simultaneously, but regardless of how lucky you are, you'll never get close to the bandwidth you had before you stacked the switches together, unless you started with a large oversubscription ratio.

Furthermore, by using 10GE or 40GE ports to connect the ToR switches in a ring or daisy chain, you've split the available uplink ports into two groups: inter-server ports (within the stack) and northbound ports (uplinks to the core switch). In a traditional leaf-and-spine architecture you're able to fully utilize the all the uplinks regardless of the traffic profile; the utilization of links in a stacked ToR switch design depends heavily on the east-west versus northbound traffic ratio (the pathological case being known as [Monkey Design](/2012/04/monkey-design-still-doesnt-work-well.html)).

**Conclusion:** daisy-chained stackable switches were probably a great idea in campus networks and 1GE world; be careful when using switch stacks in data centers. You might have to look elsewhere if you want to reduce the management overhead of your ToR switches.

### More information

Leaf-and-spine architecture is just the simplest example of the Clos architecture. You'll find fabric designs guidelines (including numerous L2- and L3-designs) in the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures).
