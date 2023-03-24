---
title: "What Happened to Leaf Switches with Four Uplinks?"
date: 2023-03-28 06:08:00
tags: [ fabric, design ]
series: [ ASIC ]
---
The last time I spent days poring over vendor datasheets collecting information for the *overview* part of Data Center Fabrics webinar a lot of 1RU data center leaf switches came in two form factors:

* 48 low-speed server-facing ports and 4 high-speed uplinks
* 32 high-speed ports that you could break out into four times as many low-speed ports (but not all of them)

I expected the ratios to stay the same when the industry moved from 10/40 GE to 25/100 GE switches. I was wrong -- most 1RU leaf data center switches based on recent Broadcom silicon (Trident-3 or Trident-4) have between eight and twelve uplinks.
<!--more-->
{{<note warn>}}This is a thinking-out-loud blog post. The basics are obvious, but the more I tried to figure out the details, the more confused I became. Any feedback would be highly appreciated.{{</note>}}

### The Basics

Every data center switching ASIC has N lanes that can be clocked at different frequencies. For example, 25GE lanes can be clocked at 10GE or even 1GE.

You can also combine four lanes coming out of the ASIC into a higher-speed port. 100GE port is nothing more than four bundled 25GE lanes, and if you clock those 25GE lanes at 10GE and bundle them you get 40GE port.

Transceivers implementing 100GE technologies that need four transport lanes (example: short-range fiber -- 100GBASE-SR4) map ASIC lanes straight into optical signals. Transceivers that combine four lanes and push 100GE onto a single optical fiber are way more complex; for more details watch the [NFD23 presentation by Andy Bechtolsheim](https://techfieldday.com/video/networking-industry-roadmap-400g-and-beyond-with-andreas-bechtolsheim-of-arista-networks/) or [400GE section](https://my.ipspace.net/bin/list?id=DCFabric#TECHNOLOGY) in the Data Center Fabrics webinar.

### Back to Uplinks

Before going into details, it's worth noting that there should be no significant difference between *uplink* and *server-facing* ports on most leaf switches using merchant silicon. The obvious exception were early Nexus 9300 switches that had Cisco-brewed magic between Broadcom ASIC and uplink ports (those switches are long gone), and you might find switches with extra MACsec hardware in that place.

There might also be ASIC limitations like _you can only bundle so many lanes into uplink ports_ or _the total number of ports per ASIC is limited, so you cannot have as many ports as you have lanes_ but of course [we'll never know what they are](https://blog.ipspace.net/2016/05/what-are-problems-with-broadcom.html).

Jeff Tantsura [nicely summarized that in a LinkedIn comment](https://www.linkedin.com/feed/update/urn:li:activity:7041477124225949697/):

> I’m not sure about uplink/downlink nomenclature, there’s no “special” uplink functionality that makes it limited to that specific function.

With the modern ASICs being fast enough to get the job done, the most important factors when deciding how many ports to put on a switch (and how fast they should be) must be *physical packaging* and *what will the customers buy.*

For example, if your ASIC has 128 25GE lanes, and you can bundle all of them, you can build a switch with 32 100GE ports. That's a nice spine switch, or you could use it in niche scenarios with 100GE server ports, or you could use breakout cables. Alternatively, the vendor could build a switch with 96 25GE ports and 8 100GE uplinks, but that would no longer be a 1RU switch, and some customers might hate having such a large blast radius. 48 low-speed ports seems to be a sweet spot; some vendors are also offering 24-port and 12-port switches.

Anyway, we still don't know why the old switches had four uplinks while the new ones have eight. The number of ASIC lanes hasn't changed. [Trident2](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56850-series) had 128 lanes, and most switches used just 64 of them. [Trident3](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56870-series) has 128 lanes, and most switches use 80 of them (48 x 25GE ports, 8 x 100GE ports @ 4 lanes). It could be that it became cheaper to add high-speed ports (not transceivers), so it doesn't hurt to have switches with more uplinks addressing the needs of customers requiring lower oversubscription ratios.

However, something doesn't add up:

* Broadcom always claimed that the ASICs bandwidth is the number of lanes x lane speed. For example, [Trident3-X7](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm56870-series) has 128 25GE lanes and 3.2 Tbps of forwarding capacity.
* That figure works out nicely when you connect senders to half of the ports and receivers to the other half of the ports and blast packets across the ASIC. In real life, each port has to *send and receive* packets, so you need twice the declared ASIC bandwidth to get that done.
* Invoking "marketing math" doesn't help. The ASIC of a linerate switch with 32 100GE ports has to shuffle 6.4 terabits per second if all ports are sending and receiving at the same time.
* Switch manufacturers usually claim twice the bandwidth Broadcom claims in its ASIC specs. For example, Arista claims 7050X3 switches have 6.4 Tbps of switching bandwidth[^BD].

[^BD]: Sometimes the vendors add "bidirectional" to the bandwidth they claim to make sure no-one multiplies it by another factor of two.

What is the actual forwarding bandwidth of Broadcom ASICs? Is Broadcom underselling its ASICs or are vendors being too optimistic? Are vendors counting on most deployments being heavily underutilized? After all, it's quite unusual to have a scenario where all ports on a switch would be simultaneously sending and receiving packets at line rate. I have no idea, and if you have a pointer to test results pointing one way or another I'd appreciate if you'd leave a comment.

In any case, even if the ASIC can shuffle the required number of bits through its internal pipelines, we got the *minimum packet size for linerate forwarding* calculations wrong. For example, when I was [writing about the Tomahawk ASIC](https://blog.ipspace.net/2015/12/broadcom-tomahawk-101.html), I wrote:

> Tomahawk becomes line-rate (3.2 Tbps) at packet sizes above 250 bytes

I don't remember if I did the calculation or got it from the Juniper presentation, but I'm pretty sure that _250 bytes_ is the result of dividing the declared bandwidth (3.2 Gbps) with the declared packet-per-second forwarding performance. The actual bandwidth an ASIC would need to support 32 100GE ports is 6.4 Tbps, so the minimum packet size where the ASIC gets linerate forwarding performance would be 500 bytes.

Do these discrepancies and mysteries matter or is it all just another "angels dancing on pins" discussion? In most cases, it doesn't as the average switch utilization stays well below one or the other threshold, but if you're building an environment where you expect to see high traffic volumes, large spikes, or tons of small-sized packets, you'd be better off doing some testing first, and [the results might surprise you](https://people.ucsc.edu/~warner/Bufs/Hepix-2019-San-Diego.pdf).