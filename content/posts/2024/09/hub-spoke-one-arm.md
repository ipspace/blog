---
title: "One-Arm Hub-and-Spoke VPN with MPLS/VPN"
date: 2024-09-24 08:15:00+0200
tags: [ netlab, design ]
netlab_tag: mpls
series: hub_spoke_vpn
---
All our previous designs of the [hub-and-spoke VPN](/2024/09/hub-spoke-vpn-topology/) ([single PE](/2024/09/hub-spoke-single-pe/), [EVPN](/2024/09/hub-spoke-evpn/)) used two VRFs for the hub device (ingress VRF and egress VRF). Is it possible to build a one-arm hub-and-spoke VPN where the hub device exchanges traffic with the PE router over a single link?

**TL&DR:** Yes, but only on some devices (for example, Cisco IOS or FRRouting) when using MPLS transport.

Here's a high-level diagram of what we'd like to achieve:
<!--more-->
{{<figure src="/2024/09/hub-spoke-one-arm.png">}}

You're not wrong if you think this looks exactly like a common-services VPN topology. However, we'll use a routing trick and a very particular feature of the MPLS transport to make it work as a hub-and-spoke VPN.

Before going into the details: this is the [_netlab_](https://netlab.tools/) lab topology we'll use to build the network ([source code](https://github.com/ipspace/netlab-examples/blob/master/MPLS/hub-spoke-one-arm/topology.yml)):

{{<printout>}}
defaults.device: iosv

module: [ bgp ]
plugin: [ bgp.session ]

groups:
  ce:
    device: frr
    provider: clab
    members: [ ce_s1, ce_s2, ce_hub ]
  pe:
    members: [ pe_a, pe_b, pe_h ]
    module: [ ospf, bgp, vrf, mpls ]
    bgp.as: 65000
    mpls.vpn: True

mpls.ldp: True

vrfs:
  s_1:
    links: [ pe_a-ce_s1 ]
    export: [ 65000:100 ]
    import: [ 65000:101 ]
  s_2:
    links: [ pe_b-ce_s2 ]
    export: [ 65000:100 ]
    import: [ 65000:101 ]
  hub:
    import: [ 65000:100 ]
    export: [ 65000:101 ]
    links:
    - pe_h:
      ce_hub:
        bgp.default_originate: True

nodes:
  pe_a:
  pe_b:
  pe_h:
  p:
    module: [ mpls, ospf ]
  ce_hub:
    bgp.as: 65100
  ce_s1:
    bgp.as: 65101
  ce_s2:
    bgp.as: 65102

links: [ pe_a-p, pe_b-p, pe_h-p ]
{{</printout>}}

Most of the topology has been explained in the previous blog posts ([single PE](/2024/09/hub-spoke-single-pe/), [EVPN](/2024/09/hub-spoke-evpn/)); here's the gist of the minor changes:

* We'll use Cisco IOSv virtual machines as the PE- and P routers and FRRouting containers as the CE routers (lines 1, 8-9)
* The PE routers will use the OSPF, BGP, MPLS, and VRF netlab modules (line 13). The P router will use only the OSPF and the MPLS modules (line 41).
* All MPLS-enabled routers will run LDP (line 17). PE routers will also run MPLS/VPN (line 15).

Now for the fun part:

* We're using the alternate approach to implement common services VRFs[^CSRT]. All spoke VRFs export routes with a common RT (lines 22,26); those routes are imported into the `hub` VRF (line 29). The `hub` VRF exports its routes with a different route target (line 30) that is then used to import routes into the spoke VRFs (lines 23,27).
* The crucial bit: the hub router is advertising a default route (line 34)[^DF].

[^CSRT]: The approach described in the [Common Services VRF with EVPN Control Plane](/2024/08/evpn-common-services-vrf/) would work as well, but this one scales better.

[^DF]: It could also advertise a summary prefix that covers all the spoke address space.

Does this really work? Of course it does, or I wouldn't be writing this blog post ;) Packets from CE_S1 to CE_S2[^R191] traverse:

* VRF `s_1` on PE_A
* P router
* VRF `hub` on PE_H
* Ethernet interface on CE_HUB
* VRF `hub` on PE_H
* P router
* VRF `s_2`on PE_B

[^R191]: You'll get the fancy hostnames that include VRFs and interfaces in _netlab_ release 1.9.1.

```
$ netlab connect ce_s1 traceroute ce_s2
Connecting to container clab-hub-spoke-on-ce_s1, executing traceroute -w 1 ce_s2
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  GigabitEthernet0-2.s_1.pe_a (172.16.0.1)  0.421 ms  0.360 ms  0.271 ms
 2  GigabitEthernet0-1.p (10.1.0.1)  0.883 ms  0.683 ms  0.537 ms
 3  GigabitEthernet0-2.hub.pe_h (172.16.2.3)  0.522 ms  0.542 ms  0.489 ms
 4  eth1.ce_hub (172.16.2.5)  0.554 ms  0.513 ms  0.424 ms
 5  GigabitEthernet0-2.hub.pe_h (172.16.2.3)  0.611 ms  0.470 ms  0.546 ms
 6  GigabitEthernet0-3.p (10.1.0.9)  1.031 ms  0.934 ms  1.100 ms
 7  GigabitEthernet0-2.s_2.pe_b (172.16.1.2)  1.037 ms  0.968 ms  0.976 ms
 8  ce_s2 (10.0.0.7)  1.004 ms  1.069 ms  1.083 ms
 ```

### Behind the Scenes

The second part of the packet's path (CE_HUB to CE_S2) is trivial (we've covered it in the previous blog posts), but how does a packet get from CE_S1 to CE_HUB?

