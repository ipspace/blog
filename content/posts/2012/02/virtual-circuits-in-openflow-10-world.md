---
date: 2012-02-03 06:47:00+01:00
tags:
- OpenFlow
- MPLS
- SDN
title: Virtual Circuits in OpenFlow 1.0 World
url: /2012/02/virtual-circuits-in-openflow-10-world/
---
Two days ago I described how you can [use tunneling or labeling to reduce the forwarding state in the network core](/2012/02/forwarding-state-abstraction-with/) (which you have to do if you want to have reasonably fast convergence with currently-available OpenFlow-enabled switches). Now let's see what you can do in the very limited world of OpenFlow 1.0.

{{<note warn>}}OpenFlow 1.0 is obsolete, but it's still worth noting some of the underlying technical limitations -- see also RFC 1925 Rule 11.{{</note>}}
<!--more-->
### OpenFlow 1.0 does not support tunneling of any sort

Open vSwitch (OpenFlow-capable soft switch running on Linux/Xen/KVM) can use GRE tunnels to exchange MAC frames between hypervisor hosts across an IP backbone, but cannot use OpenFlow to provision those tunnels -- it uses [Open vSwitch Database](http://manpages.ubuntu.com/manpages/natty/man1/ovsdb-server.1.html) to get its configuration information (including GRE tunnel definitions).

After the GRE tunnels have been created, they appear as regular interfaces within the Open vSwitch; an [OpenFlow controller](/2011/10/what-is-nicira-really-up-to/) can use them in flow entries to push user packets across GRE tunnels to other hypervisor hosts.

Tunneling support within existing OpenFlow-enabled data center switches is virtually non-existent (Juniper's MX routers with OpenFlow add-on might be an exception), primarily due to hardware constraints.

We will probably see [VXLAN](/2011/08/finally-mac-over-ip-based-vcloud/)/NVGRE/GRE [implementations in data center switches](/2011/10/vxlan-termination-on-physical-devices/) in the next few months, but I expect most of those implementations to be software-based and thus useless for anything else but a proof-of-concept.

Cisco already has VXLAN-capable chipset in the M-series linecards; [believers in merchant silicon](http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/) will have to wait for the next-generation chipsets.

{{<note info>}}As of February 2022, most data center switching silicon supports VXLAN, and Nexus 7000 is mostly obsolete.{{</note>}}

### OpenFlow 1.0 has limited labeling functionality

MPLS support was added to OpenFlow in release 1.1 and while MPLS-capable hardware devices could use MPLS labeling with OpenFlow, there aren't many devices that would support both MPLS and OpenFlow today (yet again, talk to Juniper). Forget MPLS for the moment.

VLAN stacking was also introduced in OpenFlow 1.1. While it would be a convenient labeling mechanism (similar to SPBV, but with a different control plane), many data center switches don't support Q-in-Q (802.1ad). No VLAN stacking today.

The only standard labeling mechanism left to OpenFlow-enabled switches is thus VLAN tagging (OpenFlow 1.0 supports VLAN tagging, VLAN translation and tag stripping). You could use VLAN tags to build virtual circuits across the network core (similar to what MPLS labels do) and the source-destination-MAC combination at the egress node to recreate the original VLAN tag, but the solution is messy, hard to troubleshoot, and immense fun to audit. But wait, it gets worse.

### The reality

I had the *virtual circuits* discussion with multiple vendors during the [OpenFlow symposium](http://techfieldday.com/2011/openflow-symposium/) and [Networking Tech Field Day](http://techfieldday.com/2011/nfd2/) and we always came to the same conclusions:

-   Forwarding state abstraction is mandatory;
-   OpenFlow 1.0 has very limited functionality;
-   Standard tagging/tunneling mechanisms are almost useless due to hardware/OpenFlow limitations (see above);
-   Everyone uses their own secret awesomesauce to solve the problem \... often with proprietary OpenFlow extensions.

Someone was also kind enough to give me a hint that solved the *secret awesomesauce* riddle: "*We can use any field in the frame header in any way we like.*"

Looking at the [OpenFlow 1.0 specs](http://www.openflow.org/documents/openflow-spec-v1.0.0.pdf) (assuming no proprietary extensions are used) you can rewrite source and destination MAC addresses to indicate whatever you wish -- you have 96 bits to work with. Assuming the hardware devices support wildcard matches on MAC addresses (either by supporting OpenFlow 1.1 or a proprietary extension to OpenFlow 1.0), you could use the 48 bits of the destination MAC address to indicate egress node, egress port, and egress MAC address.

I might have doubts about the *VLAN translation* mechanism described in the previous paragraph (I am positive many security-focused engineers *will* have doubts), but the *reuse header fields* approach is even more interesting to support. How can you troubleshoot a network if you never know what the source/destination MAC addresses really mean?

#### Summary

Before buying an OpenFlow-based data center network, figure out what the vendors are doing (they will probably ask you to sign an NDA, which is fine), including:

-   What are the mechanisms used to reduce forwarding state in the OpenFlow-based network core?
-   What's the actual packet format used in the network core (or: how are the fields in the packet header really used?)
-   Will you be able to use standard network analysis tools to troubleshoot the network?
-   Which version of OpenFlow are they using?
-   Which proprietary extensions are they using (or not using)?
-   Which switch/controller combinations are tested and fully supported?
