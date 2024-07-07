---
date: 2019-03-20 10:03:00+01:00
tags:
- SD-WAN
- SDN
title: 'Lock-In and SD-WAN: a Match Made in Heaven'
url: /2019/03/lock-in-and-sd-wan-match-made-in-heaven/
sd-wan_tag: myth
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

I made a statement along these lines in an SD-WAN blog post and related email sent to our [SDN and Network Automation mailing list](https://www.ipspace.net/Subscribe/Five_SDN_Tips):

> The architecture of most SD-WAN products is thus much cleaner and easier to configure than traditional hybrid networks. However, do keep in mind that most of them use proprietary protocols, resulting in a perfect lock-in.

While reading that one of my readers sent me a nice email with an interesting question:
<!--more-->
> Do you think that a lock-in regarding a specific company is only based on technology? Do you think that a suboptimal technology solution would trigger an introduction of a new vendor? My feeling is that the lock-in is not forced by technology solutions but more relationship oriented.

Obviously, there are all sorts of lock-ins, from contractual, relationship, CYA (nobody was ever fired for buying \$vendor), religious (in \$vendor we trust), philosophical (I buy from \$vendor, therefore I am :D)...

However, being primarily an engineer, I prefer to focus on the technology lock-in (while keeping in mind that technology is nothing more than means to an end). Let's compare a more traditional hybrid WAN architecture implemented with routers or firewalls to the wonderful new world of SD-WAN.

Traditional hybrid WANs are implemented on multi-purpose devices and use standardized protocols. You can troubleshoot them with off-the-shelf tools (Wireshark...) and even connect third party devices to the same network although with reduced functionality (example: P2P IPsec instead of DMVPN).

All SD-WAN solutions I've seen so far (apart from Cisco's IWAN... but let's not start the discussion whether that one counts or not) use undocumented proprietary protocols, making it impossible to use standard troubleshooting tools, or establish WAN/VPN-side connectivity with third-party devices.

If you decide to migrate from Cisco to Fortinet (as an example), you could start deploying Fortinet at remote sites and use P2P IPsec tunnels with your central Cisco router until the traffic increases to the point where it makes sense to deploy a hub device from the same vendor. If you want to change your SD-WAN vendor, the only choice you have today is to build a parallel network.
