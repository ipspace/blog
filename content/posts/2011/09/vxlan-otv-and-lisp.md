---
date: 2011-09-01 06:06:00+02:00
tags:
- bridging
- VXLAN
- switching
- data center
- overlay networks
- WAN
- LISP
- virtualization
title: VXLAN, OTV and LISP
url: /2011/09/vxlan-otv-and-lisp.html
---
Immediately after VXLAN was announced @ VMworld, the twittersphere erupted in speculations and questions, many of them focusing on how VXLAN relates to OTV and LISP, and why we might need a new encapsulation method.

VXLAN, OTV and LISP are point solutions targeting different markets. VXLAN is an IaaS infrastructure solution, OTV is an enterprise L2 DCI solution and LISP is \... whatever you want it to be.
<!--more-->
VXLAN tries to solve a very specific IaaS infrastructure problem: replace VLANs with something that might scale better. In a massive multi-tenant data center having thousands of customers, each one asking for multiple isolated IP subnets, you quickly run out of VLANs. VMware tried to solve the problem with [MAC-in-MAC encapsulation (vCDNI)](/2011/04/vcloud-director-networking.html), and you could potentially do the same with the right combination of [EVB (802.1Qbg)](/2011/05/edge-virtual-bridging-evb-8021qbg-eases.html) and [PBB (802.1ah)](http://en.wikipedia.org/wiki/IEEE_802.1ah-2008), [very clever tricks a-la Network Janitor](/2011/05/edge-virtual-bridging-evb-8021qbg-eases.html), or even with [MPLS](/2011/04/vcloud-architects-ever-heard-of-mpls.html).

Compared to all these, VXLAN has a very powerful advantage: it runs over IP. You don't have to touch your existing well-designed L3 data center network to start offering IaaS services. The need for multipath bridging voodoo magic that a decent-sized vCDNI deployment would require is gone. VXLAN gives Cisco and VMware the ability to start offering reasonably-well-scaling IaaS cloud infrastructure. It also gives them something to compete against Open vSwitch/Nicira combo.

Reading the [VXLAN draft](http://tools.ietf.org/html/draft-mahalingam-dutt-dcops-vxlan-00), you might notice that all the control-plane aspects are solved with [handwaving](http://en.wikipedia.org/wiki/Handwaving). Segment ID values just happen, IP multicast addresses are defined *at the management layer* and the hypervisors hosting the same VXLAN segment don't even talk to each other, but rely on layer-2 mechanisms (flooding and dynamic MAC address learning) to establish inter-VM communication. VXLAN is obviously a QDS (Quick-and-Dirty-Solution) addressing a specific need -- increasing the scalability of IaaS networking infrastructure.

VXLAN will indeed scale way better than VLAN-based solution, as it provides total separation between the virtualized segments and the physical network (no need to provision VLANs on the physical switches), it will scale somewhat better than MAC-in-MAC encapsulation because it relies on L3 transport (and can thus work well in existing networks), but it's still a very far cry from Amazon EC2. People with extensive (bad) IP multicast experience are also questioning the wisdom of using IP multicast instead of source-based unicast replication \... but if you want to remain control-plane ignorant, you have to rely on third parties (read: IP multicast) to help you find your way around.

It seems there have already been claims that VXLAN solves inter-DC VM mobility (I sincerely hope I've got a wrong impression from [Duncan Epping's summary of Steve Herrod's general session @ VMworld](http://www.yellow-bricks.com/2011/08/30/general-session-steve-herrod/)). If you've ever heard about [traffic trombones](/2011/02/traffic-trombone-what-it-is-and-how-you.html), you should know better (but it does [prove a point \@etherealmind made recently](http://twitter.com/etherealmind/status/108629286050729984)). Regardless of the [wishful thinking](http://twitter.com/etherealmind/status/108629676922122241) and beliefs in flat earth, holy grails and unicorn tears, a pure bridging solution (and VXLAN is no more than that) will never work well over long distances.

Here's where OTV kicks in: if you do become tempted to implement long-distance bridging, OTV is the least horrendous option ([BGP MPLS-based MAC VPN](http://tools.ietf.org/html/draft-raggarwa-mac-vpn-01) will be even better, but it still seems to be working primarily in PowerPoint). It replaces dynamic MAC address learning with deterministic routing-like behavior, provides proxy ARP services, and stops unicast flooding. Until we're willing to change the fundamentals of transparent bridging, that's almost as good as it gets.

As you can see, it makes no sense to compare OTV and VXLAN; it's like comparing a racing car to a downhill mountain bike. Unfortunately, you can't combine them to get the best of both worlds; at the moment, OTV and VXLAN live in two parallel universes. OTV provides long-distance bridging-like behavior for individual VLANs, and VXLAN cannot even be transformed into a VLAN.

LISP is yet another story. It provides a very rudimentary approximation to IP address mobility across layer-3 subnets, and it might be able to do it better once everyone realizes hypervisor is the only place to do it properly[^LD]. However, it's a layer-3 solution running *on top of* layer-2 subnets, which means you might run LISP in combination with OTV (not sure it makes sense, but nonetheless. You could also be able to run LISP in combination with VXLAN *once you can terminate VXLAN on a LISP-capable L3 device*.

[^LD]: This idea died before it got anywhere close to a product.

So, with the introduction of VXLAN, the networking world hasn't changed a bit: the vendors are still serving us all isolated incompatible technologies \... and all we're asking for is tightly integrated and well-architected designs.
