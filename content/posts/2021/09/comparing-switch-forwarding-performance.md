---
title: "Comparing Forwarding Performance of Data Center Switches"
date: 2021-09-06 06:34:00
tags: [ data center, switching ]
---
One of my subscribers is trying to decide whether to buy an -EX or an -FX version of a Cisco Nexus data center switch:

> I was comparing [Cisco Nexus 93180YC-FX](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742284.html) and [Nexus 93180YC-EX](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742283.html). They have the same port distribution (48x 10/25G + 6x40/100G), 3.6 Tbps switching capacity, but the -FX version has just 1200 Mpps forwarding rate while EX version goes up to 2600 Mpps. What could be the reason for the difference in forwarding performance?

Both switches are single-ASIC switches. They have the same total switching bandwidth, thus it must take longer for the FX switch to forward a packet, resulting in reduced packet-per-seconds figure. It looks like the ASIC in the -FX switch is configured in more complex way: more functionality results in more complexity which results in either reduced performance or higher cost.
<!--more-->

> I don’t know if that means that the -FX variant can not give all the bandwidth to all ports at the same time, or if it is not a non-blocking switch.

Whether a switch is non-blocking switch depends on internal architecture (whatever “non-blocking” means for a single-ASIC design). Can it saturate all links? Most probably it can assuming the forwarded packets are big enough. For more details, see _[Does Small Packet Forwarding Performance Matter in Data Center Switches?](/2021/05/small-packet-forwarding-performance.html)_ and follow the links.

[Lukas Krattiger](https://www.ipspace.net/Author:Lukas_Krattiger) confirmed the numbers and did the math for me:

> The minimum packet size for line rate is close to each other (EX = 72, FX = 166) and the bandwidth of the ASIC is the same.

I would love to see an environment generating over a billion 100-byte packets per second *on a single switch*[^1]. However, my reader was still worried:

[^1]: And as often as I'm mentioning it, there are still no takers.

> How can I be sure that the -FX forwarding rate is high enough for me?

Using the golden rule of good design -- **Know Your Requirements**:

* Figure out how much traffic you have in your data center (total bandwidth and packets-per-second). It’s as easy as collecting port statistics over a reasonable period of time.
* Figure out how much traffic you could realistically get in a few years, or multiply existing traffic by whatever fudge factor you feel comfortable.
* Check whether the hardware you’re planning to buy supports that much traffic.

Unless you're doing something very specific, you'll probably find that most modern data center switches easily handle an order of magnitude more than what you could reasonably need.
