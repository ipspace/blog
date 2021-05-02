---
title: "Mythbusting: NFV Data Center Fabric Buffering Requirements"
date: 2021-05-25 06:49:00
tags: [ data center, fabric, QoS ]
---
Every now and then I stumble upon an article or a comment explaining how Network Function Virtualization (NFV) introduces new data center fabric buffering requirements. Here's a recent example:

> For Telco/carrier Cloud environments, where NFVs (which are much slower than hardware SGW) get used a lot, latency is higher with a lot of jitter due to the nature of software and the varying link speeds, so DC-level near-zero buffer is not applicable.

It seems to me we're dealing with another myth. Starting with the basics:
<!--more-->
* NFV is Network Function Virtualization -- routing, switching, network security, or load balancing running in virtual machines or containers (often within a carrier cloud).
* Some people add voice gateways to the mix, like voice wouldn't be just another application using small packets on top of the network infrastructure (like DNS).
* In any case, I haven't seen many network functions that would *create* significant amount of *new* traffic. In most cases, a packet gets into the (virtual or physical) appliance, is inspected, mangled, and sent out or dropped.

One-to-many media gateways are an obvious exception to that rule, but I wouldn't worry about them[^1]. After all, we're running most of our voice and video calls over public Internet, and they mostly work reasonably well in an environment that's way more demanding than anything that could happen in a data center fabric.

[^1]: And I still don't understand why someone would call them *network function*. You don't call a web site implementing a video streaming a *network function*, do you?

For the ballpark discussion we're having right now, let's assume NFV instances do *packet processing* and not *packet generation*. Now let's look at a typical NFV-hosting data center and try to figure out what that means assuming NFV consumers are outside of the data center:

{{<figure src="/2021/05/NFV-Architecture.png" caption="Typical NFV architecture">}}

* The total bandwidth requirement of your NFV cloud is limited by the WAN ingress bandwidth.
* You need more bandwidth within the fabric if you chain NFV devices, but unless you're doing something extremely convoluted, you won't need more than an order of magnitude more bandwidth.
* Required egress WAN bandwidth is comparable to the ingress bandwidth (obvious exception: media gateways).
* Aggregate data center fabric bandwidth is usually order(s) of magnitude bigger than the WAN bandwidth. Four pizza-box spine switches give you 50 Tbps of forwarding bandwidth[^2]. Compare that to a few 100 Gbps WAN links you might have (or not).
* There are no traffic bursts. Speeds within the data center fabric are higher than the WAN speeds, which means that the packets arriving to an NFV appliance are effectively trickling in.
* NFV instances might be batching packets to optimize processing, but I wouldn't expect to see megabyte-size bursts. That would just introduce too much latency.

[^2]: Make that 100 Tbps when using marketing math.

Considering all that, it looks to me like:

* NFV deployments might be even less demanding than typical data center applications (because they're bandwidth-limited).
* There is no buffering problem within a data center fabric.
* You still need decent buffers in the WAN edge router, but probably not any more than what you have on the other side of the WAN link.[^3]

Of course I could be totally wrong (even though this thingy was simmering for a few years before I managed to write it down). Should that be the case, I would appreciate someone pointing out my errors.

[^3]: If the remote buffers were good enough to get a packet into the data center, similar egress buffers should be good enough to get the processed packet out of it.