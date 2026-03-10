---
title: "Dynamic Path MTU Discovery in Cloudflare One Client"
date: 2026-03-11 08:14:00+0100
tags: [ worth reading, VPN ]
---
Here's an interesting tidbit from the *what took them so long* department: [Cloudflare One Client continuously measures end-to-end MTU](https://blog.cloudflare.com/client-dynamic-path-mtu-discovery/) and adjusts the local tunnel interface MTU size accordingly (warning: there's a fair amount of dubious handwaving over the interesting details), generating ICMP packet-too-big messages as close to the source as possible.

I managed to avoid VPN clients most of my life, so I have no idea whether this is a "*finally someone figured that out* 🎉" moment or a late catch-up to what other VPN clients have been doing for ages. Feedback (in comments or otherwise) would be most welcome!
