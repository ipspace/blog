---
title: "Understanding Linux Networking"
date: 2020-09-28 06:27:00
tags: [ switching, training ]
---
Got this interesting question from one of my readers

> Based on my experience, the documentation regarding Linux networking is either elementary man pages for user-space utilities or [very complicated Linux kernel source code](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/net/ipv4/). Does getting deep into Linux networking mean reading source code?

It all depends on how deep you plan to go:
<!--more-->
**Deploying whitebox switches**. If you're just starting you SHOULD buy a supported solution that includes hardware and a variant of Linux running on it. Your problem transformed into "configuring control-plane protocols on Linux". Congratulations, you'll be perfectly fine studying Cumulus Networks documentation. Apart from the secret-sauce-ASIC-blob they're using open-source software, so whatever you learn there should be transferrable to any other Linux networking environment.

{{<note>}}I'm hearing rumors that Broadcom is not exactly happy with Mellanox/Nvidia snapping up Cumulus. It might be that the best chance of having a documented open-source network operating system just transmogrified into another dead-end.{{</note>}}

However, even though the documentation is pretty good, expect a few gotchas. As [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt) told me:

* Unlike a traditional NOS, Linux is not a monolithic entity. There's the kernel and there are software packages than run on top. To make installation and management easier, different folks put together different Linux distributions, and each of them might have different configuration mechanisms.
* Configuring Linux networking consists of configuring different parts: interfaces and everything else. You can manually configure MACs, routes and such, but this distinction between interfaces and the rest is common.
* How you configure interfaces and how you configure the rest depends on the software and Linux distribution you use.

**Low-speed network device running on Linux**. You can use Linux-based solutions to implement a router (there's a reasonable chance your home router is already doing it), a firewall, or a load balancer (all high-volume web properties and CDNs run on Linux-based load balancers). As long as you're OK with out-of-the-box performance configure interfaces (see above for caveats), populate the routing table, order a margarita, and enjoy the sunset.

Out-of-the-box performance obviously depends on CPU speed, whether the device performs packet forwarding or TCP session termination (where you can use NIC TCP offload to speed things up), and whether you plan to use multiple cores to get the job done. Vanilla Linux is not exactly a stellar platform when it comes to multi-core packet forwarding. Just saying...

**High speed packet forwarding on Linux**. Hopefully you bought a shrink-wrapped product that includes a high-speed packet forwarding solution and tons of documentation.

No? You thought you could hack it together based on what you heard about BPF/XDP/...? I wish you luck, but do keep in mind that you're in the uncharted "here be dragons" land of unicorns where (according to [immortal words of Artur Bergman](https://www.youtube.com/watch?v=oebqlzblfyo)) we run on a stack built on shit, and each relevant parameter is only mentioned twice: when a patch is submitted to Linux Git repository, and when that patch is applied. Given enough effort, you might master the details, and people like [CloudFlare engineers](https://blog.cloudflare.com/) or [Andree Toonk](https://toonk.io/) write detailed blog post that should help you get started (you can also [explore Snabb Switch](https://snabbco.github.io/)), but [expect a lot of frustration along the way](/2020/09/need-smart-nic/#122).

{{<note>}}Using a more productized solution like PF_RING or DPDK is probably a bit less stressful, but I have no hands-on experience with either of them. If you do, please share it in the comments.{{</note>}}

Will the situation ever get better? Don't expect miracles. A lot of people developing high-performance stuff do it to solve their business problems, and while they are super-interested in submitting their work back to mainstream Linux code (so they don't have to deal with out-of-sync forks), they have little motivation to document or productize it.

However, even in the unicorn land things are getting better. Here's what [Thomas Graf](https://www.linkedin.com/in/thomas-graf-73104547/) (Linux networking guru, founder of Cilium, and a guest on our podcast) sent me when I asked him about his view on high-speed Linux networking:

---

I wouldn't call it unicorn land anymore even though eBPF is a 
technology that shouldn't be directly leveraged unless you are a 
unicorn whisperer. That said, the eBPF power users have been open sourcing their efforts with eBPF so there are several good options to experience the power of eBPF without having to use it directly. 

One is obviously **Cilium** which has recently been adopted by Google for GKE and Anthos[^0] to drive networking, load balancing (E/W and N/S), network security and network visibility. Google is clearly seeing the future as eBPF, and interestingly less in the green field cloud environment but in the on-premises k8s enterprise segment with complex legacy requirements. 

We are also integrated into environments like Adobe, Palantir, Datadog, Sky Betting, PostFinance, and many more, so we are definitely past the stage of cloud native unicorn tamers. That said, we also clearly still have unicorn level users that push their implementation on top of Cilium in a PR to contribute it back to the community. 

Another good example is **Katran**, the load balancer used by Facebook based on eBPF/XDP. Most of this functionality is now also available in Cilium; Katran is more opinioned and more tailored to the Facebook network model so a lot closer to the unicorn land. 

The third option I point out is **Cloudflare**, they are primarily open sourcing tooling they used, and not the actual dataplane, but they have been building all QoS and DDoS mitigation for their CDN. 

Lastly, we are at the point where the current old-school CNI leader **Calico** has been forced to invest into eBPF to try and stay relevant in the future. 

eBPF is clearly the next winner but the technology is too low-level to be used directly for the majority of users out there. Cilium and other abstractions are the right way to think about using eBPF. For a more complete list of eBPF projects, check out [https://ebpf.io](https://ebpf.io). 

[^0]: https://cloud.google.com/blog/products/containers-kubernetes/bringing-ebpf-and-cilium-to-google-kubernetes-engine 

---

Still want to use that stuff? Invest a few years in educating yourself (you didn't become a top-notch CCIE/CCDE in a week, did you?), or hire/partner with someone who did it before. Igalia comes to mind, and I'm positive there are a few other companies out there doing similar work.