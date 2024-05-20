---
title: "EVPN Designs: IBGP Full Mesh Between Leaf Switches"
series_title: "IBGP Full Mesh Between Leaf Switches"
date: 2024-05-23 07:52:00+0100
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the [previous blog post](/2024/04/evpn-designs-vxlan-leaf-spine-fabric.html) in the EVPN Designs series, we explored the simplest possible VXLAN-based fabric design: static ingress replication without any L2VPN control plane. This time, we'll add the simplest possible EVPN control plane: a full mesh of IBGP sessions between the leaf switches.

{{<note warn>}}This blog post describes an initial BGP design that we'll refine in subsequent blog posts. Having a full mesh of IBGP sessions between leaf switches is a bad idea unless you have a tiny fabric or you're deploying a small-scale EVPN pilot.{{</note>}}
<!--more-->
This is the fabric we're working with:

{{<figure src="/2024/04/evpn-design-fabric.png" caption="Leaf-and-spine fabric with two VLANs">}}

And this is how we'll use routing protocols in our fabric:

* Leaf- and spine switches are running OSPF
* There's a full mesh of IBGP sessions between the leaf switches.
* IBGP is used solely to transport EVPN address family.

{{<figure src="/2024/05/evpn-design-ibgp-full-mesh.png" caption="Full mesh of IBGP sessions between the leaf switches">}}

