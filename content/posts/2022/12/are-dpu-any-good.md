---
title: "Are DPUs Any Good?"
date: 2022-12-01 08:14:00
tags: [ switching, virtualization ]
---
After [VMware launched DPU-based acceleration for VMware NSX](https://blogs.vmware.com/networkvirtualization/2022/08/announcing-dpu-based-acceleration-for-nsx.html/), marketing-focused websites frantically started discussing the benefits of DPUs. Although I've been writing about SmartNICs and DPUs for years, it's time for another closer look at the emperor's clothes.

### What Is a DPU

DPU (Data Processing Unit) is a fancier name for a network adapter formerly known as SmartNIC -- a server repackaged into an interface card form factor. We had them for decades (anyone remembers iSCSI offload adapters?)
<!--more-->
A DPU has a CPU (these days, usually based on ARM architecture), memory, storage, network interface, and a PCI interface that behaves like a network interface, making the host operating system think it's dealing with an interface card. Every DPU is running an operating system (often Linux) that cannot be configured from the attached host if you want to retain any [semblance of a security boundary](/2020/09/need-smart-nic/) -- another [wonderful upgrade nightmare and attack vector](/2020/06/smart-nic-security/) (FWIW, check out Broadpwn). Just ask anyone who had to deal with ILOBleed or other IPMI vulnerabilities.

### DPU and Bare-Metal Servers

Sarcasm aside, you must use DPUs to offer bare-metal compute resources in a public cloud; there's no other way to implement a security boundary between a bare-metal server and a virtual network. That's how the AWS Nitro project started, and once they solved that particular challenge, they decided to offload networking to a DPU anyway[^UH].

[^UH]: If you have a hammer, use it whenever you see a nearby nail

Not surprisingly, that's not how the marketers are selling DPUs to the unsuspecting CxOs. VMware talks about DPU acceleration but does not yet support NSX running on a DPU attached to a bare-metal server.

### Improved Packet Forwarding Performance

What else is there? Improved performance and reduced power utilization are the usual claims. Now let's assume that the network interface in a DPU has no secret sauce that wouldn't be available in a regular network interface card[^NA]. Where would the perceived performance improvement come from? There are only a few possible answers:

[^NA]: I have yet to see a vendor with a magic unicorn-smelling bit of silicon that is not packaged in every possible form factor.

-   The networking stack of the host operating system sucks so badly[^OVS], that it makes sense to offload packet processing to a more streamlined implementation. Please note we're talking about bloatware not hardware limitations -- when done right, a 2-socket Xeon server can handle 1 Tbps of encrypted traffic (or so [fd.io claims](https://fd.io/latest/news/terabit_ipsec/)).
-   The ARM CPU used in the DPU can do the same amount of work while transforming less electricity into heat than the host x86 CPU. While that might be true, I wouldn't expect drastic savings assuming the comparable quality of software packet forwarding implementations.
-   You're hitting the bandwidth limitations of the server PCI/memory bus, and reducing the number of times the main CPU has to look at a byte in transit (for example, offload encryption to DPU) helps you reach the 700 Gbps-per-server goal. Offloading encryption to DPU is thus a fantastic feature if you're Netflix ([talk](https://www.youtube.com/watch?v=36qZYL5RlgY), [slides](https://people.freebsd.org/~gallatin/talks/euro2022.pdf)); everyone else probably doesn't care.

[^OVS]: One of the Linux virtual switch implementations managed to push [1 Gbps of traffic](/2014/11/open-vswitch-performance-revisited/) when a VMware virtual switch effortlessly saturated multiple 10 Gbps uplinks. No wonder one can use DPU offload to increase its performance.

Not surprisingly, [NVIDIA loves comparing its DPU performance with OVS](https://www.nextplatform.com/2022/11/03/economics-and-the-inevitability-of-the-dpu/). It's easy to excel when you start with a pretty low bar ;), and reading their reports it looks like the primary role of the DPUs is to add another layer of abstraction to hide how much the software packet forwarding of the virtual switch you believed in sucks[^1925].

[^1925]: RFC 1925 Rule 6a is proud of those efforts ;)

But wait, there's more. DPU vendors love to point out that DPUs reduce the number of host CPU cores needed to perform a specific task. What a revelation: you add CPU cores on DPUs to the data center, so you need fewer CPU cores in servers to get the same amount of work done. I would say that's a classic attempt to shift revenue away from Intel[^CL].

[^CL]: ... and vendors licensing their software based on CPU cores.

In the end, DPUs aren't magic. DPUs are additional servers inserted between existing servers and the network. Unless you're using them as a front-end to bare-metal servers, you're just shifting the workload and squashing the complexity sausage.

Do they make sense if you're not at the absolute bleeding edge of the packet forwarding performance? Do the math (ignoring for the moment the increased complexity and exciting new bugs):

-   How much does a DPU cost, and how many CPU cores will it free up for other work?
-   How much will you save on core-based licensing[^VL] if you deploy DPUs, and how much will the DPU licenses cost?

[^VL]: There's a reason I'm mentioning CPU core-based licensing, DPUs, and VMware NSX in the same blog post. Caveat emptor.
