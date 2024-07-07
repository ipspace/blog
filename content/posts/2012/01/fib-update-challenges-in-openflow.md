---
date: 2012-01-31 07:00:00+01:00
tags:
- SDN
- switching
- data center
- workshop
- OpenFlow
title: FIB Update Challenges in OpenFlow Networks
url: /2012/01/fib-update-challenges-in-openflow/
---
Last week I described the problems high-end service provider routers (or layer-3 switches if you prefer that terminology) [face when they have to update large number of entries in the forwarding tables](/2012/01/prefix-independent-convergence-pic/) (FIBs). Will these problems go away [when we introduce OpenFlow into our networks](/2011/11/openflow-enterprise-use-cases/)? Absolutely not, OpenFlow is [just another mechanism to download forwarding entries](/2011/04/what-is-openflow/) (this time from an external controller) not a [laws-of-physics-changing miracle](/2011/03/open-networking-foundation-fabric/).
<!--more-->
NEC, the only company I'm aware of that has production-grade OpenFlow deployments *and is willing to talk about them* admitted as much in their [Networking Tech Field Day 2 presentation](http://techfieldday.com/2011/nec-presents-networking-tech-field-day-2/) (watch the *ProgrammableFlow Architecture and Use Cases* video around 12:00). Their particular controller/switch combo can set up 600-1000 flows per switch per second (which is still way better than what researchers using HP switches found and documented in the [DevoFlow paper](http://www.cmlab.csie.ntu.edu.tw/~kenneth/qing2011/paper/6.pdf) -- they found the switches can set up \~275 flows per second).

Now imagine a core of a simple L2 network built from tens of switches and connecting hundreds of servers and thousands of VMs. Using traditional L2 forwarding techniques, each switch would have to know the MAC address of each VM . The core switches would have to update thousands of entries after a link failure, resulting in multi-second convergence time. Obviously OpenFlow-based networks need prefix-independent convergence (PIC) as badly as anyone else.

OpenFlow 1.0 could use flow matching priorities to implement primary/backup forwarding entries and OpenFlow 1.1 provides a *fast failover* mechanism in its *group tables* that could be used for prefix-independent convergence, but it\'s questionable how far you can get with existing hardware devices, and PIC doesn\'t work in all topologies anyway.

It's possible to build [OpenFlow 1.1-compliant switches with existing hardware](/2011/04/openflow-11-in-hardware-i-was-wrong/), but you probably wouldn't be willing to pay for them. As long as [everyone is using merchant silicon](http://nerdtwilight.wordpress.com/2011/07/19/cisco-the-merchant-silicon-question/) from Broadcom, we'll be stuck where we are until Broadcom decides it's time to expand their feature list.

Just in case you're wondering how existing L2 networks work at all -- their data plane performs dynamic MAC learning and populates the forwarding table in hardware; the communication between the control and the data plane is limited to the bare minimum (which is another reason why implementing OpenFlow agents on existing switches is like attaching a jetpack to a camel).

Is there another option? Sure -- it's called *forwarding state abstraction*, or for those more familiar with MPLS terminology *Forwarding Equivalence Class (FEC)*. While you might have thousands of servers or VMs in your network, you have only hundreds of possible paths between switches. The trick every single OpenFlow controller vendor has to use is to replace endpoint-based forwarding entries in the core switches with path-indicating forwarding entries. Welcome back to [virtual circuits](/2011/10/mpls-is-not-tunneling/) and [BGP-free MPLS core](/2012/01/bgp-free-service-provider-core-in/). It's amazing how the old tricks keep resurfacing in new disguises every few years.

#### Need more information?

You might want to read a few other OpenFlow posts I wrote:

-   [What is OpenFlow](/2011/04/what-is-openflow/)
-   [What is OpenFlow (part 2)](/2011/10/what-is-openflow-part-2/)
-   [OpenFlow and the state explosion](/2011/10/openflow-and-state-explosion/)
-   [OpenFlow deployment models](/2011/11/openflow-deployment-models/)
-   [VXLAN, IP Multicast, OpenFlow and control planes](/2011/12/vxlan-ip-multicast-openflow-and-control/)
-   [You don't need OpenFlow to solve every age-old problem](/2011/09/you-dont-need-openflow-to-solve-every/)
-   [OpenFlow: BIOS does not a server make](/2011/04/openflow-bios-does-not-server-make/)
