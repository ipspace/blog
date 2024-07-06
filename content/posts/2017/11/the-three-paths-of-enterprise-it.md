---
date: 2017-11-06 09:35:00+01:00
lastmod: 2022-12-15 10:07:11
tags:
- design
- cloud
title: The Three Paths of Enterprise IT
url: /2017/11/the-three-paths-of-enterprise-it.html
---
Everyone knows that Service Providers and Enterprise networks diverged decades ago. More precisely, organizations that offer network connectivity as their core business usually (but not always) behave differently from organizations that use networking to support their core business.

Obviously, there are grey areas: from people claiming to be service providers who can't get their act together, to departments (or whole organizations) who run enterprise networks that look a lot like traditional service provider networks because they're effectively an internal service provider.
<!--more-->
### A More Nuanced Perspective

When I asked Russ White for his opinion, he provided an interesting perspective:

{{<long-quote>}}
You seem to be using "provider" in a couple of different ways here, it might be useful to clarify. I think what you mean is "*people who sell transit services for a living,*" but most folks seem to include content providers into the mix.

Second, I always think the "*enterprise/provider*" split is kind-of useless. I think we tend to mean "*those who treat their network as either a strategic asset for making money or a direct profit center,*" when we say provider, and "*those who consider the network as something they must pay for, although they'd rather not,*" for enterprise. This doesn't always seem to relate to what a company does for a living, but rather company culture. I've been trying to figure this out for years, but haven't yet.

Third, I would say the problem isn't just about scale, but also about perception along the lines above. If you think your network is an asset to your company, then you're more likely to build your own, rather than dealing with vendors, either cloudy or traditional. If you think your network is a cost, then you're likely to pay just about any price to keep from having to think about it. There's some kind of stupidity or lack of awareness about what you're really paying here.
{{</long-quote>}}

### Data Centers Are Not Created Equal {#dc}

Even outside traditional service providers we can see major differences. Paraphrasing [Peter Wohlers](https://www.linkedin.com/in/peterwohlers/) (unfortunately his phenomenal Networking Field Day presentation wasn't recorded), he saw three types of data center customers in 2010:

-   **Cloud-scale web properties** who try to keep things as simple as possible because they have plenty of other headaches to deal with. These days they'd use pure layer-3 data centers running BGP to achieve the scale they need.
-   **Cloud providers** who also try to keep things as simple as possible but already have to deal with crazy requirements like stretched subnets and workload mobility. These days they'd typically use hypervisor-based overlay virtual networks on top of pure layer-3 data centers.
-   **Traditional enterprises** where all bets are off. As always, the bell curve applies to this category (some environments are crazier than others)... or maybe it's a [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution) with a very long tail of people who try to cram a zillion features into every box in their network to solve [yet another one-off request](/2022/11/public-cloud-snowflakes.html).

I'm pretty sure we could identify further distinct environments at the edges of the many-dimensional bell curve:

* **High-performance computing** clusters. Throughput and latency are so important that they use technologies you rarely see anywhere else like Infiniband and RDMA.
* **High-frequency trading**. Reducing latency is their prime objective -- they are the customers prompting Cisco and Arista to develop switches with forwarding delay measured in nanoseconds. They often go as far as using FPGAs in data center switches or SmartNICs to reduce the amount of data processing done on the servers.
* **Service provider clouds** that try to reinvent centralized packet forwarding using virtualized network devices running on generic cloud infrastructure. They must focus on packet forwarding performance but often use technologies like Linux networking stack that were never designed for fast packet forwarding, and hope that crazy tricks like SmartNIC offloads will save the day.
* **Small data centers** that don't need [more than two switches](https://www.ipspace.net/Optimize_Data_Center_Infrastructure/) but often get duped into buying a leaf-and-spine fabric (for future expansion) using [complex technology](/2018/02/using-evpn-in-very-small-data-center.html) and controlled with a black-box solution (example: Cisco ACI) or overpriced intent-based system.

### Back to Enterprise IT

During the [Open Networking](http://www.ipspace.net/Open_Networking_for_Large-Scale_Networks) webinar Russ White made an interesting observation: enterprise IT will soon split into three categories along totally different lines:

-   Organizations who won't be able to afford internal compute/storage/fabric infrastructure anymore and will **move as much to the (public) cloud** as possible;
-   Organizations that will want to retain some on-premises infrastructure and will **use hyper-converged solutions** or managed services like Azure Stack;
-   Organizations that are big enough to afford to invest heavily in networking software to be able to **control their own destiny** (as opposed to moving from one failed vendor marketecture to another every 3-5 years).

I had discussions with engineers who were heavily involved in cloudy infrastructures, and they claim your AWS bill has to be in the million-per-year range before it makes sense to think about internal infrastructure (due to costs of running that infrastructure).

Russ put the low-end size for the third type of organization to ~10.000 server ports in the [Whitebox Switching @ LinkedIn podcast](/2016/09/whitebox-switching-at-linkedin-with.html) and Giacomo Bernardi also mentioned thousands of boxes in [Build Your Own Service Provider Gear](/2016/06/build-your-own-service-provider-gear-on.html) podcast.

However, as Russ pointed out in our (private) conversation:

> I tend to think around 10k ports is probably a break-over point for the rational person. For irrational ones in either direction, all bets are off. The size and quality of the ecosystem also matters -- as the ecosystem becomes better, then the minimum size when building starts making sense probably goes down. I don't know how to measure or account for this. And maybe the ecosystem just won't get any better -- I don't honestly know.

And a final comment from Russ:

> I suspect cloud services are going to end up in the same place as the other vendors -- tossing features in because they can, causing their customers to move from marketecture to marketecture over time. It's just all so new right now that we're not seeing this yet. Once the market starts to mature, though, there's going to need to be a scramble for customers, and that scramble is probably going to be feature driven, and it's not going to be any prettier than what we have now.

Disagree? Write a comment!

### Revision History

2022-12-15
: Added other common types of data centers to the _Data Centers Are Not Created Equal_ section.
