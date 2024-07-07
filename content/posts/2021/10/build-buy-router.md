---
title: "Should You Build or Buy a Router?"
date: 2021-10-07 07:11:00
tags: [ SDN ]
---
[Patrik Schindler](https://www.pocnet.net/) sent me an interesting comment to my *Open-Source DMVPN Alternatives* blog post:

{{<long-quote>}}
I've done searches myself some time ago about the readymade Linux distros supporting DMVPN and [got exactly what I asked for](https://wiki.alpinelinux.org/wiki/Dynamic_Multipoint_VPN_(DMVPN)_Phase_3_with_Quagga_NHRPd).

Glancing over that page appalled me: Different stuff with different configuration languages, probably the need to restart things, thus generating service outages for configuration changes...  

Your blog is heavily biased towards big deployments with good opportunities for automation, and the diversity of different components can be easily hidden behind automation scripts of choice. Smaller deployments are almost never being able to compensate the initial overhead of creating all the automation fuzz, and from that perspective, I must admit that configuring a Cisco router feels way more smooth to me. 
{{</long-quote>}}

Welcome to the *[build-or-buy](/2020/12/video-build-or-buy/)* dilemma, router edition. 
<!--more-->
**TL&DR**: Unless you have a very special use case, it's probably easier and cheaper (in the long run) to buy a router than to try to build it from open-source components.

As always, there are numerous reasons why one might want to build a solution instead of buying it. The reasonable ones first:

* **You can't get what you need**. In most cases, that means you should go back to the drawing board and rethink your requirements. You're often not as special as you think you are.
* **You want an extensible solution** and you can only buy black boxes. As with the previous bullet, it's worth rethinking your requirements, and looking around a bit more. Admittedly, the router products are not as extension-friendly as the data center switching products, but if you're looking for high speeds, a deep buffer data center switch might be just what you need[^1], and on the low-end you might want to look at OpenWRT (unless you want a [supported product with a severe case of featuritis](/2018/12/can-i-replace-commercial-load-balancer/)).
* **You want to build all elements of what you think is your core competence**. Wake up. [You're not Google](/2016/03/you-want-your-network-to-be-like/), AWS, Facebook, Azure, or LinkedIn. Find an extensible solution that fits your needs and go from there. On a more serious note, master [Wardley maps](https://en.wikipedia.org/wiki/Wardley_map) and figure out which elements of your supposed core competence are commoditized and where it makes sense to add value by building stuff.
* **It's cheaper to build than to buy**. In most cases, this is a fallacy based on incomplete information, and ignoring *time value of money* and *ongoing operations expenses*. Switching and IP routing are getting commoditized; while there might be environments big enough to justify building your own stuff, there's a 99% chance you're in the *rest of the world* category.

[^1]: Assuming you're interested in simple high-speed services. The moment you want to squeeze every feature ever invented into a provider edge device, all bets are off, and you'll pay dearly for the privilege. For more details, listen to the _[SDN Internet Router Is in Production](/2015/10/sdn-internet-router-is-in-production-on/)_ podcast with David Barroso.

Then there are less objective reasons that I will refrain from commenting on:

* It's a hobby project, and you love tinkering.
* You always wanted to build stuff, and getting your employer to pay for it is an unexpected bonus.
* You want to prove a point.
* You want to pad your resume.
* You know best.

I should also mention that there's a bit of a difference between building your own automation scripts and your own networking device. You can run your automation script on any compute platform (hopefully a VM or a container); when you decide to build your own hardware device you have to understand the whole stack, from environmental requirements to real-time packet forwarding and the control-plane software running on the device. 

In any case, should you decide to build something, keep in mind that someone will have to support it for the foreseeable future (or longer: a quick search seems to indicate COBOL developers are paid almost as much as CCIEs).

I described some of the considerations in more details in the _[Does It Make Sense to Build Your Own Networking Solutions?](/2016/06/does-it-make-sense-to-build-your-own/)_ blog post; you might also want to listen to [Giacomo Bernardi describing how Eolo built their own service provider gear](/2016/06/build-your-own-service-provider-gear-on/).
