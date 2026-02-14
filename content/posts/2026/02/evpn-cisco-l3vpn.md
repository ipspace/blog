---
title: "EVPN IP-VRFs on Cisco IOS/XE: Configuration Notes"
date: 2026-02-18 07:31:00+0100
tags: [ evpn ]
evpn_tag: details
---
Last week, I described some of the gotchas I encountered while [trying to make EVPN MAC-VRFs work on Cisco IOS/XE](/2026/02/evpn-cisco-ios/). In the meantime, I got [IP-VRFs with transit VXLAN segments working](https://github.com/ipspace/netlab/pull/3101). Here are the CliffsNotes:

Starting with the disgusting configuration mechanism:
<!--more-->
* Cisco IOS/XE is one of the very few devices I encountered that expects you to configure *an explicit VLAN* for the transit VXLAN segment.
* Obviously, that also means you have to keep track of the VLAN allocation. The only other devices where we had to do that were the pre-NVUE Cumulus Linux and Cisco Nexus OS. At that time, we hard-coded the VLAN IDs (3000-something + VRF index); this time, I did it "the right way" and allocated an unused VLAN to the transit VNI. I can't imagine why the same idea never occurred to someone in the Cisco IOS/XE development team[^DMWL]

[^DMWL]: Maybe it's an inevitable consequence of believing in the Doing More With Less mantra for decades.

Like that wouldn't be bad enough, you have to deal with the [router-versus-switch](https://blog.ipspace.net/2022/09/interfaces-ports/) differences. Even worse, you can find tons of examples telling you how to configure the transit VLAN on switch-focused images (using VLANs), but almost nothing on doing it on router-focused images (using *bridge domains*).

Here are the cheat sheets, just in case someone stumbles upon this blog post while searching for the same topic[^AIL]:

[^AIL]: Or maybe it will be scrapped by the [biggest thieves of intellectual property in the history of humanity](https://garymarcus.substack.com/p/irony-irony-laced-with-karma-and) and then presented as their brilliant conclusion.

{{<cc>}}Transit VLAN configuration on IOS/XE switch images{{</cc>}}
{{<printout>}}
vlan 3800
 name VRF_customer_TRANSIT
!
vlan configuration 3800
 member vni 5042
!
interface Vlan3800
 vrf forwarding customer
 ip unnumbered Loopback0
 no shutdown
 no autostate
{{</printout>}}

{{<cc>}}Transit bridge domain on IOS/XE router images{{</cc>}}
{{<printout>}}
bridge-domain 3800
 member vni 5042
!
interface BDI3800
 vrf forwarding customer
 ip unnumbered Loopback0
 no shutdown
{{</printout>}}

**Notes**

* The transit VXLAN segment (VNI) is tied to a **vlan configuration** or a **bridge-domain** with the **member vni** command.
* The corresponding SVI/BDI/VLAN interface has to be configured, placed in the correct VRF, given an IP address, and enabled.
* The **autostate** has to be turned off on the VLAN interface, as it has no attached interfaces.

Next, you have to tie the transit VXLAN segment to a VXLAN interface (no surprise there), using the **member vni vrf** command (which only works after you configured **‌host-reachability protocol bgp** on the same interface).

That solves the data-plane issues. Now for the control plane:

* The IP-VRFs need EVPN route targets. While you can configure MPLS/VPN route targets under **vrf definition**, the EVPN route targets have to be configured under VRF **address-family**. OK, whatever.
* The "this is an EVPN route target" keyword is **stitching** 🤦‍♂️ 🤦‍♂️ 🤦‍♂️[^TFE]. Seriously. You can't make this up. For example:

[^TFE]: Unicode desperately needs a [triple-facepalm](https://www.google.com/search?udm=2&q=triple+facepalm) emoji.

{{<cc>}}IOS/XE VRF definition with EVPN route targets{{</cc>}}
{{<printout>}}
vrf definition customer
 address-family ipv4
  route-target import 65000:1 stitching
  route-target export 65000:1 stitching
 exit-address-family
{{</printout>}}

After that, the configuration is pretty smooth:

* Activate neighbors in the EVPN address family
* Include EVPN routes into the BGP VRF instances with the **advertise l2vpn evpn** command under **address-family _af_ vrf _name_** BGP configuration.

The fun starts when you try to test your work. Everything works out of the box *if you configured stuff in just the right sequence*, which seems to be (sometimes):

* Enable EVPN address family
* Configure transit VNIs on the VXLAN interface
* Configure VRF EVPN route targets
* Configure **bridge-domain** or VLAN configuration
* Configure BDI/VLAN interface

However, if you happen to have *more than one VRF* and configure the VRF EVPN route targets before enabling the EVPN address family, it takes almost a minute for some *VPN import* stuff to kick in and redistribute connected subnets into EVPN. At the same time, routes received from the CE-routers via BGP are propagated (almost) immediately.

Even worse, if you have EVPN address family enabled and configure VRF EVPN route targets *before configuring the member VNI on the VXLAN interface*, the router advertises the IP-PREFIX (type-5) routes with MPLS labels but without the VXLAN VNI. After configuring the transit VNI, it can take up to a minute[^60s] for the changed IP-PREFIX routes to be sent. However, even doing things *in the right order* does not guarantee that the first EVPN update sent from IOS/XE will include the VNI and Router MAC communities. The command that worked for me was **neighbors encap vxlan** under the **l2vpn evpn** address family.

You might wonder why I'm so focused on IOS/XE sending the first EVPN update with the correct information. After all, things get sorted out eventually.

Here's the kicker: receiving an EVPN route with an MPLS label and no VNI (or router MAC address) confuses FRRouting (at least the 10.5.1 release). It installs the route into the VRF routing table, but the route remains *inactive*:

```
s2# show ip route vrf customer
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF customer:
B   172.16.0.0/24 [200/0] via 10.0.0.1, tvni-100 inactive onlink, label 257, weight 1, 00:02:12
C>* 172.16.1.0/24 is directly connected, eth2, weight 1, 00:04:29
L * 172.16.1.2/32 is directly connected, eth2, weight 1, 00:04:29
L>* 172.16.1.2/32 is directly connected, eth2, weight 1, 00:04:29
```

Even after IOS/XE sends an updated EVPN route with VNI and router MAC address, FRRouting claims the router MAC address is all zeros:

```
s2# show evpn next-hops vni 5042
Number of NH Neighbors known for this VNI: 1
IP              RMAC
10.0.0.1        00:00:00:00:00:00
```

Clearing the BGP session[^CBS] solves that problem.

[^60s]: There must be a 60-second VRF import timer somewhere in the Cisco IOS/XE BGP process. I wasn't able to find how to tweak it. Pointers in the right direction would be most welcome; as expected, ChatGPT produced a 5-page "*I have no idea, but I believe things eventually work*" response.

[^CBS]: Something we love to do almost as much as reloading a box when a level-1 TAC engineer claims *it will make the problem go away*.