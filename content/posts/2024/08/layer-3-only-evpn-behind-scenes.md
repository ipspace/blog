---
title: "Layer-3-Only EVPN: Behind the Scenes"
date: 2024-08-13 10:08:00+0200
tags: [ EVPN ]
evpn_tag: designs
---
In the [previous blog post](/2024/08/netlab-layer-3-only-evpn/), I described how to build a lab to explore the layer-3-only EVPN design and asked you to do that and figure out what's going on behind the scenes. If you didn't find time for that, let's do it together in this blog post. To keep it reasonably short, we'll focus on the EVPN control plane and leave the exploration of the data-plane data structures for another blog post.

The most important thing to understand when analyzing a layer-3-only EVPN/VXLAN network is that the data plane looks like a VRF-lite design: each VRF uses a hidden VLAN (implemented with VXLAN) as the transport VLAN between the PE devices.
<!--more-->
{{<figure src="/2024/08/evpn-l3vpn-data-plane.png">}}

Don't believe me? Let's [start the lab](/2024/08/netlab-layer-3-only-evpn/) (using Arista cEOS containers) and check whether that's true ;)

### Device Configuration

Before starting our journey, let's review the relevant parts of the Arista cEOS device configuration (taken from S1):

{{<printout>}}
vrf instance blue
   rd 65000:2
!
vrf instance red
   rd 65000:1
!
interface Ethernet1
   description s1 -> s2
   mtu 1600
   mac-address 52:dc:ca:fe:01:01
   no switchport
   ip address 10.1.0.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2
   description s1 -> h1 [stub]
   mac-address 52:dc:ca:fe:01:02
   no switchport
   vrf red
   ip address 172.16.0.1/24
!
interface Ethernet3
   description s1 -> h3 [stub]
   mac-address 52:dc:ca:fe:01:03
   no switchport
   vrf blue
   ip address 172.16.2.1/24
!
interface Loopback0
   ip address 10.0.0.1/32
   ip ospf area 0.0.0.0
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vrf blue vni 200001
   vxlan vrf red vni 200000
!
ip routing
ip routing vrf blue
ip routing vrf red
!
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description s2
   neighbor 10.0.0.2 send-community standard extended large
   !
   address-family evpn
      neighbor 10.0.0.2 activate
   !
   !
   vrf blue
      rd 65000:2
      route-target import evpn 65000:2
      route-target export evpn 65000:2
      redistribute connected
   !
   vrf red
      rd 65000:1
      route-target import evpn 65000:1
      route-target export evpn 65000:1
      redistribute connected
{{</printout>}}

* Lines 1-5: We have two VRFs (red and blue)
* Lines 7-14: The link between the switches is a P2P link with a larger MTU. We're running P2P OSPF to speed up the convergence.
* Lines 16-28: The host-to-switch links are layer-3 links in VRFs red and blue
* Lines 37-38: We need transit VNI for the blue and red VRF
* Lines 44-51: We have an IBGP neighbor
* Lines 53-54: We're exchanging EVPN routes with that IBGP neighbor
* Lines 57-67: Defining RD/RT values for the two VRFs. We're also redistributing connected subnets into BGP.

### Let's Start Exploring

Using the **show vlan** command, it's trivial to confirm that the switches use two VLANs (one per EVPN transit VNI) on the VXLAN interface:

```
s1>show vlan
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active    Mt1
4093* VLAN4093                         active    Cpu, Vx1
4094* VLAN4094                         active    Cpu, Vx1

* indicates a Dynamic VLAN
```

Want to check that these are VXLAN-backed VLANs? Sure (notice how the VNI values match the values we defined in the `vxlan vrf vni` command):

```
s1>show vxlan vni
VNI to VLAN Mapping for Vxlan1
VNI       VLAN       Source       Interface       802.1Q Tag
--------- ---------- ------------ --------------- ----------

VNI to dynamic VLAN Mapping for Vxlan1
VNI          VLAN       VRF        Source
------------ ---------- ---------- ------------
200000       4094       red        evpn
200001       4093       blue       evpn
```

