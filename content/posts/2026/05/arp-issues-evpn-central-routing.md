---
title: "ARP Issues in EVPN Centralized Routing Design"
subtitle: "TL&DR: SIP of Networking Was an Understatement 🤦‍♂️"
date: 2026-05-04 07:45:00+0200
tags: [ evpn ]
evpn_tag: details
---
Adding IRB to a EVPN MAC-VRFs (the fancy way of saying *stretched VLANs*) seems like a no-brainer:

* Add IP addresses to VLAN interfaces
* Optionally add a shared anycast gateway
* Declare "Mission Accomplished" (and try to ignore the inevitable phone call at 2 AM on a Sunday night)

Making that work in a multi-vendor environment is even more fun[^MP], as I sadly discovered when creating the [EVPN lab exercises](https://evpn.bgplabs.net/#evpn) or trying to figure out why some EVPN implementations were failing _netlab_ [EVPN integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration/evpn).
<!--more-->
Trying to explain those issues from scratch in an already convoluted asymmetric IRB environment would probably just confuse you, so I decided to start with a simpler scenario: central routing on a single spine switch.

[^MP]: For people with masochistic tendencies

{{<figure src="/2026/05/evpn-fwd-central-routing.png" caption="Packet forwarding in centralized routing design">}}

Here are our assumptions:

* L1, L2, and Spine are running EVPN and advertising type-2 (MAC-IP) and type-3 (ingress replication) routes.
* L1 and L2 are acting as bridges[^BSB], and have a single EVPN MAC-VRF.
* The Spine has two EVPN MAC-VRF instances and an IP address configured in each MAC-VRF instance. We'll call those IP addresses SIPB and SIPR for obvious reasons. The underlying MAC addresses are SMACB and SMACR.
* HB1 and HR1 have static routes using the adjacent Spine IP address as the next hop.

[^BSB]: The devices lovingly called *layer-2 switches* by vendor marketing departments

Anyone claiming to know a bit about IP routing should be able to recite[^BMC] what happens when HB1 tries to send the first packet to HR1:

[^BMC]: Before the first morning coffee

1. HB1 does a routing table lookup and finds SIPB as the next hop.
2. HB1 sends a broadcast ARP request for SIPB
3. SIPB replies with a unicast ARP reply sent from SMACB
4. HB1 sends the packet for HR1 to Spine using SMACB as the destination MAC address
5. Spine does a routing table lookup and realizes the red VLAN is directly connected.
6. Spine sends a broadcast ARP request for HR1 from SMACR.
7. HR1 replies with a unicast ARP reply sent to the SMACR.
8. Spine can now forward the packet received from HB1 to HR1 using the MAC address of HR1.

Sounds trivial, right? What could possibly go wrong? Where do I start, and how much time do you have?

The easy bit first: several EVPN implementations do not advertise their VLAN IP/MAC addresses without some serious ~~arm twisting~~ nerd knobbing. When HB1 sends an Ethernet packet to SMACB, L1 has no idea where SMACB is (because the Spine switch never advertised the MAC-IP route for SMACB/SIPB), so *all inter-subnet traffic is flooded* ([more details](https://evpn.bgplabs.net/evpn/3-irb/#evpn-routes-and-arp-resolution)). 

Not too bad in our scenario with three switches, but a major disaster in a large-scale fabric with dozens of switches in the same VLAN (oops, MAC-VRF instance).

**Lesson#1:** The spine switch MUST advertise its VLAN MAC/IP address as an EVPN MAC-IP route.

Even worse, some EVPN implementations do not process ARP requests received over VXLAN (because the vendor believes someone else should handle them), making it impossible to make centralized routing work without yet another nerd knob: ARP proxy.

These implementations expect the ingress layer-2 switches to respond to ARP requests *on behalf of routers behind them* based on the information received in the MAC-IP routes. More nerd knobs to twist on the layer-2 switches (L1/L2)

**Lesson#2:** Sometimes you have to enable ARP proxy on the layer-2 EVPN switches to cope with routers not listening to ARP-over-VXLAN.

{{<note info>}}
Please note that ARP proxy (responding to ARP requests *on behalf of someone else in the same subnet*) is not the same as proxy ARP (responding to ARP requests *for IP addresses outside of the subnet on which the ARP request was received*).

Yeah, sometimes we get the terminology *just right* 🤦‍♂️
{{</note>}}

But wait, that's not all. Some implementations refuse to send ARP requests over VXLAN. In our case, Spine would never send an ARP request for HR1, dropping all packets from HB1 to HR1.

These implementations expect the EVPN layer-2 switches (L1 and L2) to snoop for packets that might reveal MAC-to-IP mappings (ARP, ND, DHCP, sometimes even regular IP traffic) and advertise that information as a type-2 (MAC-IP) EVPN route. The central router would then use that information to build its ARP cache, eliminating the need for ARP requests.

**Lesson#3**: If your EVPN implementation refuses to send ARP requests over VXLAN, configure ARP snooping (or however it's called) on layer-2 switches.

{{<note stop>}}
Figuring out how to make ARP snooping work with silent hosts is left as an exercise for the reader. If needed, ask your vendor technical contacts about that minor detail and watch them squirm.
{{</note>}} 

Sometimes, an EVPN implementation might use the defaults that make things *just work* in a *single-vendor environment*. If you're unlucky, your vendor believes in the magic powers of type-5 routes and expects everyone to do symmetric IRB (we'll talk about that some other time). With a bit of luck and arcane knowledge of nerd knobs, you might get some of these implementations to work. If you're truly unlucky, you're stuck, and you can't even use the handheld DMTF tone generator like we could in the wonderful mismatched SIP signaling days.
