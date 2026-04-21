---
title: "Ten Years of ITNOG"
date: 2026-04-22 07:25:00+0200
tags: [  ]
---
I spent the last two days in Bologna at ITNOG 10 in the excellent company of Italian networking engineers (many of them personal friends) and a few guests from around the world. As always, the organizers and the program committee didn't disappoint -- it was a smoothly organized, lovely event full of interesting presentations. Thanks a million to everyone involved; I'll definitely be back!

Now for the highlights, starting with the ultimate catnip for the differently attentive: running two presentations *in parallel on the same screen* with the soundtrack distributed via headphones. I've never seen anything like that, and while it looked weird (I have no idea how the presenters took it), it turned out to be very useful, as you could easily tune out AI-washing presentations and switch to something more interesting. On the other hand, you could be faced with a hard choice of having to select one of two excellent presentations:
<!--more-->
{{<figure src="/2026/04/itnog-parallels.jpeg" caption="Steve Jones and Christian Adell competing for audience's attention">}}

I was thus forced to miss some of the presentations; these are the ones I enjoyed most[^WAL]:

[^WAL]: I will add links to the slides if the materials get published. I don't think they were recorded.

**National Layer-2 wholesale FWA leveraging VxLAN** -- Christian Biasibetti persuaded ASIC vendors to include VXLAN silicon in 5G-to-Ethernet chips and device vendors to use that feature, allowing his company to build a layer-2-over-5G service using VXLAN.

**Security Functions in EVPN/VXLAN Using Group-Based Policy** -- Did you know that there's an RFC that allows you to use 16 bits in the VXLAN header as a *security group* and add a BGP community to EVPN routes to automatically map EVPN destinations to those security groups? Nicola Modena explained how the technology works and how you can use this barely-known function to implement microsegmentation and service insertion.

**Transforming BGP operations to serve the best prefix out of 26 million** -- Alessandro D'Eliseo explained how his company optimized end-to-end routing using BGP AddPath and BGP Optimal Route Reflection functionality (as suggested by [Nicola Modena's presentation from 2022](/2022/05/modern-bgp-design-addpath-orr/)), combined with [BGP RIB sharding, update threading](/2021/11/multi-threaded-routing-daemons/), and prefix prioritization for faster information dissemination. Their route reflectors (running as VMs on decent hardware[^NVC]) currently handle 26 million paths.

[^NVC]: Because no vendor would pay as much for a CPU they put in their 100K$ box.

**Hollow Core Fibre** by Steve Jones was an intriguing introduction into the world of carrying light in the void between the fibers, resulting in 30% reduced latency, reduced signal loss, and significantly higher power budgets. The gotchas: limited availability and high cost, but one can hope that the economies of scale will kick in.

**AS/IXP Traffic Observability** by Luca Deri (author of *ntopng* and a guest on the [Software Gone Wild podcast](https://blog.ipspace.net/2015/04/ntopng-deep-dive-with-luca-deri-on/)) was an nice overview of new *ntopng* features, including BGP integration and the web interface. The screenshots looked almost like I'd be watching a [Kentik presentation](https://blog.ipspace.net/2017/09/nfd16-first-impressions/)[^AFK].

[^AFK]: Avi Freedman from Kentik was also a guest on [Software Gone Wild](https://blog.ipspace.net/2020/12/streaming-telemetry-software-gone-wild/).

I'm positive the **Network Automation Framework** presentation by Christian Adell and Damien Garros[^DG] was also great, but unfortunately, I had to choose between that or *void in the fiber*, and the futuristic title won.

[^DG]: Another [Software Gone Wild guest](https://blog.ipspace.net/2026/01/infrahub-damien-garros/) ;) and a [speaker](https://www.ipspace.net/Building_Network_Automation_Solutions#DS19) in ipSpace.net network automation course.

Now for a pair of minor drawbacks:

* Most of the presentations were in Italian. Fortunately, my 1K-day streak on Duolingo paid its dividends, and I was able to follow most of them (at least when the slides were in English). Definitely something to consider if you're intrigued by ITNOG content but not fluent in Italian. But hey, Bologna is known for great food, so...
* The vendors can't resist AI-washing. The *‌SRv6 uSID for Deterministic AI Backend Networking* title says it all.

The latter annoyance was easy to fix. Most of the vendor marketing pitches were in the two-track part of the event, so it wasn't hard to ignore them ;), and you could always opt out and spend some time with an excellent espresso ;))
