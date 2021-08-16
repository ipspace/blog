---
title: "Comparing Forwarding Performance of Data Center Switches"
date: 2021-09-25 06:34:00
tags: [ data center, switching ]
draft: True
---
One of my subscribers is trying to decide whether to buy an -EX or an -FX version of a Cisco Nexus data center switch:

> I was comparing Cisco Nexus 93180YC-FX and Nexus 93180YC-EX. They have the same port distribution (48x 10/25G + 6x40/100G), 3.6 Tbps switching capacity, but FX version just 1200 Mpps Forwarding rate while EX version goes up to 2600 Mpps. What could be the reason for the difference in forwarding performance?

Assuming both switches use a non-blocking architecture, they must have the same total switching bandwidth, thus it must take longer for the FX switch to forward a packet, resulting in reduced packet-per-seconds figure. Either Cisco is using a different ASIC in the -FX switches, or they have the same ASIC configured in more complex way.
<!--more-->
As always, more functionality results in more complexity which results in either reduced performance or higher cost.

> I don’t know if that means that the -FX variant can not give all the bandwidth to all ports at the same time, or if it is not a non-blocking switch.

Whether it’s non-blocking switch depends on internal architecture (whatever “non-blocking” means for a single-ASIC design). Can it saturate all links? Most probably it can assuming the forwarded packets are big enough. For more details, see _[Does Small Packet Forwarding Performance Matter in Data Center Switches?](https://blog.ipspace.net/2021/05/small-packet-forwarding-performance.html)_ and follow the links.

> How can I be sure that the -FX forwarding rate is high enough for me?

Using the golden rule of good design -- **Know Your Requirements**:

* Figure out how much traffic you have in your data center (total bandwidth and packets-per-second). It’s as easy as collecting port statistics over a reasonable period of time.
* Figure out how much traffic you could realistically get in a few years, or multiply existing traffic by whatever factor you feel comfortable.
* Check whether the hardware you’re planning to buy supports that much traffic.

Unless you're doing something very specific, you'll probably find that most modern data center switches easily handle an order of magnitude more than what you could reasonably need.
