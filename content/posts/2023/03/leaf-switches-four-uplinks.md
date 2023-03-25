---
title: "What Happened to Leaf Switches with Four Uplinks?"
date: 2023-03-28 06:08:00
tags: [ fabric, design ]
series: [ ASIC ]
---
The last time I spent days poring over vendor datasheets collecting information for the *overview* part of [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics) webinar a lot of 1RU data center leaf switches came in two form factors:

* 48 low-speed server-facing ports and 4 high-speed uplinks
* 32 high-speed ports that you could break out into four times as many low-speed ports (but not all of them)

I expected the ratios to stay the same when the industry moved from 10/40 GE to 25/100 GE switches. I was wrong -- most 1RU leaf data center switches based on recent Broadcom silicon (Trident-3 or Trident-4) have between eight and twelve uplinks.
<!--more-->
### The Basics

Every data center switching ASIC has N lanes that can be clocked at different frequencies. For example, Broadcom Trident3 has 128 25GE lanes can be clocked at 10GE.

You can also combine four lanes coming out of the ASIC into a higher-speed port. 100GE port is nothing more than four bundled 25GE lanes, and if you clock those 25GE lanes at 10GE and bundle them you get 40GE port.

Transceivers implementing 100GE technologies that need four transport lanes (example: short-range fiber -- 100GBASE-SR4) map ASIC lanes straight into optical signals. Transceivers that combine four lanes and push 100GE onto a single optical fiber (example: 100GBASE-LR1) are way more complex; for more details watch the [NFD23 presentation by Andy Bechtolsheim](https://techfieldday.com/video/networking-industry-roadmap-400g-and-beyond-with-andreas-bechtolsheim-of-arista-networks/) or [400GE section](https://my.ipspace.net/bin/list?id=DCFabric#TECHNOLOGY) in the Data Center Fabrics webinar.

### Back to Uplinks

Before going into details, it's worth noting that there should be no significant difference between *uplink* and *server-facing* ports on most leaf switches using merchant silicon, or as Jeff Tantsura [wrote in a LinkedIn comment](https://www.linkedin.com/feed/update/urn:li:activity:7041477124225949697/):

> I’m not sure about uplink/downlink nomenclature, there’s no “special” uplink functionality that makes it limited to that specific function.

The obvious exception were early Nexus 9300 switches that had Cisco-brewed magic between Broadcom ASIC and uplink ports (those switches are long gone), and you might find switches with extra MACsec hardware in that place.

There might also be ASIC limitations like _you can only bundle so many lanes into uplink ports_ or _the total number of ports per ASIC is limited, so you cannot have as many ports as you have lanes_ but of course [we'll never know what they are](https://blog.ipspace.net/2016/05/what-are-problems-with-broadcom.html).

With the modern ASICs being fast enough to get the job done, the most important factors when deciding how many ports to put on a switch (and how fast they should be) must be *physical packaging* and *what will the customers buy.*

For example, if your ASIC has 128 25GE lanes, and you can bundle all of them, you can build a switch with 32 100GE ports. That's a nice spine switch, or you could use it in niche scenarios with 100GE server ports, or you could use breakout cables. Alternatively, the vendor could build a switch with 96 25GE ports and 8 100GE uplinks, but that would no longer be a 1RU switch, and some customers might hate having such a large blast radius. 48 low-speed ports seems to be a sweet spot; some vendors are also offering 24-port and 12-port switches.

Anyway, we still don't know why the old switches had four uplinks while the new ones have eight. The number of ASIC lanes hasn't changed. According to exceedingly-sparse public Broadcom documentation [Trident2](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56850-series) had 128 10GE lanes, and most switches used just 64 of them (48 x 10GE ports, 4 x 40GE ports). [Trident3](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56870-series) has 128 25GE lanes, and most switches use 80 of them (48 x 25GE ports, 8 x 100GE ports @ 4 lanes).

It could be that it became cheaper to add high-speed ports (not transceivers), so it doesn't hurt to have switches with more uplinks addressing the needs of customers requiring lower oversubscription ratios. It could also be that the true limiting factor was the packet-per-second performance -- when using all lanes, the [forwarding performance of small packets](https://blog.ipspace.net/2021/02/importance-switching-small-packets.html) would be way below the advertised bandwidth figure.

Your guess is as good as mine -- comments highly appreciated ;)

Anyway, in most environments the details discussed in this blog post don't matter -- the average switch (or link) utilization is often an order of magnitude lower than the maximum forwarding performance. On the other hand, if you're building an environment where you expect to see high traffic volumes, large spikes, tons of small-sized packets, mixed speeds, or a mix of TCP and UDP traffic, you'd be better off doing some testing first, and [the results might surprise you](https://people.ucsc.edu/~warner/Bufs/Hepix-2019-San-Diego.pdf).

### Off-Topic: Marketing Math

While trying to figure out the mystery of missing links, I rediscovered the beautiful world of marketing math:

* Broadcom always claimed that the ASICs bandwidth is the number of lanes x lane speed. For example, [Trident3-X7](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56870-series) has 128 25GE lanes and 3.2 Tbps of forwarding capacity.
* Switch manufacturers usually claim twice the bandwidth Broadcom claims in its ASIC specs, sometimes adding "bidirectional" to the inflated figure. For example, Arista claims 7050X3 switches have 6.4 Tbps of switching bandwidth.
* The vendor claims are an obvious example of marketing math. The forwarding performance of an ASIC (or a switch) is the sum of all packets *entering* the switch. Counting each packet twice (once entering once leaving the ASIC) and claiming that's the true forwarding performance is nonsense.
