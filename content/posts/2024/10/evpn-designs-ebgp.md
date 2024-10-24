---
title: "EVPN Designs: EBGP Everywhere"
series_title: "EBGP Everywhere"
date: 2024-10-08 08:12:00+0200
lastmod: 2024-10-10 18:04:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the previous blog posts, we explored the [simplest possible IBGP-based EVPN design](/2024/05/evpn-designs-ibgp-full-mesh/) and [made it scalable with BGP route reflectors](/2024/09/evpn-designs-ibgp-rr/).

Now, imagine someone persuaded you that EBGP is better than any IGP (OSPF or IS-IS) when building a data center fabric. You're running EBGP sessions between the leaf- and the spine switches and exchanging IPv4 and IPv6 prefixes over those EBGP sessions. Can you use the same EBGP sessions for EVPN?

**TL&DR:** It depends&trade;.
<!--more-->
We'll yet again work with a simple leaf-and-spine fabric:

{{<figure src="/2024/04/evpn-design-fabric.png" caption="Leaf-and-spine fabric with two VLANs">}}

However, this time:

* We'll be running EBGP and no IGP between leaf- and spine switches.
* We'll try to run [EBGP sessions over IPv6 link-local addresses](https://bgplabs.net/basic/d-interface/) ([more details](https://blog.ipspace.net/2022/11/bgp-unnumbered-duct-tape/)) to reduce the overhead of managing IPv4 subnets.
* The EBGP sessions will transport IPv4 and EVPN address families.

What could possibly go wrong? Starting with the *EBGP-as-better-IGP* idea:

