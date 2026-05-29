---
title: "EVPN Centralized Routing with Arista EOS"
subtitle: "TL&DR: SIP of Networking Was an Understatement 🤦‍♂️"
date: 2026-06-03 07:44:00+0200
tags: [ evpn ]
evpn_tag: details
---
A month ago, I described [ARP issues in EVPN centralized routing design](/2026/05/arp-issues-evpn-central-routing/), and Naveen Kumar Devaraj was kind enough to add some [Arista EOS implementation details](https://blog.ipspace.net/2026/05/arp-issues-evpn-central-routing/#2976). Today, let's explore what EVPN routes Arista EOS generates in that scenario. We'll use a [very simple lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/central-routing/topology.yml) with a spine switch acting as a router. The leaf switches are layer-2 switches.

{{<figure src="/2026/05/evpn-fwd-central-routing.png" caption="Packet forwarding in centralized routing design">}}
<!--more-->
When the lab is started, all switches advertise IMET routes for the attached VLANs:

{{<printout caption="EVPN IMET routes advertised by Arista EOS switches">}}
l1#show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 10.0.0.1              -       100     0       i
 * >      RD: 10.0.0.1:1001 imet 10.0.0.1
                                 10.0.0.1              -       100     0       i
 * >      RD: 10.0.0.2:1000 imet 10.0.0.2
                                 -                     -       -       0       i
 * >      RD: 10.0.0.3:1001 imet 10.0.0.3
                                 10.0.0.3              -       100     0       i
{{</printout>}}                                 

The leaf switches are advertising one IMET route each (they have a single MAC-VRF instance), the spine switch is advertising two IMET routes (it has two MAC-VRF instances within an IP-VRF instance).

Next, let's ping the default gateway (the spine switch) from one of the hosts:

{{<printout caption="HB1 pinging the default gateway IP address on Spine">}}
hb1:/# ip route
default via 192.168.121.1 dev eth0
10.0.0.0/24 via 172.16.1.1 dev eth1
10.1.0.0/16 via 172.16.1.1 dev eth1
10.2.0.0/24 via 172.16.1.1 dev eth1
172.16.0.0/16 via 172.16.1.1 dev eth1
172.16.1.0/24 dev eth1 scope link  src 172.16.1.4
192.168.121.0/24 dev eth0 scope link  src 192.168.121.104
hb1:/# ping 172.16.1.1 -c 3
PING 172.16.1.1 (172.16.1.1): 56 data bytes
64 bytes from 172.16.1.1: seq=0 ttl=64 time=14.586 ms
64 bytes from 172.16.1.1: seq=1 ttl=64 time=2.449 ms
64 bytes from 172.16.1.1: seq=2 ttl=64 time=2.351 ms
{{</printout>}}

Before HB1 could send an IP packet to Spine, it had to send an ARP request. Spine could either use ARP gleaning or do an independent ARP resolution when replying to the ICMP Echo request. Regardless of those details, the ARP cache on Spine now contains an entry for HB1:

{{<printout caption="ARP cache for HB1 in Tenant VRF on Spine">}}
spine#show arp vrf tenant
Legend:
 not learned: Associated MAC address is not present in the MAC address table
 -: Static (configuration or programmed by feature)
Address         Age (sec)  Hardware Addr   Interface
172.16.1.4        0:02:48  aac1.ab85.ab1f  Vlan1001, Vxlan1
{{</printout>}}

The ARP entry belongs to the interface Vlan1001 and is reachable over VXLAN. No surprises there.

What about the MAC-IP routes? The leaf switch is advertising the MAC address of HB1; the spine switch is not advertising anything because the IP address of HB1 was learned over the VXLAN interface:

{{<printout caption="MAC-IP routes after the initial ARP requests">}}
spine#show bgp evpn route-type mac-ip
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.3:1001 mac-ip aac1.ab85.ab1f
                                 10.0.0.3              -       100     0       i
{{</printout>}}

**Conclusion:**
* The central router (spine switch) DOES NOT advertise MAC+IP route for hosts attached to its VLANs.
* In scenarios with multiple routers attached to MAC-VRF instances, each router MUST do its own ARP resolution.

**Aside:**
* You could configure ARP snooping on L1/L2 to make them advertise MAC+IP instead of MAC routes for attached hosts. That would give the central router enough information so it wouldn't have to do ARP resolution on its own.
* Some EVPN implementations need ARP snooping to work (the central router will NOT send ARP requests over VXLAN).

What about packet flow? As I mentioned in the [original blog post](/2026/05/arp-issues-evpn-central-routing/), if the central router does not advertise its MAC address, the leaf switches MUST flood all routed traffic[^SFS]. That's exactly what's going on when you use minimal EVPN configuration on Arista EOS (remember: we saw no MAC/IP route for the default gateway's MAC address):

[^SFS]: Similar to the "famous" CCIE exam scenario where the MAC and ARP timers are mismatched.

{{<printout caption="VLAN and EVPN configuration on the Spine switch running Arista EOS">}}
interface Vlan1000
   description VLAN red (1000) -> [hr1,l1]
   vrf tenant
   ip address 172.16.0.1/24
!
interface Vlan1001
   description VLAN blue (1001) -> [hb1,l2]
   vrf tenant
   ip address 172.16.1.1/24
!
router bgp 65000
   !
   vlan 1000
      rd 10.0.0.1:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   vlan 1001
      rd 10.0.0.1:1001
      route-target import 65000:1001
      route-target export 65000:1001
      redistribute learned
{{</printout>}}

**Notes:**
* The above configuration was generated by *netlab* release 26.05. The central router does not need the **redistribute learned** command on the MAC-VRF instances, as it has no directly attached hosts.

If we want to stop the flooding of routed traffic, we MUST configure the central router to advertise at least its MAC address (advertising MAC+IP would be even better). On Arista EOS, use the **‌redistribute router-mac system** command[^TOE] on the MAC-VRF instances to advertise just the default gateway's MAC address or **‌redistribute router-mac system ip** to advertise the MAC+IP EVPN type-2 route.

[^TOE]: Following the honored ancient practice of "throw spaghetti at the wall to see what sticks," I tried out all available **redistribute** commands. This is the one that worked for me 🤷‍♂️

When adding that command to both MAC-VRF instances on the Spine switch, the Spine switch starts advertising its VLAN MAC addresses and the default gateway IP addresses, resulting in a well-behaved EVPN fabric.

{{<printout caption="EVPN MAC-IP routes after the Spine switch starts advertising its VLAN MAC/IP routes">}}
spine#show bgp evpn route-type mac-ip
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.1:1000 mac-ip 001c.733a.3232 172.16.0.1
                                 -                     -       -       0       i
 * >      RD: 10.0.0.1:1001 mac-ip 001c.733a.3232 172.16.1.1
                                 -                     -       -       0       i
 * >      RD: 10.0.0.3:1001 mac-ip aac1.ab85.ab1f
                                 10.0.0.3              -       100     0       i
{{</printout>}}

Mission Accomplished ;)

### Try It Out

The [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/central-routing/topology.yml) I used in this blog post is in the [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/EVPN/central-routing). If you want to try it out:

* [Set up your lab environment](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab) (you can use free GitHub Codespaces)
* Change directory to `EVPN/central-routing`
* Execute **netlab up** and explore
