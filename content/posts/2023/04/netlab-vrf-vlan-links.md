---
date: 2023-04-17 06:55:00+00:00
netlab_tag: vlan_vrf
series_title: Using VLAN and VRF Links
tags:
- netlab
title: 'Using VLAN and VRF Links in netlab Topologies'
---
I already mentioned the introduction of [VRF-](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html#module-vrf-links) and [VLAN access](https://netsim-tools.readthedocs.io/en/latest/module/vlan.html#module-vlan-creating-access-links) links in
_netlab_ [release 1.5.1](https://netsim-tools.readthedocs.io/en/latest/release/1.5.html#release-1-5-1). Let's see how they can simplify your lab topologies.

I always tried to make lab topologies as concise as I could,  sometimes cheating using JSON-in-YAML syntax. For example, the topology describing three routers running OSPF could be as simple as this:

```
module: [ ospf ]
nodes: [ r1, r2, r3 ]
links: [ r1-r2, r2-r3, r3-r1 ]
```

Let's unravel that:
<!--more-->
* The **module** parameter is applied to all nodes in the topology unless specified within a single node or node group.
* While **nodes** is a dictionary of nodes, it can also be written as a list of node names which are automatically expanded into a dictionary.
* Individual links are dictionaries of nodes and link attributes[^INTF], but could be written as strings when you don't need link attributes.

[^INTF]: The final data structure is a bit more complex and contains a list of interfaces attached to a link. The only reason to use that data structure in your lab topology are links connecting two interfaces of the same device.

The above topology is thus expanded into:

```
module: [ ospf ]
nodes:
  r1:
  r2:
  r3:
links:
- r1:
  r2:
- r2:
  r3:
- r3:
  r1:
```

I'm pretty sure you realized why I'm so proud of the concise syntax ;)

### VRF Links

Unfortunately, you need link attributes to put links into VRFs. For example, if you want to build a topology with [four hosts connected to two VRFs configured on a single router](/2022/04/netsim-vrf-lite.html), you had to do it this way:

```
defaults.device: linux

vrfs:
  red:
  blue:

nodes:
  rtr:
    module: [ vrf ]
    device: eos
  h1:
  h2:
  h3:
  h4:

links:
- rtr:
  h1:
  vrf: red
- rtr:
  h2:
  vrf: red
- rtr:
  h3:
  vrf: blue
- rtr:
  h4:
  vrf: blue
```

{{<note info>}}You could use device *groups* to set parameters for the router if you like to use nodes-as-a-list syntax; you'll find an example in the [VLAN links](#vlan-links) section.{{</note>}}

With the new *VRF links* functionality, you could list intra-VRF links in the **links** attribute of a global VRF definition, for example:

```
defaults.device: linux

vrfs:
  red:
    links: [ rtr-h1, rtr-h2 ]
  blue:
    links: [ rtr-h3, rtr-h4 ]

nodes:
  rtr:
    module: [ vrf ]
    device: eos
  h1:
  h2:
  h3:
  h4:
```

Like the global **links**, the links specified within a VRF definition are converted into standard link data structure. They get the **vrf: *name*** attribute, and the resulting data structure is appended to the global **links** list. You don't even need the global **links** list if you have just the VRF links in your topology.

Want to try it out? Take the [multi-VRF topology](https://github.com/ipspace/netlab-examples/blob/master/VRF/vrf-lite-hosts/multi-vrf.yml) from [netlab examples repository](https://github.com/ipspace/netlab-examples/blob/master/VRF/vrf-lite-hosts/multi-vrf.yml).

{{<note info>}}Hint: use *containerlab* to run this topology. It's much easier to install an Arista cEOS container than it is to build an Arista vEOS Vagrant box.{{</note>}}

### VLAN Links

VLAN links are very similar to VRF links:

* They are listed in the **links** attribute of global VLAN definitions.
* They are appended to the global **links** list with **vlan.access** attribute set to the VLAN name.

For example, we could use them to simplify [VXLAN bridging](/2022/09/netlab-vxlan-bridging.html) topology:

```
groups:
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux
  switches:
    members: [ s1,s2 ]
    module: [ vlan,vxlan,ospf ]

vlans:
  red:
    mode: bridge
  blue:
    mode: bridge

nodes: [ h1, h2, h3, h4, s1, s2 ]

links:
- h1:
  s1:
  vlan.access: red
- h2:
  s2:
  vlan.access: red
- h3:
  s1:
  vlan.access: blue
- h4:
  s2:
  vlan.access: blue
- s1:
  s2:
```

Moving the VLAN access links into VLAN definitions results in a much cleaner lab description:

```
groups:
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux
  switches:
    members: [ s1,s2 ]
    module: [ vlan,vxlan,ospf ]

vlans:
  red:
    mode: bridge
    links: [ h1-s1, h2-s2 ]
  blue:
    mode: bridge
    links: [ h3-s1, h4-s2 ]

nodes: [ h1, h2, h3, h4, s1, s2 ]

links: [ s1-s2 ]
```

You can find the above topology file in the [VXLAN bridging](https://github.com/ipspace/netlab-examples/tree/master/VXLAN/vxlan-bridging) example in the [netlab examples repository](https://github.com/ipspace/netlab-examples/).

### Get Started

Both features were introduced in [netlab release 1.5.1](https://netsim-tools.readthedocs.io/en/latest/release/1.5.html#release-1-5-1). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netsim-tools.readthedocs.io/en/latest/tutorials.html) and the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
