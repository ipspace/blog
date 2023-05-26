---
date: 2008-01-10 07:35:00+01:00
tags:
- DHCP
title: DHCP Conflict between a Cisco Router and Windows DHCP Server
url: /2008/01/dhcp-conflict-between-cisco-router-and.html
---
In a response to my post [Redundant DHCP Server](https://blog.ipspace.net/2007/07/redundant-dhcp-server.html) I\'ve speculated that a Cisco router should coexist with a Windows-based DHCP server if you configure them with non-overlapping address ranges. I was wrong, Edgar Cahuana discovered that Microsoft\'s DHCP server wants to have complete control over the LAN it\'s serving and shuts down if it detects another DHCP server on the same LAN.

To make the two DHCP servers coexist, you have to disable _rogue DHCP server detection_ in Windows DHCP server.
