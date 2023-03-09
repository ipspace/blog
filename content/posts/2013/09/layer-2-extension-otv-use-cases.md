---
date: 2013-09-19 07:02:00+02:00
dr_tag: stretch
series:
- dr
tags:
- bridging
- data center
- WAN
title: Layer-2 Extension (OTV) Use Cases
url: /2013/09/layer-2-extension-otv-use-cases.html
---
I was listening to the fantastic [OTV Deep Dive PQ Packet Pushers](http://packetpushers.net/pq-show-24-cisco-otv-deep-dive-part-1/) podcast while biking around the wonderful Slovenian forests. They started the podcast by discussing OTV use cases, Ethan throwing in long-distance vMotion (the usual long-distance L2 extension selling point), but refreshingly some of the engineers said "well, that's not really the use case we see in real life."

So what were the use cases they were mentioning?
<!--more-->
I loved one of them -- someone **using OTV to get away from L2 interconnect**. They had a traditional L2 interconnect (and all the [associated "goodies"](http://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html)), decided to convert it to L3 interconnect, but still needed some stretched VLANs in the migration period.

And here are the other use cases I gleaned from the podcast:

**External BGP subnets** -- you have a single /24 IPv4 prefix that you have to announce from more than one data center, and most people would immediately think about stretching that same subnet (because you can't advertise two /25s to the Internet) across more than one location hoping that everything works.

Not surprisingly, if the inter-DC WAN link fails, you'll face a [nice split-brain scenario with both data centers advertising the subnet](https://blog.ipspace.net/2012/10/is-layer-3-dci-safe.html), effectively preventing some users from reaching the correct data center ... unless you do some fancy routing, which brings me to the point: you don't need stretched layer-2 subnet to implement this scenario, you just need proper design and some more intelligent routing.

Now, I totally understand that some customers love to sprinkle another layer of pixie dust over their network instead of investing in [proper BGP design and deployment](http://www.ipspace.net/Redundant_Data_Center_Internet_Connectivity). As a system integrator you usually have to go with what your customers want (and are willing to pay for), but the L2 extension still carries a hefty price tag (particularly if you have to buy the M2 linecards and OTV license for Nexus 7000) which might be a bit higher than attending a BGP course and paying someone to design your DC WAN edge (or [review your design](http://www.ipspace.net/ExpertExpress)).

{{<note>}}A totally irrelevant side remark: you do know that you can get more than enough IPv6 address space to cover all the data centers you might have anywhere in the solar system, don't you?{{</note>}}

**Data Center migration**, which is a perfect use case that even I would support. Do keep in mind that you have to sync a lot of things (including storage), which could make the migration project a bit more complex than a simple shutdown-move-powerup procedure, but if you have to move the data center and cannot agree on a reasonably long maintenance window within the next 6 months, you just might have to use long-distance vMotion hoping nothing crashes in the process.

Also, keep in mind that your migration [might not be as fast as you expect it to be](https://blog.ipspace.net/2011/09/long-distance-vmotion-for-disaster.html) -- some people [managed to move 30 VMs in a weekend](https://blog.ipspace.net/2012/07/long-distance-workload-mobility-in.html), which was such a phenomenal achievement that EMC simply [had to document it in a press release](http://www.emc.com/about/news/press/2012/20120709-01.htm).

Finally, don't forget to turn off layer-2 extension when you're done -- you wouldn't want to turn two data centers into a [single failure domain](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html), would you?

**Disaster recovery with SRM** -- yet another use case supporting laziness at the cost of network complexity. I totally understand that you have to use the same subnet in both data centers because [some craplications simply cannot survive a changed IP address](https://blog.ipspace.net/2012/01/ip-renumbering-in-disaster-avoidance.html), but I can't grasp why you wouldn't use SRM external hooks and [reconfigure the switches](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) with [NETCONF](https://blog.ipspace.net/2012/06/netconf-expect-on-steroids.html) (or XMPP or Puppet) during the SRM recovery process to recreate the subnet in the other data center.

BTW, if you're running anything more complex than an [SMB web hosting environment](https://blog.ipspace.net/2012/08/pvlan-vxlan-and-cloud-application.html), you probably have to [migrate firewall and load balancer configurations](https://blog.ipspace.net/2013/05/simplify-your-disaster-recovery-with.html) as well, in which case recreating the lost subnet is the least of your worries ... unless you already deployed [virtual appliances](https://blog.ipspace.net/2013/04/virtual-appliance-performance-is.html).

**Summary** -- I'm [still looking](https://blog.ipspace.net/2011/11/busting-layer-2-data-center.html) for a good layer-2 extension use case (apart from the migration ones).

### More Information

You'll find all you never wanted to know about Data Center interconnects (layer-2 and layer-3, including MPLS/VPN) in the [DCI webinar](http://www.ipspace.net/Data_Center_Interconnects).