As we know, CE_HUB advertises the default route. That default route is converted into a VPNv4 route and sent to PE_A and PE_B, which import it into S_1 and S_2 VRFs:

{{<cc>}}VPNv4 routes associated with VRF S_1 on PE_A{{</cc>}}
```
pe_a#show ip bgp vpnv4 vrf s_1
BGP table version is 15, local router ID is 10.0.0.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 65000:1 (default for vrf s_1) VRF Router ID 10.0.0.1
 *>i 0.0.0.0          10.0.0.3                 0    100      0 65100 i
 *>i 10.0.0.5/32      10.0.0.3                 0    100      0 65100 i
 *>  10.0.0.6/32      172.16.0.6               0             0 65101 i
 *>  172.16.0.0/24    0.0.0.0                  0         32768 ?
 *>i 172.16.2.0/24    10.0.0.3                 0    100      0 ?
```

As we're using the MPLS transport, there's a label attached to the default route:

{{<cc>}}The details of the default route in VRF S_1 on PE_A{{</cc>}}
```
pe_a#show ip bgp vpnv4 vrf s_1 0.0.0.0/0
BGP routing table entry for 65000:1:0.0.0.0/0, version 10
Paths: (1 available, best #1, table s_1)
  Advertised to update-groups:
     1
  Refresh Epoch 1
  65100, imported path from 65000:3:0.0.0.0/0 (global)
    10.0.0.3 (metric 3) (via default) from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Extended Community: RT:65000:101
      mpls labels in/out nolabel/16
      rx pathid: 0, tx pathid: 0x0
```

Label 16 (advertised by PE_HUB) is prepended to all packets forwarded via the default route. Now let's see what PE_HUB does when it receives packets with MPLS label 16:

{{<cc>}}The LFIB on PE_HUB{{</cc>}}
```
pe_h#show mpls forwarding-table labels 16 detail
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
16         No Label   0.0.0.0/0[V]     2826          Gi0/2      172.16.2.5
	MAC/Encaps=14/14, MRU=1504, Label Stack{}
	AAC1AB118CB352540054AC4F0800
	VPN route: hub
	No output feature configured
```

The LFIB entry for label 16 on PE_HUB says:

* Pop label 16 (replace label 16 with no label)
* Send the packet to interface Gi0/2
* The next hop on interface Gi0/2 is 172.16.2.5 (Ethernet interface on CE_HUB)
* The MAC header to use is `AAC1AB118CB352540054AC4F0800`

After inspecting the ARP entries for the `hub` VRF, it's easy to figure out that the MAC header contains the MAC address of CE_HUB, the MAC address of PE_H, and the IP protocol type (0x0800):

{{<cc>}}ARP entries for the hub VRF on PE_H{{</cc>}}
```
pe_h#show arp vrf hub
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  172.16.2.3              -   5254.0054.ac4f  ARPA   GigabitEthernet0/2
Internet  172.16.2.5             46   aac1.ab11.8cb3  ARPA   GigabitEthernet0/2
```

**Summary:** PE_H does not inspect the IP packet it receives from PE_A. It performs an MPLS label lookup, finds the outgoing interface and the corresponding layer-2 header from the MPLS label, and sends the packet toward the next hop without ever involving the IP forwarding code.

