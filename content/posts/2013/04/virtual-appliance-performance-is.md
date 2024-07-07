---
date: 2013-04-23 06:54:00+02:00
tags:
- security
- virtualization
title: Virtual Appliance Performance Is Becoming a Non-Issue
url: /2013/04/virtual-appliance-performance-is/
---
Almost exactly two years ago I wrote an [article describing the benefits and drawbacks of virtual appliances](/2011/04/virtual-network-appliances-benefits-and/), where I listed virtualization overhead as one of the major sore spots (still partially true). I also wrote: "*Implementing routers, switches **or firewalls** in a virtual appliance would just burn the CPU cycles that could be better used elsewhere.*" It's time to revisit this claim.
<!--more-->
### The Easy Ones

A few data points are obvious:

-   \$0.02 CPU used in SoHo routers is good enough for speeds up to \~10 Mbps (see also: [OpenWrt](http://en.wikipedia.org/wiki/OpenWrt)), and reasonably-sized x86 platforms are good enough for anything between 100 Mbps and 1 Gbps, depending on the functionality you need and the value of *reasonable*.
-   High-speed packet forwarding (e.g. ToR switch @ 1+Tbps) is way cheaper to implement in hardware;
-   High-end packet forwarding gear (CRS-1, MX-960) will be hardware-based for a very long time;
-   Hardware encryption is still faster than software encryption, but at least [AES is included in instruction set of recent Intel and AMD processors](http://en.wikipedia.org/wiki/AES_instruction_set) (RSA is still a CPU burner). Is hardware-assisted SSL offload cheaper than throwing more cores at the problem? I don't know; shop around and do the math.

### Vanilla Virtual Appliances

Virtual appliances are clearly good enough for low-volume loads. VMware claims the firewalling performance of vShield Edge Compact (1 vCPU) appliance is \~3 Gbps. Probably true under the ideal conditions (I got similar results testing an older version of vShield Edge with netperf).

HTTP load balancing performance of vShield Edge Large (2 vCPU) appliance is \~2.2 Gbps. F5 claims its BIG-IP LTM VE can do up to 3 Gbps in a 2 vCPU vSphere-hosted VM. Either one should be good enough unless you plan to push most of your data center traffic through a single virtual appliance (hint: don't \... although I've heard F5 VE license isn't exactly cheap).

Aiming for higher speeds? A10 claims its SoftAX virtual appliance can push up to 8 Gbps of load-balanced traffic. No idea what's required to get that number, the [hardware requirements are in the installation guide](/2012/03/cisco-vmware-merging-virtual-and/), which is hidden behind a regwall. Seems A10 is another one of those [companies that never learn](/2010/09/hiding-documentation-will-they-never/).

### Getting Beyond 10Gbps

What about even higher speeds? It's possible to [push 50 Gbps through Linux TCP stack](http://multipath-tcp.org/pmwiki.php?n=Main.50Gbps) and if you do smarter things like [custom stack](http://erratasec.blogspot.com/2013/02/custom-stack-it-goes-to-11.html), [bypassing the kernel entirely](http://erratasec.blogspot.com/2013/02/multi-core-scaling-its-not-multi.html) or using Intel's DPDK (or [6WIND equivalent](/2012/02/6wind-solving-virtual-appliance/)) you can get the same performance with lower overhead.

However, all the figures quoted in the previous paragraph don't include the virtualization tax (the performance loss, not [this one](http://lonesysadmin.net/2012/08/21/3-reasons-these-vmware-vtax-licensing-rumors-are-great/)). To get comparable performance from a VM typically requires some sort of hypervisor bypass, allowing the VM to work directly with the physical NICs, but that approach usually requires dedicated NICs (not really useful) and disables live VM mobility. You can get rid of both problems with Cisco's [VM-FEX](/2011/08/vm-fex-how-convoluted-can-you-get/) and VMware's [vMotion with VMDirectPath](/2012/03/cisco-vmware-merging-virtual-and/), but that's the only combo I'm aware of that gives you "physical" interfaces (which you need to avoid hypervisor overhead) on a migratable VM.

Good news: the hypervisor landscape seems to be changing rapidly -- [6WIND is demonstrating DPDK-accelerated Open vSwitch at Open Networking Summit](http://www.6windblog.com/virtual-switch-acceleration-boosts-vm-density-in-data-centers/) and they claim they can accelerate both OVS data plane and VXLAN encapsulation, [resulting in 50 Mpps performance on a 10-core server](http://www.sdxcentral.com/companies/6wind-virtual-switch/2013/04/). IMIX traffic profile should be pretty relevant when evaluating load balancers and firewalls, and using the IMIX average packet size of 340 bytes 50 Mpps translates into more than 130 Gbps of L2 virtual switching throughput. Good enough I'd say ;)

Finally, Intel just [announced their reference architecture](http://newsroom.intel.com/community/intel_newsroom/blog/2013/04/17/intel-accelerates-the-data-center-and-telecom-network-transformation-with-new-reference-architectures) (using, among other things, DPDK-accelerated OVS): hardware is available now and DPDK-accelerated OVS in Q3 of this year. Open Networking Platform server is scheduled to enter alpha testing in second half of the year.

**Summary:** In a year or two, we'll have plenty of software solutions and/or generic x86 hardware platforms capable of running very high speed virtual appliances. I would strongly recommend considering that in your planning and purchasing process. Obviously some firewall/load balancing vendors will adapt (major load balancing players already did) while others will stick to their beloved hardware and slowly fade in oblivion.
