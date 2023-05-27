---
date: 2023-05-27 08:53:00
index: true
kb_section: NTP
minimal_sidebar: true
title: "Network Time Protocol (NTP) In a Nutshell"
toc_title: Overview
url: /kb/Internet/NTP/
tags: [ NTP ]
---
The importance of having accurate time on distributed servers (and even personal workstations) has been recognized long time ago by the IT managers, but it hasn’t been applied consistently to the networking devices. In this article, I’ll describe the importance of time synchronization for networking devices, the basics of Network Time Protocol (NTP) that is commonly used to synchronize IP hosts and routers, how to use it on Cisco routers and IOS-based switches and how to implement it in a highly scalable way.
<!--more-->
{{<note info>}}This article was written in 2008, and has been cleaned up and republished on ipSpace.net in 2023.{{</note>}}

## The Need for Accurate Time

Years ago, the only environment where people would care about accurate time on their networking gear would be academic environments (in many cases simply because it’s fun having very precise time on the device that should do nothing more than forward IP packets), but the introduction of encryption-based Virtual Private Networks (VPNs) implemented with IPSec and the [public key infrastructure (PKI) based on X.509 certificates](http://en.wikipedia.org/wiki/X.509) required that all certificate users (including routers and VPN concentrators) have approximately correct time (all X.509 certificates have embedded timestamps defining certificates’ validity). This requirement was easily met on high-end routers that have internal real-time clock backed up with a battery. The low-end routers (for example, the 800-series routers) are a different story; unless you synchronize them to an external time source after the reload, they will not establish a VPN tunnel.

The PKI certificates require time that is accurate to a few hours. On the other hand, if you want to perform a distributed analysis of events happening in your network (for example, break-ins, denial-of-service attacks or routing instabilities) or correlate logging printouts [stored locally on various devices](http://ioshints.blogspot.com/2007/09/logging-to-flash-disk.html), the devices participating in the analysis have to be almost perfectly synchronized.

{{<note info>}}Even if you have the most accurate time on your routers, it won’t be very helpful unless you use it in syslog messages (configured with the [service timestamps](http://www.cisco.com/en/US/docs/ios/12_3/configfun/command/reference/cfr_1g07.html#wp1029551) global configuration command).{{</note>}}

Last but not least, if you decide to offload various network services to routers, you could use them as local NTP servers (together with being DHCP- and [DNS proxy servers](/2006/08/using-router-as-dns-proxy-server.html)).
