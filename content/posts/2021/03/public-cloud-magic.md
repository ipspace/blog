---
title: "Public Cloud Behind-the-Scenes Magic"
date: 2021-03-18 07:27:00
tags: [ cloud ]
---
One of my subscribers sent me this question after watching the [networking part](https://my.ipspace.net/bin/list?id=Cloud101#NET) of *[Introduction to Cloud Computing](https://www.ipspace.net/Introduction_to_Cloud_Computing)* webinar:

> Does anyone know what secret networking magic the Cloud providers are doing deep in their fabrics which are not exposed to consumers of their services?

**TL&DR**: Of course not... and I'm guessing it would be pretty expensive if I knew and told you.

However, one can always guess based on what can be observed (see also: [AWS networking 101](/2020/05/aws-networking-101/), [Azure networking 101](/2020/05/azure-networking-101/)).
<!--more-->
* They must be using overlay virtual networking to implement virtual networks. Nothing else would scale to what they need -- scalability numbers achieved by products like Cisco ACI are laughable from a hyperscaler perspective.
* It must be either complex enough or large enough not to be implementable on ToR switches.
* AWS is the only one of the big three to offer bare-metal servers, and we [know their magic runs in their smart NICs](/2020/06/cloud-networking-architectures/) (as Pensando so proudly points out like it [would validate their business model](/2020/09/need-smart-nic/)). Azure seems to be using FPGAs, and Google relied on a software solution.

For more details see:

* [Azure accelerated networking](https://blog.acolyer.org/2018/05/01/azure-accelerated-networking-smartnics-in-the-public-cloud/)
* [Andromeda: performance, isolation, and velocity at scale in cloud network virtualization](https://blog.acolyer.org/2018/05/02/andromeda-performance-isolation-and-velocity-at-scale-in-cloud-network-virtualization/)

Network load balancing and Internet-facing NAT are truly interesting. Microsoft [wrote a paper](https://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p207.pdf) describing an early implementation of their Network Load Balancer, and it's reasonably easy to envision how the same approach could be used for NAT. I'm positive AWS is doing something similar.

See also:

* [Maglev: A Fast and Reliable Software Network Load Balancer](https://blog.acolyer.org/2016/03/21/maglev-a-fast-and-reliable-software-network-load-balancer/)
* [Stateless datacenter load-balancing with Beamer](https://blog.acolyer.org/2018/05/03/stateless-datacenter-load-balancing-with-beamer/)

While you could solve load balancing with a proper combination of worker nodes and hypervisor tricks, I'm positive other complex networking services like AWS Transit Gateway run on top of the virtual networking (like virtual machines), but in multi-tenant bare-metal instances. For an overview of this idea, see [*Real Virtual Routers* used in Oracle Cloud](https://blogs.oracle.com/cloud-infrastructure/first-principles-l2-network-virtualization-for-lift-and-shift).

It seems like most everything else runs in managed VMs. It's pretty obvious Azure application load balancing is implemented with virtual machines and a Network Load Balancer sitting in front of them, VPN gateways are supposedly Windows servers (that's why it took 30 minutes to provision one), and even their recently introduced Route Server is just two managed VMs, probably with somewhat-privileged access to the orchestration system. AWS and Google are probably using similar approaches, or they could be using multi-tenant bare metal servers for efficiency reasons... but do you really care about implementation costs if you charge them to the customer?

Anything else? Would appreciate comments with links to insightful papers.
