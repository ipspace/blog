---
title: "Understanding Linux Networking"
date: 2020-09-28 06:27:00
tags: [ switching, training ]
---
Got this interesting question from one of my readers

> Based on my experience, the documentation regarding Linux networking is either elementary man pages for user-space utilities or [very complicated Linux kernel source code](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/net/ipv4/). Does getting deep into Linux networking mean reading source code?

It all depends on how deep you plan to go:

**Deploying whitebox switches**. If you're just starting you SHOULD buy a supported solution that includes hardware and a variant of Linux running on it. Your problem transformed into "configuring control-plane protocols on Linux". Congratulations, you'll be perfectly fine studying Cumulus Networks documentation. Apart from the secret-sauce-ASIC-blob they're using open-source software, so whatever you learn there should be transferrable to any other Linux networking environment.

{{<note>}}I'm hearing rumors that Broadcom is not exactly happy with Mellanox/Nvidia snapping up Cumulus. It might be that the best chance of having a documented open-source network operating system just transmogrified into another dead-end.{{</note>}}

However, even though the documentation is pretty good, expect a few gotchas. As Dinesh Dutt told me:

* Unlike a traditional NOS, Linux is not a monolithic entity. There's the kernel and there are software packages than run on top. To make installation and management easier, different folks put together different Linux distributions, and each of them might have different configuration mechanisms.
* Configuring Linux networking consists of configuring different parts: interfaces and everything else. You can manually configure MACs, routes and such, but this distinction between interfaces and the rest is common.
* How you configure interfaces and how you configure the rest depends on the software and Linux distribution you use.

**Low-speed network device running on Linux**. You can use Linux-based solutions to implement a router (there's a reasonable chance your home router is already doing it), a firewall, or a load balancer (all high-volume web properties and CDNs run on Linux-based load balancers). As long as you're OK with out-of-the-box performance configure interfaces (see above for caveats), populate the routing table, order a margarita, and enjoy the sunset.

Out-of-the-box performance obviously depends on CPU speed, whether the device performs packet forwarding or TCP session termination (where you can use NIC TCP offload to speed things up), and whether you plan to use multiple cores to get the job done. Vanilla Linux is not exactly a stellar platform when it comes to multi-core packet forwarding. Just saying...

**High speed packet forwarding on Linux**. Hopefully you bought a shrink-wrapped product that includes a high-speed packet forwarding solution and tons of documentation.

No? You thought you could hack it together based on what you heard about BPF/XDP/...? I wish you luck, but do keep in mind that you're in the uncharted "here be dragons" land of unicorns where (according to [immortal words of Artur Bergman](https://www.youtube.com/watch?v=oebqlzblfyo)) we run on a stack built on shit, and each relevant parameter is only mentioned twice: when a patch is submitted to Linux Git repository, and when that patch is applied. Given enough effort, you might master the details, and people like [CloudFlare engineers](https://blog.cloudflare.com/) or [Andree Toonk](https://toonk.io/) write detailed blog post that should help you get started (you can also [explore Snabb Switch](https://snabbco.github.io/)), but [expect a lot of frustration along the way](https://blog.ipspace.net/2020/09/need-smart-nic.html#122).

{{<note>}}Using a more productized solution like PF_RING or DPDK is probably a bit less stressful, but I have no hands-on experience with either of them. If you do, please share it in the comments.{{</note>}}

Will the situation ever get better? Don't expect miracles. A lot of people developing high-performance stuff do it to solve their business problems, and while they are super-interested in submitting their work back to mainstream Linux code (so they don't have to deal with out-of-sync forks), they have little motivation to document or productize it.

Still want to use that stuff? Invest a few years in educating yourself (you didn't become a top-notch CCIE/CCDE in a week, did you?), or hire/partner with someone who did it before. Igalia comes to mind, and I'm positive there are a few other companies out there doing similar work.