### Per-Prefix or Per-VRF Labels

Now for the bad news: the trick described in this blog works only when PE_H allocates MPLS labels to *individual prefixes*. Some devices (including Arista EOS) don't do that but assign labels to VRFs. This is the route PE_H running Arista EOS advertises to PE_A:

{{<cc>}}Default route in VRF S_1 as advertised by PE_H running Arista EOS{{</cc>}}
```
pe-a#show bgp vpn-ipv4 0.0.0.0/0 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for IPv4 prefix 0.0.0.0/0, Route Distinguisher: 65000:3
 Paths: 1 available
  65100
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric 0, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:101
      Remote MPLS label: 100000
```

And this is the LFIB entry for label 100000 on PE_H:

{{<cc>}}LFIB entry PE_H attaches to the default route it receives from CE_HUB{{</cc>}}
```
pe-h#show mpls route 100000
...
 100000   [0]
                via I, ipv4, vrf hub
```

The LFIB entry does not contain an outgoing interface; it points to the `hub` VRF forwarding table. The traceroute from CE_S1 to CE_S2 thus gets to PE_H but not to CE_HUB[^NOTTL]:

[^NOTTL]: It also looks like PE_H would not decrement TTL when turning the IP packet around. The P router is not visible in the path from PE_H to PE_B.

```
$ netlab connect ce_s1 traceroute ce_s2
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  Ethernet2.s_1.pe_a (10.1.0.14)  0.003 ms  0.002 ms  0.001 ms
 2  Ethernet1.p (10.1.0.1)  2.705 ms  0.952 ms  0.827 ms
 3  Ethernet1.pe_h (10.1.0.10)  0.740 ms  0.668 ms  0.619 ms
 4  Ethernet1.pe_b (10.1.0.6)  1.889 ms  1.293 ms  1.163 ms
 5  ce_s2 (10.0.0.7)  1.352 ms  1.271 ms  1.226 ms
```

Finally, a quick detour. If you use VXLAN transport with the EVPN control plane, the VRF transit VNI acts like a per-VRF label (it identifies the VRF on the egress router). Thus, it's impossible to implement a one-arm hub-and-spoke topology with VXLAN transport.

{{<next-in-series page="/posts/2024/10/mpls-vpn-prefix-vrf-labels.md">}}
You'll have to wait for the next blog post if you want to know more about MPLS/VPN label allocation options.
{{</next-in-series>}}

### Try It Out

Want to try it out yourself? Unfortunately, you cannot do it in [GitHub Codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/):

* You cannot run virtual machines in GitHub Codespaces. Junos, IOS, or IOS XR are out.
* FRRouting or VyOS containers use Linux MPLS drivers; you cannot load them in GitHub Codespaces.
* Arista cEOS has a user-mode MPLS data plane but does not support per-prefix label allocation.
* SR Linux requires a license to run MPLS.

Anyway, if you want to try the lab without investing in installing vendor VMs, you can use FRRouting containers:

* [Install _netlab_ into a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) ([FRRouting works on Apple silicon](/2024/03/netlab-bgp-apple-silicon/)).
* Copy the [topology file](https://github.com/ipspace/netlab-examples/blob/master/MPLS/hub-spoke-one-arm/topology.yml) into an empty directory.
* Execute **netlab up -p clab -d frr**.
* Configure **‌label vpn export allocation-mode per-nexthop** within the **‌address-family ipv4** of the **‌router bgp 65000 vrf hub** configuration of PE_H.

The only bits you would be missing with this setup would be the intermediate routers in the **traceroute** output; it looks like Linux cannot forward the ICMP TTL-exceeded packets along an MPLS path (I may be missing something, in which case please leave a comment).

{{<cc>}}Traceroute from CE_S1 to CE_S2 when using FRRouting containers as PE- and P routers{{</cc>}}
```
$ netlab connect ce_s1 traceroute ce_s2 -w 1
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  eth2.s_1.pe_a (10.1.0.14)  0.004 ms  0.003 ms  0.001 ms
 2  *  *  *
 3  eth1.ce_hub (10.1.0.21)  0.005 ms  0.001 ms  0.001 ms
 4  eth1.pe_h (10.1.0.10)  0.000 ms  0.004 ms  0.004 ms
 5  *  *  *
 6  ce_s2 (10.0.0.7)  0.032 ms  0.001 ms  0.001 ms
```