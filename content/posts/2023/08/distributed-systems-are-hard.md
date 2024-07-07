---
title: "How GitHub Learned How Hard Distributed Systems Are"
date: 2023-08-23 05:55:00
tags: [ high availability, worth reading ]
high-availability_tag: outage
---
[Anne Baretta](https://www.linkedin.com/in/abaretta/) found a [great video describing the October 2018 GitHub failure](https://www.youtube.com/watch?v=dsHyUgGMht0). Here's the TL&DW:

* The failure was caused by a short (~ 1 minute) disconnect of the primary data center
* The database replicas failed over to the secondary data center, but that failover was never tested and of course some stuff didn't work.
* In the meantime, batch jobs modified data in the primary data center, making the two replicas out-of-sync.
* It took them over 24 hours to clean up the mess.
<!--more-->
You REALLY SHOULD watch the video -- it nicely proves two points I've been making for ages (not that anyone would listen):

* [Distributed systems](/series/distributed-systems/) are hard. Making them [highly available](/tag/high-availability/) is even harder.
* A [Disaster Recovery Plan is just wishful thinking](/series/dr/) until it has been thoroughly tested under realistic conditions.
