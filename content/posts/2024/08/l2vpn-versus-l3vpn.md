---
title: "Repost: Why Are Layer-2 VPNs So Popular?"
date: 2024-08-27 08:35:00+0200
tags: [ VPN, bridging ]
---
[Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/) wrote a [succinct comment](https://blog.ipspace.net/2024/07/bgp-evpn-vxlan-srv6/#2341) explaining why so many customers prefer layer-2 VPNs over layer-3 VPNs:

---

The reason of L2VPN is becoming more popular by service providers and customers is about provisioning complexity.
<!--more-->
With an L3VPN usually you have to spend weeks on agreeing configuration details with your service provider. This process is very difficult to automate. With an L2VPN you just have to accept a few parameters and you can connect immediately. Even you can have a Network-as-a-Service style. The only disadvantage is to install your own edge routers to separate the service provider section from your private section.

By the way, this is where private LISP could be an easy to use alternative to private MPLS for your private WAN on top of L2VPN telco services. :-)

L2VPNs can be also automatically provisioned through a number of different service provider sections. L3VPNs are more difficult to manage over multiple service provider sections. It is doable, but not easy to automate.

The Metro Ethernet Forum has tons of specifications on the different VPN services. There you can see clearly the difference.

---

Not surprisingly, I've been [saying the same thing for ages](/2018/03/whos-pushing-layer-2-vpn-services/), including a [whole webinar describing different VPN types, their benefits, and drawbacks](https://my.ipspace.net/bin/list?id=ChooseVPN).

But wait, there's one more thing: you can access that webinar without registration. Have fun.