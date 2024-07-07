---
date: 2016-01-26 07:43:00+01:00
tags:
- IPv6
- data center
title: Disabling SLAAC in Data Center Subnets
url: /2016/01/disabling-slaac-in-data-center-subnets/
---
Continuing the IPv6 address selection discussion we have a few days ago, Luka Manojlovič sent me a seemingly workable proposal:

> I think we were discussing a borderline problem. In a server environment there won't be any SLAAC, and we could turn off DHCPv6 client on servers with fixed IP addresses.

Sounds great, but as always, the reality tends to be a bit harsher.
<!--more-->
The crucial question is: can you turn off [*autoconfiguration* flag](/2012/11/ipv6-router-advertisements-deep-dive/) in individual prefixes advertised in RA messages? As always, the answer is *it depends*.

I checked latest configuration guides from Cisco (Nexus 9300), Juniper (QFX5200, Junos release 15.1), Arista (EOS 14.5) and HP (5900 switches). All these switches allow you to configure flags on every single prefix advertised in router advertisement... apart from QFX5200 where it seems like you can't do a thing (even though [RA twiddling was available before Junos version 7.4](http://www.juniper.net/techpubs/en_US/junos15.1/topics/reference/configuration-statement/autonomous-edit-protocols-router-advertisement.html) on MX-series routers).

**Moral of the story**: do a thorough check of how well your vendor supports obscure IPv6 features that might become crucial in your IPv6 deployment.

As always, there's an alternative: [disable RA processing on Windows servers](http://www.excaliburtech.net/archives/192), and use static default routing and [IPv6 VRRP](/2012/12/do-we-need-fhrp-hsrp-or-vrrp-for-ipv6/). Welcome back to the 90s.

[![](/2016/01/s320-3977613.jpg)](/2016/01/s1600-3977613.jpg)
