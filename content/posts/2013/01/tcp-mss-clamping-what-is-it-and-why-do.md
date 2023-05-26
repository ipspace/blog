---
date: 2013-01-22 06:50:00+01:00
tags:
- IP services
- PPP
title: TCP MSS Clamping – What Is It and Why Do We Need It?
url: /2013/01/tcp-mss-clamping-what-is-it-and-why-do.html
---
This (not so very) short video explains what TCP MSS clamping is and why we're almost forced to use it on xDSL (PPPoE) and tunnel interfaces.

**TL&DW summary**: because Internet-wide Path MTU Discovery rarely works.

{{<video "https://www.ipspace.net/nuggets/podcast/X1%20TCP%20MSS%20Clamping.mp4">}}
<!--more-->
### More details

-   [Path MTU discovery](http://en.wikipedia.org/wiki/Path_MTU_Discovery) was first defined in [RFC 1191](http://www.ietf.org/rfc/rfc1191.txt) (yeah, it's THAT old and still doesn't work well);
-   You'll find more PMTUD and fragmentation hands-on details in my [Never-Ending Story of IP Fragmentation](/kb/Internet/PMTUD/) article;
-   [Packetization Layer Path MTU Discovery](http://tools.ietf.org/html/rfc4821) (RFC 4821) is an alternate approach that does not rely on ICMP replies;
-   [Discovering Path MTU black holes](https://ripe65.ripe.net/presentations/100-RP2_presentation_RIPE65.pdf) presentation from RIPE65 ([video](https://ripe65.ripe.net/archives/video/58/)).

### Some configuration tips

-   TCP MSS clamping can be configured on [end hosts](http://tldp.org/HOWTO/IP-Masquerade-HOWTO/mtu-issues.html) or on some routers (on Cisco IOS, use **ip tcp adjust-mss** interface configuration command).
-   The **ip tcp adjust-mss** functionality on Cisco IOS is bidirectional -- MSS option is adjusted in inbound and outbound TCP SYN packets traversing the interface on which **ip tcp adjust-mss** is configured.
-   You should configure **ip tcp adjust-mss** on interfaces with low MTUs. In other words, MSS value configured on an interface should match MTU value of the same interface minus 40 bytes.
-   [Configuration examples](http://www.cisco.com/en/US/tech/tk175/tk15/technologies_configuration_example09186a008071a6c3.shtml) where **ip tcp adjust-mss** is configured on Ethernet interface have interesting side effects if the router has more than two interfaces.
