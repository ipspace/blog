---
date: 2012-01-10 08:56:00+01:00
tags:
- VXLAN
- data center
- fabric
- overlay networks
- virtualization
title: Can We Really Ignore Spaghetti and Horseshoes?
url: /2012/01/can-we-really-ignore-spaghetti-and.html
---
Brad Hedlund wrote a [thought-provoking article](http://bradhedlund.com/2011/12/22/on-optimizing-traffic-for-network-virtualization/) a few weeks ago, claiming that the [horseshoes](http://blog.scottlowe.org/2011/12/07/revisiting-vxlan-and-layer-3-connectivity/) (or [trombones](/2011/02/traffic-trombone-what-it-is-and-how-you.html)) and [spaghetti](/2011/10/vxlan-termination-on-physical-devices.html) created by virtual workloads and appliances deployed anywhere in the network don't matter much with new data center designs that behave like distributed switches. In theory, he's right. In practice, less so.
<!--more-->
{{<note update>}}**Update 2020-12-25**: It's amazing how much our thinking has changed in the last decade. Leaf-and-spine fabrics are the only way to build data center networks (according to every vendor out there), and bandwidth became cheap enough that workload placement became a non-issue.{{</note>}}

Let's make a step back. Brad started his reasoning by comparing data center fabrics with physical switches, saying "*We don't need to engineer the switch*" and "*We don't worry too much about how this internal fabric topology or forwarding logic is constructed, or the consequential number of hops.*"

Well, we don't until we stumble across an [oversubscribed linecard](http://www.netcordia.com/community/blogs/terrys_blog/archive/2011/10/17/application-performance-troubleshooting.aspx), or a linecard design that [allows us to send a total of 10Gbps through four 10GE ports](http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9402/ps9512/Data_Sheet_C78-437757.html). The situation gets worse when we have to deal with stackable switches, where it matters a lot whether the traffic has to traverse the stacking cables or not (not to mention designs where [switches in a stack are connected with one or a few regular links](/2011/09/long-distance-irf-fabric-works-best-in.html)).

The situation is no different in the "virtual switch" scenario. We don't care about the number of hops across the virtual switch and the latency *as long as it's consistent and predictable*. If the "virtual switch" uses Clos-like architecture that [Brad can build from tens of switches](http://bradhedlund.com/2011/11/05/hadoop-network-design-challenge/), or Cisco can build from Nexus 7K/5K/2K (watch the [*Evolving Network Fabrics* video](http://techfieldday.com/2011/cisco-presents-networking-tech-field-day-2/) from Cisco's presentation @ Networking Tech Field Day 2 -- the fun part starts at approximately 26:00) \... or that you can buy [prepackaged and tested from Juniper](/2011/09/qfabric-part-1-hardware-architecture.html), then the traffic flows truly don't matter -- any two points not connected to the same access-layer switch are equidistant in terms of bandwidth and latency. As soon as you go beyond a single fabric, or out of a single data center, the situation changes dramatically, and bandwidth and latency become yet again very relevant.

Then there's also the question of costs. Given infinite budget, it's easy to build very large fabrics that give the *location doesn't matter* illusion to as many servers or virtual machines as needed. Some of us are not that lucky; we have to live with fixed budgets, and we're usually caught in a catch-22 situation. Wasting bandwidth to support spaghetti-like traffic flows costs real CapEx money (not to mention not-so-very-cheap maintenance contracts); trying to straighten cooked spaghettis continuously being made by virtualized workloads generates OpEx costs -- you have to figure out which one costs you less in the long run.

Last but not least, very large fabrics are more expensive (per port) than smaller ones due to increased number of Clos stages, so you have to stop somewhere -- supporting constant bandwidth/latency across the whole data center is simply too expensive.

I'm positive Brad knows all that, as do a lot of very smart people doing large-scale data center designs. Unfortunately, not everyone will get the right message, and a lot of people with subscribe to the "*traffic flows don't matter anymore*" mantra without understanding the underlying assumptions (like they did to the "*[stretched clusters make perfect sense](/2011/06/stretched-clusters-almost-as-good-as.html)*" one), and get [burnt in the process](/2011/12/large-scale-l2-dci-true-story.html) because they'll deploy workloads across uneven fabrics or even across lower-speed links.

For example, a few microseconds after VXLAN was launched, someone in his infinite wisdom claimed that VXLAN solves inter-data center VM mobility (no, it doesn't). It seems that every generation of engineers has to [rediscover the fallacies of distributed computing](http://en.wikipedia.org/wiki/Fallacies_of_Distributed_Computing), and the new cycle of discoveries has just begun fueled by the hype surrounding virtual switches and [software-defined networking](/2011/03/open-networking-foundation-fabric.html).

## More information

If you're faced with the question "*what is this virtual network stuff all about?*" the [*Introduction to Virtual Networking*](http://www.ipspace.net/VMintro) webinar might give you the answers you need. Clos fabrics and numerous other architectures are described in details in the [*Data Center Fabric Architectures*](http://www.ipspace.net/DCFabric) webinar. If your problem is building a data center to support cloud services, check out the [*Cloud Computing Networking*](http://www.ipspace.net/CloudNet) one.