Now we know what the data-plane topology looks like. Next, let's focus on the forwarding tables:

```
s1>show ip route vrf red bgp
...

 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 200000 router-mac 00:1c:73:eb:d5:13 local-interface Vxlan1
```

As expected, the BGP (EVPN) route for 172.16.1.0/24 uses the VXLAN interface and the next-hop MAC address `00:1c:73:eb:d5:13`. There is no next-hop IP address (apart from remote VTEP), as the switches don't assign IP addresses to the transit VLAN.

Where does S1 get the remote MAC address? Glad you asked ;) Let's explore the EVPN routes for the red VRF:

```
s1#show bgp evpn rd 65000:1 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for ip-prefix 172.16.0.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best, redistributed (Connected)
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:ff:68:31
      VNI: 200000
BGP routing table entry for ip-prefix 172.16.1.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:eb:d5:13
      VNI: 200000
```

The EVPN transit tunnel encapsulation (VXLAN), VNI, and remote MAC address are encoded as extended BGP communities in every EVPN RT5 (IP prefix) update.

But why do we need the EVPN router MAC addresses on the transit VXLAN segment? Wouldn't the VNI and remote VTEP be good enough? Unfortunately, VXLAN is nothing more than a transport mechanism that carries Ethernet frames over UDP, and every Ethernet frame must have a source- and a destination MAC address.

Want to see those MAC addresses in the forwarding tables? Let's explore the VXLAN- and VLAN MAC address tables:

```
s1#show vxlan address-table
          Vxlan Mac Address Table
----------------------------------------------------------------------

VLAN  Mac Address     Type      Prt  VTEP             Moves   Last Move
----  -----------     ----      ---  ----             -----   ---------
4093  001c.73eb.d513  EVPN      Vx1  10.0.0.2         1       2:16:21 ago
4094  001c.73eb.d513  EVPN      Vx1  10.0.0.2         1       2:16:21 ago
s1#show mac address-table
          Mac Address Table
------------------------------------------------------------------

Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ---------
4093    001c.73eb.d513    DYNAMIC     Vx1        1       2:19:02 ago
4094    001c.73eb.d513    DYNAMIC     Vx1        1       2:19:01 ago
```

But where do the local MAC addresses come from? As you know, every VLAN (including the internal VLANs) has an associated VLAN interface on a layer-3 switch:

```
s1#show interfaces vlan4093
Vlan4093 is up, line protocol is up (connected)
  Hardware is Vlan, address is 001c.73ff.6831 (bia 001c.73ff.6831)
  No Internet protocol address assigned
  IPv6 link-local address is fe80::21c:73ff:feff:6831/64
  No IPv6 global unicast address is assigned
  IP MTU 9164 bytes (default)
  Up 2 hours, 20 minutes, 10 seconds
s1#show interfaces vlan4094
Vlan4094 is up, line protocol is up (connected)
  Hardware is Vlan, address is 001c.73ff.6831 (bia 001c.73ff.6831)
  No Internet protocol address assigned
  IPv6 link-local address is fe80::21c:73ff:feff:6831/64
  No IPv6 global unicast address is assigned
  IP MTU 9164 bytes (default)
  Up 2 hours, 20 minutes, 13 seconds
```

To recap:

* A layer-3 switch creates a VLAN for every VXLAN segment.
* A local (switch) MAC address is assigned to every VLAN segment (VLAN interface)[^NIH]. The same MAC address is usually used for all VLAN segments.
* The local MAC address and the transit VNI attached as extended BGP communities to every VRF IP prefix (RT5) EVPN route
* The remote MAC address and the associated transit VNI are used to build the forwarding entry on the ingress routers.

[^NIH]: And I have no idea what they use to make the lower 24 bits unique, particularly in a virtual environment where all the containers are cloned from the same image.

[^HWL]: Due to the way the forwarding structures are built

{{<next-in-series page="/posts/2024/08/multiple-transit-vni-evpn-vrf.html">}}Interestingly, the transit VNI does not have to match across the PE devices. More about that in another blog post; this one is already too long.{{</next-in-series>}}

