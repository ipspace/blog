---
title: "External Links on Spine Switches"
date: 2023-03-21 07:18:00
tags: [ fabric, design ]
---
A networking engineer attending the [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course asked this question:

> What is the best practice to connect DC fabric to outside world assuming there are 2 spine switches in the fabric and EVPN VXLAN is used as overlay? Is it a good idea to introduce edge (border) switches, or it is better to connect outside world directly to the spine?

As always, the answer is "_it depends_," this time based on:
<!--more-->
* **Number of spine nodes**. If you want to retain the perfect load balancing across spines, then the external links should be connected across all spines. That's not a big deal if you have two spines, but if you ever expand to four spines you have to decide what you want to do. However, if you have an order of magnitude more bandwidth inside the fabric than toward the external world then this obviously doesn’t matter
* **Interface speeds**. Spines usually have higher-speed interfaces, so you might not be able to connect your WAN edge equipment to those interfaces. Even if that works, you’d be wasting several expensive interfaces, but that might still be better than buying two extra switches.
* **Packet forwarding features**. Juniper was the only vendor (I'm aware of) that thought [it makes sense to have complex high-speed (expensive) ASICs in the spine switches](/2022/06/beware-vendors-bringing-whitepapers.html). Most ASIC vendors [have high-speed ASICs with simple packet forwarding and lower-speed ASICs with complex forwarding behavior](/2022/06/data-center-switching-asic-tradeoffs.html). For example, spine switches based on Broadcom Tomahawk cannot do VXLAN routing without packet recirculation.
* **Required buffer space**. Switches connected to the WAN edge have to deal with significant incast (many sources sending WAN traffic) and speed disparity (traffic going from high-speed core links to low-speed edge links), which usually [results in higher buffer requirements](/2021/11/router-switch-hardware.html). Spine switches usually have relatively smaller buffers, unless you’re buying QFX10Ks from Juniper.

Want a rule-of-thumb[^BP]? In most cases it's better to connect external links to a dedicated pair of leaf switches (assuming you can afford them), and connect network services (firewalls, load balancers...) and maybe even storage ([which might require bigger buffers](/2021/05/packet-bursts-data-center-networks.html)) to the same switches. Buying complex spine switches with large buffers is usually an exercise in wasting money.

[^BP]: Also known as _best practice_

### More Information

We covered this dilemma somewhere in the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar, probably as part of [multi-pod and multi-site fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE), but I can't remember whether it was part of the materials or an answer to an attendee's question.
