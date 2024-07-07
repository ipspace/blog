---
title: "More: Hardware Differences between Routers and Switches"
date: 2022-01-25 08:47:00
tags: [ switching ]
---
_Aaron Glenn sent me his thoughts on hardware differences between routers and switches based on the last paragraph of [Dmytro Shypovalov](https://www.linkedin.com/in/dmytro-shypovalov-573aab58/)'s [views on the topic](/2021/12/response-router-switch-hardware/)_

---

> To conclude, what is the difference between routers and switches in my opinion? I have absolutely no idea.
<!--more-->
I've done Too Much™ reading on how they were designed and generated some opinions on how we are where we are today. It all started with the divergence from "MIPS CPUs optimized for common packet processing operations" to general CPUs (like PowerPC) and TCAMs and FPGAs to ASICs with extra bandwidth rich memory mimicking TCAM. 

There are two handfuls of switching ASIC vendors that support the Switching Abstraction Interface of the SONiC project[^2]. Looking at their datasheets broadly, you'll notice a commonality in roomy but significantly smaller table space for routes, ACLs, and queuing strategies in comparison to the router designated ASICs. Slap more memory (and a slightly longer or more complex pipelines) and you have a "routing" ASIC. which looks a little like a switching ASIC with a dedicated cross fit regimen.

> All vendors use merchant silicon now, so they will run into similar limitations, but might try to work around them in different ways

Absolutely, however not so much for routing. Broadcom StrataDNX[^1] (neé Dune) is the only "real" merchant routing silicon. Others have their own custom silicon; and some do both (Cisco! don't be surprised). Why real in air quotes? While "merchant routing silicon" might have more complex pipelines or more pipelines, the only real difference is the on-chip table memory and buffers. You can get a Broadcom Jericho 2 chip with 8GB of on chip memory; but from my understanding that is mostly DRAM and not lower latency SRAM or TCAM memory used for tables (FIB/ACLs/etc). The Jericho[^3] line specifically has additional SERDES (bandwidth) for both fabric (that's Ramon[^4]) and things like "external TCAM" (it's often SRAM with a co-processor. suprised? I was!). Qumran has larger on chip table and buffer memory than a Trident or Tomahawk, but not as much as the Jericho...so a tangibly lower price point. The problem is the hardware API is a *special* kind of disaster, apparently[^5]

> I think the discussion about platform architecture (hardware pipeline vs software forwarding) can be more productive.

Yes! A very accessible set of documentation on merchant silicon has been developed by the IOS-XR documentation team regarding the NCS line. All vendors (and business units...) should aspire to publishing that kind of detailed and well explained hardware and software pipeline operations. Arista has some exceptional resources but they're not as easy to discover or as organized as xrdocs.io. Another great technical detail resource for these kinds of pipelines and devices is OpenBNG at TIP... for those of us who drink beverages and read technical data sheets from open standards bodies on the weekends.

"Router vendors hate this one easy trick!" -- if you're willing to trade some latency measured in microseconds (for reference most ethernet switching ASICs measure their port to port latency in nanoseconds) you can very cleverly scale your table memory elastically and (effectively infinitely). Knowing that someone somewhere might find themselves having to support a MAC table measured in hundreds of millions, I share the hesitation one might feel at this kind of technology actually catching on. For those of us who read academic papers non-ironically, I highly recommend TEA[^6] over some tea. 

Finally, if you want to learn a little more, my dear friend Tom Strickx has a very accessible [article on switching ASICs](https://blog.cloudflare.com/asics-at-the-edge/) on Cloudflare blog.

[^1]: https://www.broadcom.com/products/ethernet-connectivity/switching/stratadnx
[^2]: https://azure.github.io/SONiC/Supported-Devices-and-Platforms.html
[^3]: https://www.broadcom.com/products/ethernet-connectivity/switching/stratadnx/bcm88670
[^4]: https://www.ufispace.com/products/telco/core-edge/s9705-48d-400g-disaggregated-core-router
[^5]: https://github.com/Broadcom-Network-Switching-Software/OpenBCM
[^6]: https://daehyeok.kim/assets/talks/tea-sigcomm20-slides.pdf