* OSPF or IS-IS configuration is trivial compared to EBGP configuration unless your fabric has hundreds of switches, forcing you to deploy OSPF areas or multi-level IS-IS[^SRTB].
* BGP needs way more configuration state than OSPF or IS-IS. You must keep track of BGP neighbors, their IP addresses (unless you can use IPv6 LLA EBGP sessions), and their AS numbers[^FREX]. In OSPF, you can use a one-liner: **network 0.0.0.0/0 area 0**[^LBPF]
* You could simplify BGP configuration and use the same AS number on all spine switches (recommended to prevent [path hunting](https://blog.ipspace.net/2018/09/valley-free-routing-in-data-center/)) and another AS number on all leaf switches. Still, then you'd have to [manipulate AS path](https://bgplabs.net/session/2-asoverride/), [turn off AS-path-based loop prevention checks](https://bgplabs.net/session/1-allowas_in/), or use default routing[^NDR].

[^SRTB]: In which case, I hope you're reading this blog post solely for its entertainment value ;)

[^FREX]: Unless you're using **neighbor remote-as external** FRRouting configuration command

[^LBPF]: Or whatever your loopback prefix range is

[^NDR]: Please don't unless you want a fun troubleshooting exercise after a leaf-to-spine link failure. The details are left as an exercise for the reader.

The only control-plane stack that makes EBGP as easy to deploy as IGP is still FRRouting. Multiple vendors support IPv6 LLA EBGP sessions, but most of them expect you to navigate the unexpected configuration requirements like *[we have to define a peer group for interface EBGP sessions](https://blog.ipspace.net/2024/03/arista-interface-ebgp/)*.

Now for the EVPN address family considerations:
{ #evpn-considerations }

* The EVPN next hop (VTEP) should not change across the data center fabric; you wouldn't want intermediate nodes to do VXLAN-to-VXLAN bridging[^MCD]. The spine switches, thus, should not change the BGP next hop on EBGP sessions, but that's not how EBGP works. Some vendors tweak the default EBGP behavior in the EVPN address family and leave the BGP next-hop unchanged. Others require a configuration nerd knob.
* EVPN has an excellent *auto RT* functionality that automatically sets the EVPN route targets based on the device's BGP AS number and VLAN ID. That does not work across multiple autonomous systems unless the vendor (like Cumulus Linux) decides it's OK to ignore the AS number part of EVPN route targets[^NAGA]

[^MCD]: Due to hardware limitations, most of them wouldn't be able to do that anyway.

[^NAGA]: Not always a good idea, but you already know there's a tradeoff lurking wherever you look.

Finally, the elephant in the room. Some vendors seem to have [suboptimal EVPN implementations](https://blog.ipspace.net/2019/04/dont-sugarcoat-challenges-you-have/) that struggle with EVPN churn or a lost EVPN BGP session. Those vendors will [invent all sorts of reasons](https://blog.ipspace.net/2020/02/the-evpnbgp-saga-continues/) why it makes perfect sense to run EVPN IBGP sessions between endpoints advertised with underlay IPv4 EBGP, or (even better) why it's best to run EVPN EBGP sessions between loopbacks advertised through a different set of IPv4 EBGP sessions.

We'll leave those discussions for another time and explore the more straightforward scenario of running the IPv4 and EVPN address families on the same EBGP sessions. We'll use a lab setup similar to the [IBGP Full Mesh Between Leaf Switches](/2024/05/evpn-designs-ibgp-full-mesh/); read that blog post as well as the *[Creating the Lab Environment](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab)* section of the first blog post in this series to get more details.

### Leaf-and-Spine EBGP-Everywhere Lab Topology {#lab}

This is the [_netlab_ lab topology description](https://github.com/ipspace/netlab-examples/blob/master/EVPN/ebgp/topology.yml) we'll use to set up IPv4+EVPN EBGP sessions between leaf and spine switches.

{{<printout>}}
defaults.device: eos
provider: clab

addressing.p2p.ipv4: True
evpn.as: 65000
evpn.session: [ ebgp ]
bgp.community.ebgp: [ standard, extended ]
bgp.sessions.ipv4: [ ebgp ]

plugin: [ fabric ]
fabric:
  spines: 2
  leafs: 4
  spine.bgp.as: 65100
  leaf.bgp.as: '{ 65000 + count }'

groups:
  _auto_create: True
  leafs:
    module: [ bgp, vlan, vxlan, evpn ]
  spines:
    module: [ bgp, evpn ]
  hosts:
    members: [ H1, H2, H3, H4 ]
    device: linux

vlan.mode: bridge
vlans:
  orange:
    links: [ H1-L1, H2-L3 ]
  blue:
    links: [ H3-L2, H4-L4 ]

tools:
  graphite:
{{</printout>}}

The [VXLAN Leaf-and-Spine Fabric](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#topo) blog post explains most of the topology file. We had to make these changes to implement the EBGP-everywhere scenario:

* Line 4: We're using unnumbered point-to-point links (remove this line if your device does not support interface EBGP sessions)
* Line 5: We need a global AS number to set the route targets for EVPN layer-2 segments[^NART]
* Line 6: EVPN has to be enabled on EBGP sessions
* Line 7: Switches must send extended BGP communities on EBGP sessions
* Line 8: We don't need an IBGP session between S1 and S2 (by default, _netlab_ tries to build IBGP sessions between routers in the same autonomous system). The fabric has only EBGP sessions.
* Line 14: The BGP AS number on the spine switches is set to 65100
* Line 16: The BGP AS number on the individual leaf switches is set to 65000 + switch ID ([more details](https://netlab.tools/plugins/fabric/#leaf-and-spine-parameters), [example](https://netlab.tools/plugins/fabric/#building-an-ebgp-fabric))
* Line 20: Leaf switches are running VLANs, VXLAN, BGP, and EVPN
* Line 22: Spine switches are running BGP and EVPN

[^NART]: netlab is not using automatic EVPN route targets or route distinguishers.

Assuming you already did the previous homework, it's time to start the lab with the **netlab up** command. You can also [start the lab in a GitHub Codespace](/2024/07/netlab-examples-codespaces/) (the directory is `EVPN/ebgp`); you'll still have to [import the Arista cEOS container](/2024/07/arista-eos-codespaces/), though.

### Behind the Scenes {#bds}

This is the FRRouting BGP configuration of L1. As you can see, it's as concise as it can get. The spine configuration is almost identical; it has more EBGP neighbors but no additional nerd knobs.

{{<printout>}}
router bgp 65001
 bgp router-id 10.0.0.1
 no bgp default ipv4-unicast
 bgp bestpath as-path multipath-relax
 neighbor eth1 interface remote-as 65100
 neighbor eth1 description S1
 neighbor eth2 interface remote-as 65100
 neighbor eth2 description S2
 !
 address-family ipv4 unicast
  network 10.0.0.1/32
  neighbor eth1 activate
  neighbor eth2 activate
 exit-address-family
 !
 address-family l2vpn evpn
  neighbor eth1 activate
  neighbor eth2 activate
  advertise-all-vni
  vni 101000
   rd 10.0.0.1:1000
   route-target import 65000:1000
   route-target export 65000:1000
  exit-vni
  advertise-svi-ip
  advertise ipv4 unicast
 exit-address-family
exit
{{</printout>}}

As this is the first FRRouting configuration in this series, let's walk through it:

* Lines 2-4: Defaults
* Lines 5-8: Configuring interface EBGP neighbors. We could use **neighbor remote-as external** in a manually-crafted configuration.
* Lines 10-14: We decided to configure an explicit IPv4 address family, so we must activate the EBGP neighbors.
* Lines 17-18: We must activate the EVPN address family for the EBGP neighbors.
* Lines 20-24: Defining a layer-2 VXLAN segment. Route distinguisher and route targets have static values.
* Line 25: The router should advertise its IP address in an EVPN update (not relevant for this lab)
* Line 26: The router should redistribute IPv4 unicast prefixes into EVPN type-5 routing updates (irrelevant for this lab).

And this is the functionally equivalent L1 configuration for Arista EOS. The spine configuration is almost identical; Arista EOS requires no extra nerd knobs for EBGP EVPN sessions.

{{<printout>}}
router bgp 65001
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor ebgp_intf_Ethernet1 peer group
   neighbor ebgp_intf_Ethernet1 remote-as 65100
   neighbor ebgp_intf_Ethernet1 description S1
   neighbor ebgp_intf_Ethernet1 send-community standard extended large
   neighbor ebgp_intf_Ethernet2 peer group
   neighbor ebgp_intf_Ethernet2 remote-as 65100
   neighbor ebgp_intf_Ethernet2 description S2
   neighbor ebgp_intf_Ethernet2 send-community standard extended large
   neighbor interface Et1 peer-group ebgp_intf_Ethernet1
   neighbor interface Et2 peer-group ebgp_intf_Ethernet2
   !
   vlan 1000
      rd 10.0.0.1:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   address-family evpn
      neighbor ebgp_intf_Ethernet1 activate
      neighbor ebgp_intf_Ethernet2 activate
   !
   address-family ipv4
      neighbor ebgp_intf_Ethernet1 activate
      neighbor ebgp_intf_Ethernet1 next-hop address-family ipv6 originate
      neighbor ebgp_intf_Ethernet2 activate
      neighbor ebgp_intf_Ethernet2 next-hop address-family ipv6 originate
      network 10.0.0.1/32
{{</printout>}}

Let's walk through the extra configuration we had to make:

* Lines 5-12: We must create peer groups for interface EBGP sessions. A single peer group would be good enough; netlab creates a different peer group for every EBGP peer to be able to apply per-peer routing policies.
* Lines 13-14: We create interface peers
* Lines 28,30: IPv4 address family will use IPv6 next hops (interface EBGP sessions use [RFC 8950](https://datatracker.ietf.org/doc/html/rfc8950)).

The Arista EOS configuration is a bit more verbose than FRRouting, but not too bad.

You can view [complete configurations for all switches](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ebgp/) on GitHub.

### Does It Work?

Of course, it does, or I would be fixing configuration templates instead of writing a blog post. The EVPN updates sent from L1 to S1/S2 are forwarded almost intact[^CLA] to the other leaf switches.

[^CLA]: Apart from a longer AS path

The following printout shows L2's view of one of the EVPN routes advertised from L1. Note that we have two identical EVPN routes in the BGP table; L1 is advertising its routes to S1 and S2, and they forward them to L2.

{{<printout>}}
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65002
BGP routing table entry for mac-ip aac1.ab83.733e, Route Distinguisher: 10.0.0.1:1000
 Paths: 2 available
  65100 65001
    10.0.0.1 from fe80::50dc:caff:fefe:602%Et2 (10.0.0.6)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, external, ECMP head, ECMP, best, ECMP contributor
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000 ESI: 0000:0000:0000:0000:0000
  65100 65001
    10.0.0.1 from fe80::50dc:caff:fefe:502%Et1 (10.0.0.5)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, external, ECMP, ECMP contributor
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000 ESI: 0000:0000:0000:0000:0000
{{</printout>}}

The only significant change from the IBGP case is the BGP next-hop information (lines 7 and 12):

* The next hop is the L1 VTEP (10.0.0.1)
* The router advertising the route has an IPv6 link-local address
* The router ID of the router advertising the router is the loopback interface of S1/S2.

### Was It Worth the Effort?

**TL&DR:** Meh. The only "benefit" claimed by people who like this design is a single routing protocol.

I would use this design with a device using the FRRouting control plane. I might use it with other devices if the vendor rep can point me to a relevant "validated design" and the configuration is not too cumbersome (Arista EOS is OK).

Caveats[^NXOS]? Extra nerd knobs? Run away and use IBGP-over-IGP.

[^NXOS]: Cisco Nexus OS documentation still claims that "In a VXLAN EVPN setup that has 2K VNI scale configuration, the control plane downtime may take more than 200 seconds. To avoid potential BGP flap, extend the graceful restart time to 300 seconds." I'm unsure whether that would apply to an EBGP session restart due to a link flap, but it might explain why they're talking about EVPN EBGP sessions between loopback interfaces.

{{<next-in-series page="/posts/2024/10/evpn-designs-ebgp-ebgp.md" />}}

### Revision History

2024-10-10
: Removed the unnecessary IBGP session between S1 and S2 based on the [feedback by AW](https://blog.ipspace.net/2024/10/evpn-designs-ebgp/#2436).
