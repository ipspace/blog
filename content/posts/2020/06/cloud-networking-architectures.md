---
title: Cloud Networking Architectures
date: 2020-06-09 06:33:00
tags: [ cloud, AWS, Azure, ACI, NSX ]
---
There's one thing no cloud vendor ever managed to change: virtual machines running on top of cloud infrastructure expect to have Ethernet interfaces. 

It doesn't matter if the virtual Ethernet Network Interface Cards (NICs) are implemented with software emulation of actual hardware (VMware emulated the [ancient Novell NE1000](https://en.wikipedia.org/wiki/NE1000) NIC) or with [paravirtual drivers](https://en.wikipedia.org/wiki/Paravirtualization) - the virtual machines expect to send and receive Ethernet frames. What happens beyond the Ethernet NIC depends on the cloud implementation details.
<!--more-->
Most enterprise-focused solutions (vSphere, Hyper-V, NSX, ACI) [emulate the thick yellow cable](/2015/04/what-is-layer-2-and-why-do-we-need-it/) - it's easier to do that than to tell users they can't use shenanigans like MAC- or IP address takeovers (using GARP or RARP) or forced unicast flooding ([Microsoft NLB](/2012/02/microsoft-network-load-balancing-behind/)) they relied upon for the last 30 years

Hypervisors vendors typically try to do the absolute minimum amount of work, implementing a [dumb VLAN-tagging layer-2 switch](/2019/10/the-cost-of-disruptiveness-and/) and [pushing the hard work down the stack](/2013/04/this-is-what-makes-networking-so-complex/), while at the same time [copiously blaming the networking team for their rigidity](/2016/07/why-is-every-sdn-vendor-bashing/).

Overlay virtual networking solutions replace layer-2 fabrics with Ethernet-over-IP transport. The "right" place to do that encapsulation depends on what the vendor telling you the story is trying to sell:

* Hypervisor vendors will tell you to use their [virtual switching solution](/2011/05/complexity-belongs-to-network-edge/) and build the transport fabric with commodity switches (example: buy NSX licenses, don't spend your budget on physical fabric);
* Data center switching vendors tell you to [use their fabric solutions](/2013/06/network-virtualization-and-spaghetti/) and keep hypervisors as dumb as possible (example: buy ACI, don't spend your budget on NSX licenses).

{{<note info>}}I covered the details of various architectural options in [Networking in Private and Public Clouds](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds) and [Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking) webinars.{{</note>}}

Both solutions have interesting limitations:

* Hypervisor-based solutions require virtual-to-physical gateways and have a hard time integrating bare metal servers;
* Hardware-based solutions have scalability limitations and cannot do stateful microsegmentation or any form of deep packet inspection.

Both camps will tell you they have a solution that addresses all these limitations. Cisco will gladly tell you all about ACI Virtual Edge, VMware will praise their NSX agent on bare metal servers... but in both cases you'd be dealing with kludges that desperately try to fit a square peg into a round hole.

{{<note info>}}For more details, watch the [VMware NSX or Cisco ACI webinar](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN).{{</note>}}

In the meantime public cloud vendors decided to step away from the thick yellow cable obsession, and implemented virtual networking that can scale beyond a few hundred hosts. [Azure implemented pure IP networking](/2020/05/azure-networking-101/) (ignoring MAC addresses in Ethernet headers), [AWS implemented unicast MAC forwarding within a subnet and IP forwarding across subnets](/2020/05/aws-networking-101/). 

AWS and Azure also implemented support for bare metal servers using smart interface cards (example: [AWS Nitro](https://aws.amazon.com/ec2/nitro/)). A smart NIC presents a regular Ethernet interface card to the server CPU, but does much more than just transmitting Ethernet frames to the adjacent switch - it implements full-blown overlay virtual networking stack managed from the outside to prevent the server operating system from changing its parameters.

By now you should be wondering why we don't have a similar solution in the enterprise world. Well, we do - Pensando recently launched a smart NIC they claim can do everything AWS Nitro does. For more details, listen to the [Episode 110](/2020/05/smartnic-pensando-podcast/) of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild/), or [watch Pensando presentations](https://techfieldday.com/appearance/pensando-presents-at-cloud-field-day-7/) from [Cloud Field Day 7](https://techfieldday.com/event/cfd7/).

{{<note info>}}Cisco did something similar with their Palo NICs, and even [tried to integrate their solution with vSphere](/2011/08/vm-fex-how-convoluted-can-you-get/), but I've never met anyone using that approach. You'll find more details in various [virtualization webinars](https://www.ipspace.net/Roadmap/Virtualization_webinars).{{</note>}}

Does that mean we'll soon see AWS-like functionality in enterprise clouds? I don't think so, and I can see at least two reasons to be skeptical:

* **Technical**: the smart NIC has to be tightly integrated with the rest of the cloud infrastructure solution. AWS and Azure have total control of the full stack, from server hardware to orchestration system. No enterprise networking vendor comes even close, and the two 400-pound gorillas have little interest in making it work (see below) - the lack of substance in the reply I got to my "_when will Pensando integrate with VMware NSX_" question during CFD7 told me everything I needed to know.
* **Commercial**: it has to be in someone's interest to invest a lot of resources into the full-stack integration, and to sell that solution. I don't expect Cisco to acquire Pensando any time soon, VMware is probably more interested in selling NSX licenses than in another expensive networking acquisition... and unfortunately I don't see a third vendor with a believable enterprise cloud story (HPE already tried to conquer the cloudy skies and failed miserably).
