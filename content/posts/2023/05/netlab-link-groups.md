---
date: 2023-05-22 06:45:00+00:00
netlab_tag: guidelines
series_title: Link Groups
tags:
- netlab
title: 'Simplify netlab Topologies with Link Groups'
---
Last month I described how you can simplify your VLAN- or VRF lab topologies with [VRF- and VLAN links](/2023/04/netlab-vrf-vlan-links.html), automatically setting **vlan.access** or **vrf** attribute on a set of links. [Link groups](https://netlab.tools/links/#link-groups) allow you to do the same for any set of link attributes.

### Sample Topology

Imagine you have a small network with three PE-routers connected to a central P-router:
<!--more-->
{{<figure src="/2023/05/netlab-core.png">}}

As long as you're OK with the default parameters (default OSPF cost, default IPv4 address pool), you could describe that lab with a very simple topology file:

```
defaults.device: eos
module: [ ospf ]
nodes: [ pe1, pe2, pe3, p ]
links: [ pe1-p, pe2-p, pe3-p ]
```

Now let's assume that you'd like to use unnumbered core links, set OSPF cost on those links, and set link **role** to **core**.  You can no longer use the simple list of links but have to define link attributes on every single link. Not only is the topology file harder to read, it also contains duplicate attributes[^CPRE].

[^CPRE]: And we know that copy-paste duplication [sometimes results in spectacular failures](https://en.wikipedia.org/wiki/Ariane_flight_V88).

```
defaults.device: eos
module: [ ospf ]
nodes: [ pe1, pe2, pe3, p ]
links:
- pe1:
  p:
  unnumbered: true
  ospf.cost: 100
  role: core
- pe2:
  p:
  unnumbered: true
  ospf.cost: 100
  role: core
- pe3:
  p:
  unnumbered: true
  ospf.cost: 100
  role: core
```

### Link Groups to the Rescue

[*netlab* release 1.5.1](https://netlab.tools/release/1.5/#release-1-5-1) introduced [link groups](https://netlab.tools/links/#link-groups) -- a simple way to set the same set of attributes on numerous links.

Link groups are defined within the **links** list; all you have to do is to set the **group** attribute to tell *netlab* it's dealing with a group of links, and define member links in the **members** attribute.

Using a **core** group, we can get our lab topology back into an  easy-to-read almost-non-redundant format:

```
defaults.device: eos
module: [ ospf ]
nodes: [ pe1, pe2, pe3, p ]
links:
- group: core
  unnumbered: true
  ospf.cost: 100
  role: core
  members: [ pe1-p, pe2-p, pe3-p ]
```

### Behind the Scenes

Before starting the [topology data transformation process](https://netlab.tools/dev/transform/), *netlab* expands link groups into individual links:

* A new link data structure is created for every member link, expanding various [simplified link definition formats](https://netlab.tools/example/link-definition/#simple-links-with-no-link-attributes) into dictionaries.
* Group attributes[^AGM] are added to the link attribute. Link attributes (if specified) take precedence over group attributes.

[^AGM]: Apart from **group** and **members** attributes

Using this process, _netlab_ created the following set of links from the above topology file:

{{<cc>}}Core links created from the **core** link group{{</cc>}}
```
$ netlab create -o yaml:links
- interfaces:
  - ifindex: 1
    ifname: Ethernet1
    ipv4: true
    node: pe1
  - ifindex: 1
    ifname: Ethernet1
    ipv4: true
    node: p
  linkindex: 1
  node_count: 2
  ospf:
    cost: 100
  role: core
  type: p2p
  unnumbered: true
- interfaces:
  - ifindex: 1
    ifname: Ethernet1
    ipv4: true
    node: pe2
  - ifindex: 2
    ifname: Ethernet2
    ipv4: true
    node: p
  linkindex: 2
  node_count: 2
  ospf:
    cost: 100
  role: core
  type: p2p
  unnumbered: true
- interfaces:
  - ifindex: 1
    ifname: Ethernet1
    ipv4: true
    node: pe3
  - ifindex: 3
    ifname: Ethernet3
    ipv4: true
    node: p
  linkindex: 3
  node_count: 2
  ospf:
    cost: 100
  role: core
  type: p2p
  unnumbered: true
```

### Get Started

Link groups were introduced in [netlab release 1.5.1](https://netlab.tools/release/1.5/#release-1-5-1). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
