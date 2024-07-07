---
date: 2018-01-19 08:20:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_86-Packet_Forwarding_on_Linux.mp3
tags:
- podcast
- scalability
- IP routing
- Software Gone Wild
- Cumulus Linux
title: Packet Forwarding on Linux on Software Gone Wild
url: /2018/01/packet-forwarding-on-linux-on-software/
---
Linux operating system is used as the foundation for numerous network operating systems including Arista EOS and Cumulus Linux. It provides most networking constructs we grew familiar with including interfaces, VLANs, routing tables, VRFs and contexts, but they behave slightly differently from what we're used to.

In [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild) [Episode 86](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_86-Packet_Forwarding_on_Linux.mp3) Roopa Prabhu and David Ahern explained the fundamentals of packet forwarding on Linux, and the differences between Linux and more traditional network operating systems.
<!--more-->
We started with the easy question \"*why does Cumulus care about the performance of software packet forwarding on Linux*," and continued with a long list of interesting topics:

-   Why should the control-plane processes use Linux data structures and not bypass them using things like OVSDB?
-   What is NetLink API and how is it used by Cumulus hardware drivers?
-   What is SwitchDev API and why is it becoming popular?
-   Where are routing and forwarding tables stored on Linux?
-   Why would you want to have multiple routing tables on a Linux box?
-   How could you use those routing tables to implement VRFs and why was it traditionally so hard to do?
-   How did Cumulus change the behavior of Linux routing tables to make VRFs simpler to use?
-   What scaling problems would you hit when trying to implement VRFs with Linux routing tables, and how did Cumulus engineers solve them?
-   How is route leaking between VRFs implemented on Linux?
-   What are Linux namespaces and why are they not the right mechanism to implement VRFs?

For more details [listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_86-Packet_Forwarding_on_Linux.mp3) and read the [VRF for Linux](https://cumulusnetworks.com/blog/vrf-for-linux/) blog post by David Ahern.
