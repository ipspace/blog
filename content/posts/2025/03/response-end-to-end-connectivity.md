---
title: "Response: Any-to-Any Connectivity in the Internet"
date: 2025-03-27 07:45:00+0100
tags: [ Internet ]
---
Bob left a [lengthy comment](https://blog.ipspace.net/2025/03/rise-of-nat/#2571) arguing with the (somewhat black-and-white) claims I made in the [Rise of NAT podcast](/2025/03/rise-of-nat/). Let's start with the any-to-any connectivity:

> From my young millennial point of view, the logic is reversed: it is because of NATs and firewalls that the internet became so asymmetrical (client/server) just like the Minitel was designed (yes, I am French), whereas the Internet (and later the web, although a client/server protocol, was meant for everyone to be a client and a server) was designed to be more balanced.

Let's start with the early Internet. It had no peer-to-peer applications. It connected a few large computers (mainframes) that could act as servers but also allowed terminal-based user access and thus ran per-user clients.
<!--more-->
The client/server dichotomy became more evident as we started connecting low-end machines (IBM PCs and the like) to IP networks. The low-end machines did not have enough resources to be (reasonably good) servers[^IBMAT], and once you could run applications on your personal computer and drag an email into a trash bin, terminal access quickly seemed bizarrely outmoded. Even though every device was an IP host, the split into *primarily clients* and *mostly servers* IP hosts happened without any pressure from the network side.

[^IBMAT]: [Typical personal computers in those days](https://en.wikipedia.org/wiki/IBM_Personal_Computer) had a 4.77 MHz CPU, 640 KB of RAM, and 10 MB disks. However, apart from a few niche applications like Minecraft, very few people run publicly accessible servers on laptops with 4 GHz CPUs, 16 GB of RAM, and 1TB of disk space.

Of course, we always had people running web- and SMTP servers in their basements, but they were always a tiny (but very vocal) minority.

It's also worth mentioning that all networking technologies[^IWAT] (apart from IBM SNA) available in the early 1990s used a single address space and provided any-to-any end-to-end connectivity. IP wasn't either unique or better than the others; it just happened to have a big enough address space and a global address allocation mechanism. The sacred cow of any-to-any connectivity was created primarily as an argument for the almost infinite advantage of IPv6[^RO] after we had no other option but to start using NAT.

[^IWAT]: That I was able to touch

[^RO]: IPv6 is full of sacred cows and religious opinions. For example, it took IETF over 20 years to [publish an RFC admitting that the generic extension headers don't work](https://www.rfc-editor.org/rfc/rfc9098.html). It [still refuses to acknowledge that it failed to solve IPv6 small site multihoming](https://blog.ipspace.net/2024/11/ipv6-multihoming-draft/), and people heavily influencing the development of a widespread mobile operating system are still on a [crusade against DHCPv6](https://blog.ipspace.net/2021/10/dhcpv6-matters/).

{{<long-quote>}}
At the same time, we had large country-wide DECnet networks, but their 16-bit address space inherently limited their maximum size. There were also attempts to have a global registry of Novell IPX networks, but they never got far.
{{</long-quote>}}

It's also worth noting that most residential customers didn't care at all about those technical details (as long as they could read emails and browse the web), and large organizations viewed NAT as a welcome demarcation point between internal and public networks. The only people preaching the benefits of unlimited, any-to-any connectivity were the IPv6 True Believers.

The rise of NAT was thus not an evil conspiracy by Big Tech or the cause for the client-server asymmetry. It was a pragmatic consequence of the fact that *most paying customers accessed Internet services from clients that were not also servers* while IETF was dragging its feet[^v6D], [suffering from the *not invented here* syndrome](https://datatracker.ietf.org/doc/html/rfc1752#section-8.3), and throwing all sorts of crazy ideas into the kitchen sink called IPv6 instead of reusing an already-deployed protocol as the basis for the next-generation Internet.

[^v6D]: After tons of coordination, major web properties agreed to [enable IPv6 on their websites for one day](https://en.wikipedia.org/wiki/World_IPv6_Day_and_World_IPv6_Launch_Day) in 2011, or 16 years after the [Recommendation for the IP Next Generation Protocol](https://datatracker.ietf.org/doc/html/rfc1752) RFC was published. In the next 14 years, we went from [almost zero to 45% IPv6 adoption](https://www.google.com/intl/en/ipv6/statistics.html) *in the environment in which every widespread operating system has a high-quality IPv6 stack and every browser implements happy eyeballs*.