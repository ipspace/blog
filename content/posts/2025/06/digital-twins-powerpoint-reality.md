---
title: "Network Digital Twins: Between PowerPoint and Reality"
date: 2025-06-19 07:16:00
tags: [ automation ]
---
A Network Artist left an interesting remark on one of my blog posts:

> It's kind of confusing sometimes to see the digital twin (being a really good idea) never really take off.

His remark prompted me to resurface a two-year-old draft listing a bunch of minor annoyances that make Networking Digital Twins more of a PowerPoint project than a reality.
<!--more-->
Let's start with the easy ones:

* Since [Dynamips](https://en.wikipedia.org/wiki/Dynamips) ran out of platforms to emulate, I haven't seen a virtual machine (or container) that supports **anything other than Ethernet interfaces**. That might not matter in 2025, but if you happen to have any other technology  in your network, it's an immediate showstopper.
* Network operating systems packaged as virtual machines often have **different interface names** than the real hardware. The only vendor I've seen dealing with that was Cumulus Linux, which could (being based on Linux) simply rename the devices (Ethernet ports).
* Very few virtual machines that emulate chassis switches allow you to **specify the line cards** you want to use. The only exception I'm aware of is Nokia [SR Linux](https://containerlab.dev/manual/kinds/srl/#types) and [SR-OS](https://github.com/hellt/vrnetlab/tree/master/sros#variants).
* Virtual machines usually have a **limited number of interfaces**, whether due to VM limitations or limitations of the virtualization infrastructure. That could make it impossible to reliably emulate large core switches.
* **RAM and CPU requirements**: Some virtual machines emulating bloated network devices require 4+ CPU cores and 16+ GB of RAM. On the other hand, apart from [Clabernetes](https://containerlab.dev/manual/clabernetes/), I haven't seen any serious effort to build a *Digital Twin Infrastructure* that would be able to deploy the workload on a server cluster. It must be great fun building a server that can emulate a large Nexus OS fabric.

But wait, we just got started. There's the tiny detail of  *data plane emulation*. I heard of a single company (NVIDIA) that claimed they're trying to emulate their ASICs in virtual machines.

Anyway:

* Virtual data plane functionality often doesn't match the ASIC behavior ([more details](/2022/03/dataplane-quirks-virtual-devices/), [examples](/tag/netlab/#quirks)). Even worse, some virtual machines cannot deal with basic features like interface bandwidth. I don't want to know how reliable QoS emulation is on platforms that do QoS in hardware.
* Printouts related to the data plane functionality probably don't match between virtual machines and physical hardware, making it impossible to test any network automation solution that relies on inspecting hardware details.
* Some control-plane protocols might not work as expected (I had problems with some BFD implementations)
* Control-plane protection might not work (I'm not brave enough to try it out)
* I never tested the complex failover functionality (such as TI-LFA), but I wouldn't be surprised to find quirks.

**Long story short:** It looks like most vendors decided the primary use case of the VM versions of their network devices is kicking the tires and getting familiar with the platform. That's awesome, and I can't tell you how important it is for someone evaluating a new platform to gain some hands-on experience with it. However, there's a very long way between this use case and a reliable (and thus useful) digital twin.

{{<note>}}
I hope the reality is not as bleak as what I can see from here; should that be the case, please leave a comment.
{{</note>}}

Finally, let's address the pair of elephants that was patiently waiting in the corner of the room:

* Why would you need to [build a digital twin of the whole network](/2019/09/if-you-have-to-simulate-your-whole/)? You're probably [solving the wrong problem](/2022/04/digital-twin-powerpoint/).
* If you think you can use a network digital twin to test changes to network configuration, did you [write the tests](/2021/12/ci-cd-network-automation-tests/) to validate the change? If not, what exactly do you plan to test?

The generic *I can use a digital twin to test changes in my network* idea is unfortunately as sound as *[I can move my VM around the world](/2011/10/follow-sun-workload-mobility-get-lost/) to minimize the latency for currently-active users*. Both of them look great in PowerPoint, but match reality as closely as a [spherical cow in a vacuum](https://en.wikipedia.org/wiki/Spherical_cow).
