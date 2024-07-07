---
date: 2011-08-22T04:00:00.000+02:00
tags:
- switching
- data center
- workshop
- virtualization
title: Soft Switching Might not Scale, but We Need It
url: /2011/08/soft-switching-might-not-scale-but-we/
---
Following a [series of soft switching articles](http://networkheresy.wordpress.com/category/open-vswitch/) written by Nicira engineers (hint: they are using a similar approach as Juniper’s QFabric marketing team), Greg Ferro wrote a scathing [Soft Switching Fails at Scale](http://etherealmind.com/soft-switching-fails-at-scale/) reply. 

While I agree with many of his arguments, the sad truth is that with the current state of server infrastructure virtualization we need soft switching regardless of the hardware vendors’ claims about the benefits of [802.1Qbg](/2011/05/edge-virtual-bridging-evb-8021qbg-eases/) (EVB/VEPA), [802.1Qbh](/2011/06/vn-tag8021qbh-basics/) (port extenders) or [VM-FEX](/2011/08/vm-fex-how-convoluted-can-you-get/).
<!--more-->
A virtual switch embedded in a typical hypervisor OS serves two purposes: it does (usually abysmal) layer-2 forwarding and (more importantly) hides the details of the physical hardware from the VM. Virtual machines think they work with a typical Ethernet NIC – usually based on a well-known chipset like Intel’s 82545 controller or AMD Lance controller – or you could use special drivers that allow the VM to interact with the hypervisor more effectively (for example, VMware’s VMXNET driver).

{{<figure src="/2011/08/s320-VM_Net_Stack.png" caption="Typical network virtualization stack">}}

In both cases, the details of the physical hardware are hidden from the VM, allowing you to deploy the same VM image on any hypervisor host in your data center (or cloudburst it if you believe in that particular mythical beast), regardless of the host’s physical Ethernet NIC. The hardware abstraction also makes the vMotion process run smoothly – the VM does not need to re-initialize the physical hardware once it’s moved to another physical host. VMware (and probably most other hypervisors) solves the dilemma in a brute force way – it [doesn’t allow you to vMotion](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1029371) a VM that’s communicating directly with the hardware using VMDirectPath.

The hardware abstraction functionality is probably way more resource-consuming than the simple L2 forwarding performed by the virtual switches; after all, how hard could it be to do a hash table lookup, token bucket accounting, and switch a few ring pointers?

The virtualized networking hardware also allows the hypervisor host to perform all sorts of memory management tricks. Most modern NICs use packet buffer rings to exchange data between the operating system and the NIC; both parties (NIC and the CPUs) can read or write the ring structures at any time. Allowing a VM to talk directly with the physical hardware effectively locks it into the physical memory, as the hypervisor can no longer control how the VM has set up the NIC hardware and the ring structures; the Ethernet NIC can write into any location belonging to the VM it’s communicating with at any time.

I am positive there are potential technical solutions to all the problems I’ve mentioned, but they are simply not available on any server infrastructure virtualization platform I’m familiar with. The vendors deploying new approaches to virtual networking thus have to rely on a forwarding element embedded in the hypervisor kernel, like the passthrough VEM module Cisco is using in its VM-FEX implementation.

In my opinion, it would make way more sense to develop a technology that tightly integrates hypervisor hosts with the network (EVB/VDP parts of the 802.1Qbg standard) than to try to push a square peg into a round hole using VEPA or VM-FEX, but we all know that’s not going to happen. Hypervisor vendors don’t seem to care and the networking vendors want you to buy more of their gear.
