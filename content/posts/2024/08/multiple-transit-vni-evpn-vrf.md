---
title: "Using Multiple Transit VNIs per EVPN VRF"
date: 2024-08-22 08:48:00+0200
tags: [ EVPN ]
evpn_tag: details
---
After reading the [Layer-3-Only EVPN: Behind the Scenes](/2024/08/layer-3-only-evpn-behind-scenes/) blog post, one might come to an obvious conclusion: the per-VRF EVPN transit VNI must match across all PE devices forwarding traffic for that VRF.

Interestingly, at least some EVPN implementations handle multiple VNIs per VRF without a hitch; I ran my tests in a lab where three switches used unique per-switch VNI for a common VRF.

{{<note>}}The rest of this blog post describes Arista cEOS behavior; please feel free to use the same [_netlab_ topology](https://github.com/ipspace/netlab-examples/tree/master/EVPN/l3vpn-uvni) to [run similar tests on other devices](/2024/08/netlab-layer-3-only-evpn/#old).{{</note>}}
<!--more-->
### Starting the Lab

The [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/l3vpn-uvni/topology.yml) is as simple as I could make it (you'll find the detailed explanation in the [Building Layer-3-Only EVPN Lab](/2024/08/netlab-layer-3-only-evpn/) blog post). As _netlab_ doesn't allow you to use different VNI values within the same VRF, I wrote a [short plugin](https://github.com/ipspace/netlab-examples/blob/master/EVPN/l3vpn-uvni/unique_vni.py) that scrambles the VNI values at the end of the data transformation:

```
def post_transform(topo: Box) -> None:
  for name,node in topo.nodes.items():
    if 'vrfs' not in node:
      continue
    for vname,vdata in node.vrfs.items():
      if vdata.get('evpn.evi') and vdata.get('evpn.transit_vni'):
        vdata.evpn.transit_vni = 200000 + 100 * vdata.evpn.evi + node.id
```

If you want to run your own tests:

* [Open netlab-examples repository in GitHub Codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/)
* [Upload the cEOS container image](https://blog.ipspace.net/2024/07/arista-eos-codespaces/)
* Change directory to `EVPN/l3vpn-uvni`
* Execute **netlab up**
* Wait a bit and execute **netlab validate** to check that the hosts can ping each other.

### EVPN Control Plane

EVPN shouldn't care about the VNI values you configure on individual PE devices; it should advertise whatever is configured as extended BGP communities. Thus, you should see three RT5 EVPN prefixes with RD 65000:1 (the RD for the red VRF) on every lab switch: a local prefix and two remote prefixes. Every prefix should have a different VNI value:

```
s1>show bgp evpn detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for ip-prefix 172.16.0.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best, redistributed (Connected)
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:ca:8b:41
      VNI: 200101
BGP routing table entry for ip-prefix 172.16.1.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:b0:63:de
      VNI: 200102
BGP routing table entry for ip-prefix 172.16.2.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:ed:c6:7f
      VNI: 200103
```

The VNI values should be copied into the IP routing table for the red VRF:

```
s1>show ip route vrf red|begin Gateway
Gateway of last resort is not set

 C        172.16.0.0/24
           directly connected, Ethernet3
 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 200102 router-mac 00:1c:73:b0:63:de local-interface Vxlan1
 B I      172.16.2.0/24 [200/0]
           via VTEP 10.0.0.3 VNI 200103 router-mac 00:1c:73:ed:c6:7f local-interface Vxlan1
```

Now for the crucial question: How does Arista cEOS set up the data plane?

### Exploring the Data Plane

Let's start with the VXLAN VNIs. Every device creates three VNIs: one for the incoming traffic (local VNI) and two for the outgoing traffic.

```
s1>show vxlan vni
VNI to VLAN Mapping for Vxlan1
VNI       VLAN       Source       Interface       802.1Q Tag
--------- ---------- ------------ --------------- ----------

VNI to dynamic VLAN Mapping for Vxlan1
VNI          VLAN       VRF       Source
------------ ---------- --------- ------------
200101       4094       red       evpn
200102       4093                 evpn
200103       4092                 evpn
```

The "local" VNI (200101) is connected to the red VRF; traffic received on that VNI will be forwarded using the red VRF's IP forwarding table. The other two VNIs are not associated with any routing table; incoming IP traffic (there shouldn't be any) will probably be dropped.

Not surprisingly, the VLAN table mirrors the VXLAN VNI allocation:

```
s1>show vlan
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active    Mt1
4092* VLAN4092                         active    Cpu, Vx1
4093* VLAN4093                         active    Cpu, Vx1
4094* VLAN4094                         active    Cpu, Vx1
```

Finally, the VXLAN and the VLAN MAC address tables contain the remote router MAC addresses (one per VNI/VLAN):

```
s1>show vxlan address-table
          Vxlan Mac Address Table
----------------------------------------------------------------------

VLAN  Mac Address     Type      Prt  VTEP             Moves   Last Move
----  -----------     ----      ---  ----             -----   ---------
4092  001c.73ed.c67f  EVPN      Vx1  10.0.0.3         1       0:23:40 ago
4093  001c.73b0.63de  EVPN      Vx1  10.0.0.2         1       0:23:40 ago
Total Remote Mac Addresses for this criterion: 2
s1>show mac address-table
          Mac Address Table
------------------------------------------------------------------

Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ---------
4092    001c.73ed.c67f    DYNAMIC     Vx1        1       0:24:13 ago
4093    001c.73b0.63de    DYNAMIC     Vx1        1       0:24:13 ago
Total Mac Addresses for this criterion: 2
```

**To recap:**

* At least some EVPN implementations graciously handle multiple transit EVPN VNIs per VRF.
* A separate VLAN is created for every unique VNI value the peer PE devices advertised.
* As you're usually limited to 4096 VLANs per switch, you might run out of VLANs in large deployments.

**TL&DR:** Just because you could doesn't mean that you should. 

{{<next-in-series page="/posts//2024/08/evpn-common-services-vrf.html">}}However, you could use this capability to implement common-services VRFs with EVPN. More about that in another blog post.{{</next-in-series>}}
