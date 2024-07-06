---
title: "Will DPUs Change the Network?"
date: 2023-01-24 07:16:00
tags: [ switching ]
---
It's easy to get excited about what seems to be a new technology and conclude that it will forever change the way we do things. For example, I've seen claims that SmartNICs (also known as *Data Processing Units* -- DPU) will forever change the network.

**TL&DR**: Of course they won't.

Before we start discussing the details, it's worth remembering what a DPU is: it's another server with its own CPU, memory, and network interface card (NIC) that happens to have PCI hardware that emulates the host interface cards. It might also have dedicated FPGA or ASICs.
<!--more-->
Now let's try to put the current blast of hype in perspective by asking two simple questions:

* Have we seen DPUs before?
* What was their impact at that time?

Of course, we've seen DPUs before. Engineers have always tried to offload processing from expensive resources like generic CPU cores to dedicated hardware optimized for a particular task.

The first programmable DPU I'm aware of was the [IBM 3705 Communications Controller](https://en.wikipedia.org/wiki/IBM_3705_Communications_Controller), announced in March 1972 ([2700-series controllers](https://en.wikipedia.org/wiki/IBM_270x) were hard-wired). I also had the dubious privilege of being involved with the IBM 3745 [Front End Processors](https://en.wikipedia.org/wiki/Front-end_processor) (a fancier name for the same idea) while developing a 3271 emulator. Did Front-End Processors (FEP) change networking? No. The real game-changer was the IBM 3270 family of terminals and controllers, with its ability to do local editing and screen-by-screen data transfers.

Even the early Arpanet used DPUs called [Interface Message Processors](https://en.wikipedia.org/wiki/Interface_Message_Processor) (IMP). One might claim Arpanet changed networking forever, but it wasn't the IMPs. IMPs were an early equivalent of Frame Relay switches and provided WAN connectivity. [The attached hosts did all the hard work](/2021/05/fundamentals-interface-node-addresses.html) that eventually brought us The Internet[^AG].

[^AG]: Unless it were the [efforts of Al Gore](https://en.wikipedia.org/wiki/Al_Gore_and_information_technology#Urban_legend_that_Gore_claims_to_have_invented_the_Internet)

One of the first LAN DPUs also came from IBM -- the IBM 3172 Interconnect Controller. Cisco developed another monstrous DPU -- the IBM Channel Interface Processor for the Cisco 7500-series routers. These DPUs were nothing more than Network Interface Cards on steroids and added nothing new to the networking technologies or designs.

We've seen many other DPU attempts in the days when the CPU cycles were expensive, from reassuringly-expensive software-defined[^SD] TCP offload NICs to ridiculously expensive [iSCSI adapters](https://www.computerworld.com/article/2586263/intel-announces-iscsi-network-interface-card.html) that ran the whole TCP/IP stack while presenting the (emulated) registers of a common SCSI adapter to the attached server. Most of that functionality was either integrated into NIC hardware (TCP offload) or [migrated back to the host CPU](/2010/05/iscsi-moores-law-won.html) once the CPU cycles became cheaper. Having it available on a DPU made no difference in the long term; it just allowed early adopters to deploy iSCSI.

[^SD]: Because they had software running on them ;)

The idea to offload well-defined functionality to dedicated hardware is not limited to networking. Most personal computers used simple video adapters with shared memory decades ago; today, it's hard to find one that does not use a Graphic Processing Unit (GPU) -- another server with its memory and CPU attached to the PCI bus. Did GPUs change the way we do GUI? Nope. They did enable smoother-running games and reduced battery consumption[^VT] for the rest of us, though.

[^VT]: Increasing the time we can watch squirrel videos on long-haul flights.

Something similar will probably happen with the currently overhyped batch of DPUs. Eventually, Smart NICs will be everywhere, we'll figure out how to use them most efficiently, and a few organizations will do remarkable things like AWS did with their [Nitro hypervisor](https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/security-design-of-aws-nitro-system.html)[^HFC]. For most of us, nothing will change apart from our devices being a smidgen faster and using a tad less power.

[^HFC]: High-frequency trading is another early adopter of anything that can process incoming data stream before it reaches the server. However, they rarely talk about what they do for obvious reasons.

Or maybe we're already there: did you know you have a DPU within your mobile phone or tablet? Most WiFi chipsets used on those devices have an ARM CPU with RAM, ROM, and operating system[^BP]. Did those DPUs change the way we do networking? They might have, but I failed to notice.

[^BP]: You'll find more details (including an explanation of how one can exploit those chipsets) in the [Broadpwn blog post](https://blog.exodusintel.com/2017/07/26/broadpwn/).

Finally, a word of warning: every time you're offloading complex-enough functionality, you're creating a distributed system with a plethora of interesting edge cases[^CE]. Someone will have to deal with that complexity and iron out the wrinkles. Remember how long it took for TCP offload on Linux to work flawlessly?

[^CE]: And according to developers who had to work with them, existing NICs are [complex enough to make you pull your hair out](/2018/09/smart-or-dumb-nics-on-software-gone-wild.html).
