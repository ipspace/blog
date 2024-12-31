---
title: "netlab: Multi-Site VLANs"
series_title: "Multi-Site VLANs"
date: 2025-01-13 08:12:00+0100
tags: [ netlab ]
netlab_tag: vlan_vrf
---
Imagine you want to create a simple multi-site network with _[netlab](https://netlab.tools/)_:

* The lab should have two sites (A and B).
* Each site has a layer-3 switch, a single VLAN (VLAN 100), and two hosts connected to that VLAN.
* As you don't believe in the magic powers of stretched VLANs, you have a layer-3 (IPv4) link between sites.

{{<figure src="/2025/01/multi-site-vlan.png" caption="Network diagram">}}
<!--more-->
A simplistic attempt to model this network would define a single VLAN and use it on both sites:

{{<printout>}}
nodes: [ s1, s2, h1, h2, h3, h4 ]

groups: 
  switches:
    members: [ s1, s2 ]
    module: [ vlan, ospf ]
    device: eos
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux

vlans:
  blue:
    links: [ s1-h1, s1-h2, s2-h3, s2-h4 ]

links: [ s1-s2 ]
{{</printout>}}

**Notes**:

* The lab has six devices (line 1).
* The devices belong to two [groups](https://netlab.tools/groups/). Switches are EOS devices using [VLANs](https://netlab.tools/module/vlan/) and [OSPF](https://netlab.tools/module/ospf/) (lines 4-7). Hosts are running Linux (lines 8-10).
* The lab has a single VLAN (lines 12-13) with four access links (line 14).
* The two site switches have an extra WAN link (line 16).

This approach has just a tiny little problem: a single VLAN has one IP prefix, and so _netlab_ assigns the same IP prefix to both sites. Here's the [addressing report](https://netlab.tools/netlab/report/) to prove it:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **h1** |
| eth1 | 172.16.0.3/24 |  | h1 -> [s1,h2,h3,s2,h4] |
| **h2** |
| eth1 | 172.16.0.4/24 |  | h2 -> [h1,s1,h3,s2,h4] |
| **h3** |
| eth1 | 172.16.0.5/24 |  | h3 -> [h1,s1,h2,s2,h4] |
| **h4** |
| eth1 | 172.16.0.6/24 |  | h4 -> [h1,s1,h2,h3,s2] |
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | s1 -> s2 |
| Ethernet2 |  |  | [Access VLAN blue] s1 -> h1 |
| Ethernet3 |  |  | [Access VLAN blue] s1 -> h2 |
| Vlan1000 | 172.16.0.1/24 |  | VLAN blue (1000) -> [h1,h2,h3,s2,h4] |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s2 -> s1 |
| Ethernet2 |  |  | [Access VLAN blue] s2 -> h3 |
| Ethernet3 |  |  | [Access VLAN blue] s2 -> h4 |
| Vlan1000 | 172.16.0.2/24 |  | VLAN blue (1000) -> [h1,s1,h2,h3,h4] |
{ .fmtTable }

### Site-Specific VLANs

Back to the drawing board. We could define two VLANs (one per site) to [get two IP prefixes](https://netlab.tools/module/vlan/#vlan-addressing):

{{<printout>}}
nodes: [ s1, s2, h1, h2, h3, h4 ]

groups: 
  switches:
    members: [ s1, s2 ]
    module: [ vlan, ospf ]
    device: eos
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux

vlans:
  blue_a:
    links: [ s1-h1, s1-h2 ]
  blue_b:
    links: [ s2-h3, s2-h4 ]

links: [ s1-s2 ]
{{</printout>}}

**Notes:**

* We defined two VLANs (Blue VLAN on site A and site B), each with two access links (lines 13-16)

This topology results in the desired addressing scheme but uses different VLAN IDs on each site (_netlab_ automatically assigns VLAN IDs). The interface descriptions in the addressing reports clearly prove we have VLAN 1000 on one site and VLAN 1001 on the other.

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **h1** |
| eth1 | 172.16.0.3/24 |  | h1 -> [s1,h2] |
| **h2** |
| eth1 | 172.16.0.4/24 |  | h2 -> [h1,s1] |
| **h3** |
| eth1 | 172.16.1.5/24 |  | h3 -> [s2,h4] |
| **h4** |
| eth1 | 172.16.1.6/24 |  | h4 -> [h3,s2] |
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | s1 -> s2 |
| Ethernet2 |  |  | [Access VLAN blue_a] s1 -> h1 |
| Ethernet3 |  |  | [Access VLAN blue_a] s1 -> h2 |
| Vlan1000 | 172.16.0.1/24 |  | VLAN blue_a (1000) -> [h1,h2] |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s2 -> s1 |
| Ethernet2 |  |  | [Access VLAN blue_b] s2 -> h3 |
| Ethernet3 |  |  | [Access VLAN blue_b] s2 -> h4 |
| Vlan1001 | 172.16.1.2/24 |  | VLAN blue_b (1001) -> [h3,h4] |
{ .fmtTable }

### Static VLAN IDs

Fortunately, _netlab_ allows you to specify [static VLAN IDs](https://netlab.tools/module/vlan/#vlan-definition) and does not check whether they overlap. We can thus set the same **vlan.id** on both VLANs:

{{<printout>}}
nodes: [ s1, s2, h1, h2, h3, h4 ]

groups: 
  switches:
    members: [ s1, s2 ]
    module: [ vlan, ospf ]
    device: eos
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux

vlans:
  blue_a:
    links: [ s1-h1, s1-h2 ]
    id: 100
  blue_b:
    links: [ s2-h3, s2-h4 ]
    id: 100

links: [ s1-s2 ]
{{</printout>}}

Let's redo the addressing report, this time using `netlab report addressing.md --node s1,s2` to limit the report to the two switches:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | s1 -> s2 |
| Ethernet2 |  |  | [Access VLAN blue_a] s1 -> h1 |
| Ethernet3 |  |  | [Access VLAN blue_a] s1 -> h2 |
| Vlan100 | 172.16.0.1/24 |  | VLAN blue_a (100) -> [h1,h2] |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s2 -> s1 |
| Ethernet2 |  |  | [Access VLAN blue_b] s2 -> h3 |
| Ethernet3 |  |  | [Access VLAN blue_b] s2 -> h4 |
| Vlan100 | 172.16.1.2/24 |  | VLAN blue_b (100) -> [h3,h4] |
{ .fmtTable }

As you can see, we have two VLANs (blue_a and blue_b) with independent IP prefixes (172.16.0.0/24 and 172.16.1.0/24) but with the same VLAN ID (100). Mission Accomplished ;)

### Credits

This blog post is based on a [discussion idea](https://github.com/ipspace/netlab/discussions/1608) by [@astrotokii](https://github.com/Astrotokii). 