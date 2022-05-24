---
title: "Beware of Vendors Bringing Whitepapers"
date: 2022-06-01 06:20:00
draft: True
tags: [ switching ]
---
Here's an [interesting observation](https://blog.ipspace.net/2022/05/network-hardware-disaggregation-2022.html#1241) I got as a comment to [one of my blog posts](https://blog.ipspace.net/2022/05/network-hardware-disaggregation-2022.html) where I briefly mentioned different ASIC families:

---

[An article from Juniper](https://www.juniper.net/content/dam/www/assets/white-papers/us/en/routers/deploying-data-center-switching-solutions.pdf) I found on the web was saying quite opposite [_from what you were saying_]: Low On-Chip Memory ASIC for low buffer leafs, Large External Memory ASIC for high speed/high buffer leaf and spine.

---

Never forget Rule#2 of good network design: beware of vendors bringing whitepapers[^GBG].
<!--more-->

[^GBG]: Based on [beware of Greeks bearing gifts](https://en.wikipedia.org/wiki/Beware_of_Greeks_bearing_gifts), in particular when they look like a wooden horse.

Juniper is selling numerous switches based on Broadcom merchant silicon (QFX 5000 series), and deep buffer ([100 msec of buffers per port](https://www.juniper.net/us/en/products/switches/qfx-series/qfx10002-fixed-ethernet-switches-datasheet.html)) QFX 10000 switches using in-house silicon. The whitepaper mentioned above compares switches using Broadcom Tomahawk ASIC with switches using Juniper Q5 ASIC, and wrongly concludes that you should use Tomahawk ASIC at the edge and Q5 ASIC at the core.

Tomahawk ASIC is a pretty bad choice for a data center fabric edge -- it's missing a lot of functionality available in Broadcom Trident chipset (for example, VXLAN Routing In and Out of Tunnels).

What about deep buffer switches at the spine layer? Do you really think you need tens of milliseconds of buffer space _per port_ on a spine switch? Is that what you want the fabric latency to be?

Most everyone else agrees you _don't need deep buffers for spine switches_ ([more details](https://my.ipspace.net/bin/list?id=xBuffers)). You might need deep buffers at the network edge at points with significant incast-based congestion and orders-of-magnitude speed mismatch between high-speed ingress and low-speed egress links. WAN edge is a prime example. Storage nodes serving a high percentage of write requests might be another.

To wrap up: when a whitepaper comparing Tomahawk and Q5 ASICs is saying...

> Switching platforms based on low on-chip memory ASICs are best suited for cost-effective, high-speed, high-density server access deployments.

... they really mean:

> We want you to buy QFX10K for your spine switches, but we can't justify it any other way, so we'll claim shallow-buffer switches are only good for the network edge.
