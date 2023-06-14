---
title: "When a Device Without an IP Address Wants to Play the IP Game"
date: 2023-06-20 06:41:00
tags: [ IP routing ]
---
After I published the [Source IP Address in Multicast Packets](/2023/06/multicast-source-address.html) blog post, [Erik Auerswald](https://www.linkedin.com/in/erik-auerswald-2b8b73171) sent me several examples of network devices sending IP packets with source IP address set to 0.0.0.0:

* Cisco wireless access points [using 0.0.0.0 as the source IP address in IGMP queries](https://extremeportal.force.com/ExtrArticleDetail?an=000111647).
* Extreme (formerly Avaya) switches sending IGMP queries with source IP address 0.0.0.0 on VLANs on which they have no IP address.
<!--more-->
There's also the infamous case of switches configured with EVPN proxy ARP functionality but without a usable IP address. Those switches send ARP requests with source IP address 0.0.0.0 when trying to validate cached ARP entries, confusing Windows hosts acquiring their IP address via DHCP -- ARP requests sent from IP address 0.0.0.0 are used early in DHCP address acquisition process to allow DHCP clients to detect duplicate IPv4 addresses.

The root cause of all these SNAFUs: a network device allows you to configure IP functionality on interfaces without usable IP addresses. I wouldn't be surprised if those devices use whatever value is in the "interface IP address" field without checking it's not zero. Or as Erik concluded in his email:

> What I see as problematic is that all of the above often just works, so vendors have no motivation to find a clean solution.  Sometimes something breaks in unexpected ways, and one starts to wonder how anything could have worked before.

Even worse, sometimes vendors publish a _knowledge base_ article telling you how to configure _other vendor's gear_ to tolerate their stupidity. [Static ARP entries for Microsoft NLB](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-network-to-support-nlb-operation-mode) immediately come to mind as does [this VMware mastepiece](https://kb.vmware.com/s/article/1003804).