Let's set up a lab and try it out. We'll use a lab setup similar to the [VXLAN-only fabric](/2024/04/evpn-designs-vxlan-leaf-spine-fabric.html); read that blog post (in particular the *[Creating the Lab Environment](/2024/04/evpn-designs-vxlan-leaf-spine-fabric.html#lab)* section) to get started.

### Leaf-and-Spine Lab Topology

This is the _netlab_ lab topology description we'll use to set up IBGP full mesh carrying EVPN updates in our leaf-and-spine fabric.

{{<printout>}}
defaults.device: eos
provider: clab

plugin: [ fabric ]
fabric.spines: 2
fabric.leafs: 4

bgp.as: 65000
bgp.activate.ipv4: []

groups:
  _auto_create: True
  leafs:
    module: [ ospf, bgp, vlan, vxlan, evpn ]
  spines:
    module: [ ospf ]
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

Most of the topology file is [explained in the previous blog post](/2024/04/evpn-designs-vxlan-leaf-spine-fabric.html#topo); all we had to do to get from a VXLAN fabric to a full-blown EVPN fabric were three changes[^SPO]:

* Line 8: The BGP AS number used in the lab[^BAG]
* Line 9: Our fabric will have BGP sessions between IPv4 loopback addresses, but we'll not run the IPv4 address family over these sessions.
* Line 14: We also run BGP and EVPN on the leaf switches.

[^BAG]: The BGP AS number has to be specified as a global parameter, or the EVPN module won't be able to use it to set route targets or route distinguishers.

[^SPO]: Sometimes it pays off to have a flexible high-level tool ;)

Assuming you already did the previous homework, starting the lab is time.

### Behind the Scenes

This is the relevant part of the configuration of L1 running Arista EOS (you can view complete configurations for all switches on GitHub).

{{<printout>}}
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description L2
   neighbor 10.0.0.2 send-community standard extended large
   neighbor 10.0.0.3 remote-as 65000
   neighbor 10.0.0.3 update-source Loopback0
   neighbor 10.0.0.3 description L3
   neighbor 10.0.0.3 send-community standard extended large
   neighbor 10.0.0.4 remote-as 65000
   neighbor 10.0.0.4 update-source Loopback0
   neighbor 10.0.0.4 description L4
   neighbor 10.0.0.4 send-community standard extended large
   !
   vlan 1000
      rd 10.0.0.1:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   address-family evpn
      neighbor 10.0.0.2 activate
      neighbor 10.0.0.3 activate
      neighbor 10.0.0.4 activate
   !
   address-family ipv4
      network 10.0.0.1/32
{{</printout>}}

Let's walk through the changes:

* Line 1: We're starting a BGP routing process. 
* Line 3: We're not activating the IPv4 address family when configuring an IPv4 BGP neighbor.
* Lines 2 and 4: _netlab_ sets a few parameters to ensure a working BGP configuration under all circumstances. These parameters are not relevant to our discussion.
* Lines 5-16: We have to define the IBGP neighbors (all other leaf switches)
* Line 18: Configuring a VLAN under the BGP routing process creates an EVPN instance (MAC VRF) on Arista EOS.
* Lines 19-21: _netlab_ manages EVPN route targets and route distinguishers. You could use **rd auto**; Arista EOS documentation claims you could use automatic route targets, but I couldn't find the corresponding configuration command.
* Lines 24-27: We must exchange EVPN routes with other leaf switches. 

### Does It Work?

Let's look around a bit. BGP neighbors are active, and they're exchanging BGP prefixes:

```
L1>show bgp evpn summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  L2                       10.0.0.2 4 65000             39        39    0    0 00:26:08 Estab   2      2
  L3                       10.0.0.3 4 65000             39        39    0    0 00:26:10 Estab   2      2
  L4                       10.0.0.4 4 65000             39        38    0    0 00:26:10 Estab   2      2
```

Each leaf switch is advertising a single MAC address (H1 through H4) and a VTEP IP address (*imet* route) that should be used for BUM flooding.

```
L1>show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.4:1001 mac-ip aac1.ab45.fdc3
                                 10.0.0.4              -       100     0       i
 * >      RD: 10.0.0.1:1000 mac-ip aac1.ab4a.93bb
                                 -                     -       -       0       i
 * >      RD: 10.0.0.2:1001 mac-ip aac1.aba9.4d50
                                 10.0.0.2              -       100     0       i
 * >      RD: 10.0.0.3:1000 mac-ip aac1.abbc.7c69
                                 10.0.0.3              -       100     0       i
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 -                     -       -       0       i
 * >      RD: 10.0.0.2:1001 imet 10.0.0.2
                                 10.0.0.2              -       100     0       i
 * >      RD: 10.0.0.3:1000 imet 10.0.0.3
                                 10.0.0.3              -       100     0       i
 * >      RD: 10.0.0.4:1001 imet 10.0.0.4
                                 10.0.0.4              -       100     0       i
```

The *imet* routes are used to build the ingress replication lists:

```
L1>show vxlan vtep detail
Remote VTEPS for Vxlan1:

VTEP           Learned Via         MAC Address Learning       Tunnel Type(s)
-------------- ------------------- -------------------------- --------------
10.0.0.3       control plane       control plane              unicast, flood

Total number of remote VTEPS:  1
```

The *mac-ip* routes are used to build VLAN MAC address tables:

```
L1#show mac address-table
L1>show mac address-table vlan 1000
          Mac Address Table
------------------------------------------------------------------

Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ---------
1000    aac1.ab4a.93bb    DYNAMIC     Et3        1       0:03:11 ago
1000    aac1.abbc.7c69    DYNAMIC     Vx1        1       0:03:11 ago
Total Mac Addresses for this criterion: 2
```

The MAC address reachable over the VXLAN interface sits behind VTEP 10.0.0.3. L3 advertised it to L1 in an EVPN update.

```
L1>show vxlan address-table
          Vxlan Mac Address Table
----------------------------------------------------------------------

VLAN  Mac Address     Type      Prt  VTEP             Moves   Last Move
----  -----------     ----      ---  ----             -----   ---------
1000  aac1.abbc.7c69  EVPN      Vx1  10.0.0.3         1       0:03:27 ago
Total Remote Mac Addresses for this criterion: 1
```

### Was It Worth the Effort?

**TL&DR:** Barely

Let's start with the **benefits**:

* The ingress replication lists are built automatically.
* Each VLAN (EVPN instance) has an independent ingress replication list, which means that the client traffic is flooded only to the VTEPs with a compatible (according to route targets) EVPN instance. That's a massive win in Carrier Ethernet networks where a customer port often has a single VLAN. It is somewhat irrelevant in data center environments where we [usually configure every VLAN on every server port](https://blog.ipspace.net/2011/12/vm-aware-networking-improves-iaas-cloud.html) so we don't have to talk with the server team.

What about the **drawbacks**?

* We introduced a new routing protocol and a new technology. While it looks simple, it might be fun trying to troubleshoot it at the proverbial 2 AM on a Sunday morning.
* The configurations can become quite lengthy unless you generate them automatically. Whether you are ready to do that is a different question[^AE].
* Managing the full mesh of IBGP sessions is obviously a nightmare. However, things will improve once we add route reflectors.

[^AE]: Regardless of what the automation evangelists (myself included) tell you.

Should you choose EVPN when building a small data center that provides VLAN connectivity? Probably not[^NT]. EVPN starts to make sense when you use advanced features like proxy ARP, multi-subnet VRFs, or the [much-praised active-active multihoming](/2022/11/mlag-vxlan-evpn.html)[^AAMH].

[^NT]: Unless you want to play with a new toy or boost your resume.

[^AAMH]: The server team might [not want the link aggregation anyway](https://blog.ipspace.net/2014/01/vsphere-does-not-need-lag-bandaids.html). Most virtualization solutions are happier with multiple independent uplinks.
