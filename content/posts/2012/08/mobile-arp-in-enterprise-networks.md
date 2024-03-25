---
date: 2012-08-16 06:30:00+02:00
tags:
- ARP
- IP routing
- LISP
title: Mobile ARP in Enterprise Networks
url: /2012/08/mobile-arp-in-enterprise-networks.html
---
Keith sent me a set of Mobile ARP questions, starting with "*What's your view on using Mobile ARP in a large enterprise?*"

**Short summary**: Mobile ARP is an [ancient technology that was designed to solve a problem that disappeared with the deployment of DHCP](https://blog.ipspace.net/2011/02/local-area-mobility-lam-true-story.html). Now, let's look at the bigger picture.
<!--more-->
### The Basics

What we could do with Mobile ARP is what I'll call *IP address mobility* in the scope of this article (if there's a better name, write a comment) -- the ability to create host routes to IP hosts in "wrong" subnet, and distribute those host routes through a routing protocol to everyone that might care to know how to reach those hosts.

Obviously, this approach doesn't scale well, particularly if implemented with a single enterprise-wide IGP. However, that hasn't stopped some people from proposing a similar LISP Mobility Architecture, yet again proving the infinite wisdom of [RFC 1925 (section 2.11)](http://tools.ietf.org/html/rfc1925).

Furthermore, the original problem Mobile ARP was trying to solve did not involve moving nodes or fast topology changes. It allowed a stationary node to appear in a foreign IP subnet and still receive traffic for its IP address, but did not allow fast moves between IP subnets.

{{<figure src="/2012/08/s1600-Snail.jpg" caption="The expected pace of Mobile ARP-driven IP address mobility (source: [openphoto.net](http://openphoto.net/gallery/image.html?image_id=10035))">}}

### Campus Networks

Problems with host route scalability prompted IETF to design Mobile IP for IPv4 and IPv6 years ago. If you have to support mobile IP nodes moving across L3 subnets in your campus network, you're better off enabling Mobile IP support on them.

{{<note>}}A [friend of mine](http://www.pragma.si/resume/index.html) was [working on 3G/4G Mobile IPv6 deployment for emergency response teams with Nokia](http://translate.google.com/translate?sl=sl&tl=en&u=http%3A%2F%2Fgo6.si%2F2010%2F12%2Fhome-agent-server-za-mobile-ipv6-postavljen-tudi-sloveniji%2F&act=url). They got the whole thing up and running in a semi-production environment; contact him for more details.{{</note>}}

### Data Centers

The data center is a whole different story. Nobody can ever touch the virtualized holy cows (aka VMs) because something just might break if you install an additional bit of software on them, so the common assumption is Mobile IP is off-limits, and we're using [all sorts of kludges to allow VMs to be moved around and still retain their IP addresses](https://blog.ipspace.net/2010/09/vmotion-elephant-in-data-center-room.html).

Hypervisors already use fake gratuitous ARP messages to indicate a VM has moved to a different location in the data center, so the Mobile ARP seems to be a perfect match. After all, the first-hop routers could use those gratuitous ARPs to discover the VM moves and change the IP forwarding tables accordingly (and there's the [Virtual Subnet IETF draft that proposes exactly that](http://tools.ietf.org/html/draft-xu-virtual-subnet-04)).

The fake gratuitous ARP trick works only due to non-deterministic data-plane-driven forwarding behavior of layer-2 switches (formerly known as bridges) -- as soon as the hypervisor to which the VM has been moved sends the gratuitous ARP with the VM's source MAC address, every switch in the network scraps the previous information and installs the new forwarding entry. Unfortunately, that's not how routers work.

A proper L3-focused IP mobility solution would need at least two steps:

-   The hypervisor from which the VM has been removed would have to inform the first-hop router that the VM's IP address is no longer reachable;
-   The hypervisor to which the VM has moved would have to inform its first-hop router that a new IP address has appeared.

Gratuitous ARP is a mechanism that could potentially solve the second problem assuming we ignore all the security implications, overloaded semantics, and the fact that ARP works only for IPv4 \... but we're still missing the first step (although the [Virtual Subnet draft uses an interesting trick](http://tools.ietf.org/html/draft-xu-virtual-subnet-04#page-9) to solve that problem). Note that we can't rely on ARP timeouts (like Mobile ARP does); the traffic disruption would be way too long.

### VM Mobility with LISP

Cisco has yet another solution for your data center woes: [LISP for Virtual Machine Mobility](http://www.cisco.com/en/US/prod/collateral/iosswrel/ps6537/ps6554/ps6599/ps10800/at_a_glance_c45-646350.pdf) (is it just me or does LISP really look like a hammer desperately searching for a nail?), which is only slightly better than Mobile ARP.

LISP for VM Mobility won't pollute the core IP routing tables with VM host routes because LISP uses another layer of indirection (and IP-over-IP tunneling), but is still hasn't solved the fundamental problem: since there's no protocol between hypervisors and xTRs (LISP terminology for PE-router), LISP relies on traffic snooping to figure out a VM has moved.

{{<note>}}[LISP on Nexus 1000V would be a great solution](https://blog.ipspace.net/2011/06/inter-dc-ip-based-vmotion-with-lisp.html) (because Nexus 1000V knows exactly what's going on with VMs, and could update LISP mapping database accordingly), but that code mysteriously disappeared almost two years ago.{{</note>}}

### Short summary

Mobile ARP was an ancient technology that was solving a now-extinct problem. Please don't try to resurrect it; you might experience a zombie apocalypse.
