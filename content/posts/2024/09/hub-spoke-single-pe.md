---
title: "Hub-and-Spoke VPN on a Single PE-Router"
date: 2024-09-17 07:59:00+0200
tags: [ netlab, VPN, design ]
netlab_tag: vlan_vrf
series: hub_spoke_vpn
---
[Yesterday's blog post](/2024/09/hub-spoke-vpn-topology/) discussed the traffic flow and the routing information flow in a hub-and-spoke VPN design (a design in which all traffic between spokes flows through the hub site). It's time to implement and test it, starting with the simplest possible scenario: a single PE router using inter-VRF route leaking to connect the VRFs.
<!--more-->
{{<figure src="/2024/09/hub-spoke-single-pe.png">}}

Here's the baseline [_netlab_](https://netlab.tools/) lab topology we'll use:

{{<printout>}}
defaults.device: eos
provider: clab

groups:
  ce:
    device: frr
    members: [ ce_s1, ce_s2, ce_hub ]

vrfs:
  s_1:
    links: [ pe-ce_s1 ]
  s_2:
    links: [ pe-ce_s2 ]
  hub_ingress:
    links: [ pe-ce_hub ]
  hub_egress:
    links: [ pe-ce_hub ]

nodes:
  pe:
    module: [ bgp, vrf ]
    bgp.as: 65000
  ce_hub:
  ce_s1:
  ce_s2:
{{</printout>}}

**Notes**

* We'll use cEOS as the PE-router (lines 1-2) and FRR containers as the CE-routers (lines 4-7)
* We need four VRFs (s_1, s_2, hub_ingress, hub_egress) and a link in every VRF (lines 9-17)
* We need the VRF and the BGP configuration module on the PE router. We also have to specify the BGP AS number for the PE router (lines 19-22)

Next, let's add the PE-CE routing protocol. We'll use BGP to see the nodes (AS numbers) a route traverses. All we have to add to the lab topology is the BGP configuration module on all devices and the BGP AS numbers for the CE routers. _netlab_ will take care of EBGP sessions.

{{<printout>}}
module: [ bgp ]

nodes:
  pe:
    bgp.as: 65000
  ce_hub:
    bgp.as: 65100
  ce_s1:
    bgp.as: 65101
  ce_s2:
    bgp.as: 65102
{{</printout>}}

Finally, we need route leaking between VRFs. Let's use the diagram from the previous blog post as a reminder:

{{<figure src="/2024/09/hub-spoke-as-override.png">}}

In a nutshell:

* All spoke routes must be exported to the `hub_egress` VRF.
* Spoke VRFs have to import routes from the `hub_ingress` VRF.

Here's the relevant lab topology snippet:

{{<printout>}}
vrfs:
  s_1:
    export: [ hub_egress ]
    import: [ hub_ingress ]
  s_2:
    export: [ hub_egress ]
    import: [ hub_ingress ]
{{</printout>}}

Finally, we need the AS-override configured on the EBGP session in the `hub_ingress` VRF. We have to add the **bgp_session** plugin to the lab topology and **bgp.as_override** to the `ce_hub` part of the `hub_ingress` link:

{{<printout>}}
plugin: [ bgp.session ]

vrfs:
  hub_ingress:
    links:
    - pe:
      ce_hub:
        bgp.as_override: True
{{</printout>}}

The [complete lab topology](https://github.com/ipspace/netlab-examples/blob/master/VRF/vrf-hub-spoke/topology.yml) is available in the [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples/).

### Kicking the Tires

Let's start the lab. The easiest way to do it is to:

* [Open the netlab-examples repository in a GitHub Codespace](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/)
* [Copy the cEOS container into the codespace](https://blog.ipspace.net/2024/07/arista-eos-codespaces/)
* Change directory to `VRF/vrf-hub-spoke`
* Execute **netlab up**

Alternatively, you could execute **netlab up -d frr** if you don't want to waste time with Arista cEOS containers.

Done? Let's look at the results. Here's the BGP table on CE_S1:

```
$ netlab connect ce_s1 --show ip bgp
Connecting to container clab-vrf-hub-spok-ce_s1, executing vtysh -c "show ip bgp"
BGP table version is 7, local router ID is 10.0.0.3, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
 *> 10.0.0.2/32      10.1.0.2                               0 65000 65100 i
 *> 10.0.0.3/32      0.0.0.0(ce_s1)           0         32768 i
 *> 10.0.0.4/32      10.1.0.2                               0 65000 65100 65100 65102 i
 *> 10.1.0.0/30      10.1.0.2                               0 65000 i
 *> 10.1.0.4/30      10.1.0.2                               0 65000 65100 65100 i
 *> 10.1.0.8/30      10.1.0.2                               0 65000 i
 *> 10.1.0.12/30     10.1.0.2                               0 65000 65100 65100 i
```

Knowing the lab addressing scheme would make the decoding process easier, so here it is:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **ce_hub** |  10.0.0.2/32 |  | Loopback |
| eth1 | 10.1.0.9/30 |  | ce_hub -> pe |
| eth2 | 10.1.0.13/30 |  | ce_hub -> pe |
| **ce_s1** |  10.0.0.3/32 |  | Loopback |
| eth1 | 10.1.0.1/30 |  | ce_s1 -> pe |
| **ce_s2** |  10.0.0.4/32 |  | Loopback |
| eth1 | 10.1.0.5/30 |  | ce_s2 -> pe |
| **pe** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | pe -> ce_s1 (VRF: s_1) |
| Ethernet2 | 10.1.0.6/30 |  | pe -> ce_s2 (VRF: s_2) |
| Ethernet3 | 10.1.0.10/30 |  | pe -> ce_hub (VRF: hub_ingress) |
| Ethernet4 | 10.1.0.14/30 |  | pe -> ce_hub (VRF: hub_egress) |
{.fmtTable}

CE_S1 received routes for the loopback addresses of CE_S2 (10.0.0.4/32) and CE_HUB (10.0.0.2/32), as well as the routes for the connecting subnets[^TWCH]. The AS path attached to the CE_S2 prefix contains 65102 (CE_S2), two copies of 65100 (PE AS changed by the CE_HUB plus the CE_HUB AS), and 65000 (PE). The routing information exchange works.

[^TWCH]: That will come in handy when we run **traceroute**; figuring out why we need the connecting subnets is left as an exercise for the reader.

Let's run **traceroute** from CE_S1 to CE_S2:

```
$ netlab connect ce_s1 traceroute ce_s2
Connecting to container clab-vrf-hub-spok-ce_s1, executing traceroute ce_s2
traceroute to ce_s2 (10.0.0.4), 30 hops max, 46 byte packets
 1  pe-s_1 (10.1.0.2)  0.003 ms  0.001 ms  0.001 ms
 2  ce_hub (10.1.0.13)  0.787 ms  0.139 ms  0.079 ms
 3  pe-hub_egress (10.1.0.14)  0.062 ms  0.045 ms  0.043 ms
 4  ce_s2 (10.0.0.4)  0.172 ms  0.140 ms  0.135 ms
```

The printout tells us that the packets traverse `s_1` VRF on PE, CE_HUB, and `hub_egress` VRF on PE before arriving at CE_S2. Mission accomplished.

{{<next-in-series page="/posts/2024/09/hub-spoke-evpn.html">}}
Now that we know how to implement hub-and-spoke VPN on a single PE router, it's trivial to migrate the design to an MPLS/VPN or EVPN network. All we have to do is stretch the VRFs across multiple PE routers; the topic of the next blog post in this series.
{{</next-in-series>}}

### Reference Information

This is the relevant part of the PE configuration. It was generated exclusively with _netlab_ configuration templates; all I did was run **netlab up** and enjoy the results.

```
vrf instance hub_egress
   rd 65000:4
!
vrf instance hub_ingress
   rd 65000:3
!
vrf instance s_1
   rd 65000:1
!
vrf instance s_2
   rd 65000:2
!
interface Ethernet1
   description pe -> ce_s1 [external]
   vrf s_1
   ip address 10.1.0.2/30
!
interface Ethernet2
   description pe -> ce_s2 [external]
   vrf s_2
   ip address 10.1.0.6/30
!
interface Ethernet3
   description pe -> ce_hub [external]
   vrf hub_ingress
   ip address 10.1.0.10/30
!
interface Ethernet4
   description pe -> ce_hub [external]
   vrf hub_egress
   ip address 10.1.0.14/30
!
interface Loopback0
   ip address 10.0.0.1/32
!
interface Management0
   vrf management
   ip address 192.168.121.101/24
   no lldp transmit
   no lldp receive
!
ip routing
ip routing vrf hub_egress
ip routing vrf hub_ingress
ip routing vrf s_1
ip routing vrf s_2
!
mpls ip
!
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   network 10.0.0.1/32
   !
   vrf hub_egress
      rd 65000:4
      route-target import vpn-ipv4 65000:4
      route-target export vpn-ipv4 65000:4
      router-id 10.0.0.1
      neighbor 10.1.0.13 remote-as 65100
      neighbor 10.1.0.13 description ce_hub
      neighbor 10.1.0.13 send-community standard large
      !
      address-family ipv4
         neighbor 10.1.0.13 activate
         redistribute connected
   !
   vrf hub_ingress
      rd 65000:3
      route-target import vpn-ipv4 65000:3
      route-target export vpn-ipv4 65000:3
      router-id 10.0.0.1
      neighbor 10.1.0.9 remote-as 65100
      neighbor 10.1.0.9 description ce_hub
      neighbor 10.1.0.9 send-community standard large
      !
      address-family ipv4
         neighbor 10.1.0.9 activate
         redistribute connected
   !
   vrf s_1
      rd 65000:1
      route-target import vpn-ipv4 65000:3
      route-target export vpn-ipv4 65000:4
      router-id 10.0.0.1
      neighbor 10.1.0.1 remote-as 65101
      neighbor 10.1.0.1 description ce_s1
      neighbor 10.1.0.1 send-community standard large
      !
      address-family ipv4
         neighbor 10.1.0.1 activate
         redistribute connected
   !
   vrf s_2
      rd 65000:2
      route-target import vpn-ipv4 65000:3
      route-target export vpn-ipv4 65000:4
      router-id 10.0.0.1
      neighbor 10.1.0.5 remote-as 65102
      neighbor 10.1.0.5 description ce_s2
      neighbor 10.1.0.5 send-community standard large
      !
      address-family ipv4
         neighbor 10.1.0.5 activate
         redistribute connected
```
