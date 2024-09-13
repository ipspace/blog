---
title: "Common Services VRF with EVPN Control Plane"
date: 2024-08-29 07:49:00+0200
tags: [ EVPN, netlab ]
netlab_tag: vxlan_evpn
evpn_tag: vpn_topo
---
After discovering that some EVPN implementations support multiple transit VNI values in a single VRF, I had to check whether I could implement a _common services_ L3VPN with EVPN.

{{<note info>}}A *common services* VPN is a VPN in which server sites can communicate with each other and the clients, but the clients cannot communicate between themselves.{{</note>}}

**TL&DR:** It works (on Arista cEOS)[^OW].

[^OW]: However, you might be the only one in the world doing it and might hit unexpected bugs. I might also be overly pessimistic; if you're using something similar in production, please leave a comment.

Here are the relevant parts of a _[netlab](https://netlab.tools/)_ lab topology I used in my test (you can find the complete lab topology in [_netlab-examples_ GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/EVPN/l3vpn-cs)):
<!--more-->
{{<printout>}}
module: [ ospf, bgp, vrf, vlan, vxlan, evpn ]
bgp.as: 65000

groups:
  _auto_create: True
  switches:
    members: [ s1, s2, s3 ]
  hosts:
    device: linux
    members: [ h1, h2, cs ]

vrfs:
  spoke:
    links: [ h1-s1, h2-s2 ]
    evpn.transit_vni: True
    export: spoke
    import: hub
  hub:
    links: [ cs-s3 ]
    evpn.transit_vni: True
    export: hub
    import: [ hub, spoke ]
{{</printout>}}

You'll find a detailed explanation of various topology elements in the [Building Layer-3-Only EVPN Lab](/2024/08/netlab-layer-3-only-evpn/) blog post. That blog post also describes how to start the lab or use lab devices from other vendors.

**Notes:**

* I used two VRFs (_hub_ and _spoke_).
* Hub VRF imports _hub_ and _spoke_ prefixes. Devices attached to the _hub_ VRF (CS) can communicate with all other devices.
* Spoke VRFs import only the _hub_ prefixes. Devices attached to a _spoke_ VRF (H1, H2) can thus communicate with devices attached to the _hub_ VRF but not with other spoke devices.
* The only exception to the above rule is the spoke devices attached to the same VRF instance. If you want to prevent all inter-spoke communication, attach every spoke device to a different VRF.

Here's the relevant Arista EOS configuration. Note the mismatch between **import evpn** and **export evpn** values on S1, and multiple **import evpn** values on S3.

{{<cc>}}EVPN-related configuration on S1{{</cc>}}
```
vrf instance spoke
   rd 65000:1
!
!
interface Ethernet3
   description s1 -> h1 [stub]
   vrf spoke
   ip address 172.16.0.1/24
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vrf spoke vni 200000
!
router bgp 65000
   !
   vrf spoke
      rd 65000:1
      route-target import evpn 65000:2
      route-target export evpn 65000:1
      redistribute connected
```

{{<cc>}}EVPN-related configuration on S3{{</cc>}}
```
vrf instance hub
   rd 65000:2
!
interface Ethernet3
   description s3 -> cs [stub]
   vrf hub
   ip address 172.16.2.3/24
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vrf hub vni 200001
!
router bgp 65000
   !
   vrf hub
      rd 65000:2
      route-target import evpn 65000:1
      route-target import evpn 65000:2
      route-target export evpn 65000:2
      redistribute connected
```

### Test Results

Every PE device advertises a single IP prefix. IP prefixes carry the expected RT communities:

```
s3>show bgp evpn detail
BGP routing table information for VRF default
Router identifier 10.0.0.3, local AS number 65000
BGP routing table entry for ip-prefix 172.16.0.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.1 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:4e:42:aa
      VNI: 200000
BGP routing table entry for ip-prefix 172.16.1.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:a6:f6:a6
      VNI: 200000
BGP routing table entry for ip-prefix 172.16.2.0/24, Route Distinguisher: 65000:2
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best, redistributed (Connected)
      Extended Community: Route-Target-AS:65000:2 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:01:aa:de
      VNI: 200001
```

The _hub_ VRF imports prefixes with RT 65000:1 and RT 65000:2. The _hub_ routing table contains the expected three prefixes:

```
s3>show ip route vrf hub | begin Gateway
Gateway of last resort is not set

 B I      172.16.0.0/24 [200/0]
           via VTEP 10.0.0.1 VNI 200000 router-mac 00:1c:73:4e:42:aa local-interface Vxlan1
 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 200000 router-mac 00:1c:73:a6:f6:a6 local-interface Vxlan1
 C        172.16.2.0/24
           directly connected, Ethernet3
```

The _spoke_ VRF imports only prefixes with RT 65000:2. As expected, the _spoke_ VRF on S1 (or S2) contains only two prefixes:

```
s1>show ip route vrf spoke | begin Gateway
Gateway of last resort is not set

 C        172.16.0.0/24
           directly connected, Ethernet3
 B I      172.16.2.0/24 [200/0]
           via VTEP 10.0.0.3 VNI 200001 router-mac 00:1c:73:01:aa:de local-interface Vxlan1
```

Finally, I added validation rules to the lab topology and ran the validation tests:

{{<figure src="/2024/08/evpn-cs-validation.png">}}
