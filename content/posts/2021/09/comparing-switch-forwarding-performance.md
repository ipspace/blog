---
title: "Comparing Forwarding Performance of Data Center Switches"
date: 2021-09-06 06:34:00
tags: [ data center, switching ]
---
One of my subscribers is trying to decide whether to buy an -EX or an -FX version of a Cisco Nexus data center switch:

> I was comparing [Cisco Nexus 93180YC-FX](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742284.html) and [Nexus 93180YC-EX](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742283.html). They have the same port distribution (48x 10/25G + 6x40/100G), 3.6 Tbps switching capacity, but the -FX version has just 1200 Mpps forwarding rate while EX version goes up to 2600 Mpps. What could be the reason for the difference in forwarding performance?

My first thought was "*the FX-series must use a different ASIC or more complex packet lookups, resulting in reduced forwarding performace*, but [Lukas Krattiger](https://www.ipspace.net/Author:Lukas_Krattiger) quickly set me straight:
<!--more-->
> The -EX and -FX actually have the same bandwidth and close to the same PPS (there must be a typo in the datasheet). The -EX has a slightly higher PPS as line rate is at a lower packetsize vs. -FX but it is “marginal” I would say. If I remember correctly, we talk about 2.6Bpps with -EX, and 2.4Bpps with -FX.

The obvious (non-existent, as it turns out) discrepancy in forwarding performance worried my subscriber:

> I don’t know if that means that the -FX variant can not give all the bandwidth to all ports at the same time, or if it is not a non-blocking switch.

Most modern high-end single-ASIC architectures are linerate and non-blocking (whatever “non-blocking” means for a single-ASIC design), and can saturate all the links... at least at large enough packet sizes. For more details, see _[Does Small Packet Forwarding Performance Matter in Data Center Switches?](https://blog.ipspace.net/2021/05/small-packet-forwarding-performance.html)_ and follow the links.

> How can I be sure that the -FX forwarding rate is high enough for me?

Using the golden rule of good design -- **Know Your Requirements**:

* Figure out how much traffic you have in your data center (total bandwidth and packets-per-second). It’s as easy as collecting port statistics over a reasonable period of time.
* Figure out how much traffic you could realistically get in a few years, or multiply existing traffic by whatever fudge factor you feel comfortable.
* Check whether the hardware you’re planning to buy supports that much traffic.

Unless you're doing something very specific, you'll probably find that most modern data center switches easily handle an order of magnitude more than what you could reasonably need.
