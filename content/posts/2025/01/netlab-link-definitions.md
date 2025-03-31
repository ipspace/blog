---
title: "Concise Link Descriptions in netlab Topologies"
date: 2025-01-20 08:22:00+0100
tags: [ netlab ]
netlab_tag: guidelines
---
One of the goals we're always trying to achieve when developing _netlab_ features is to make the lab topologies as concise as possible[^VF]. Among other things, _netlab_ supports numerous ways of describing links between lab devices, allowing you to be as succinct as possible.

[^VF]: I created _netlab_ [because I hated the Vagrantfile clutter](/2020/12/build-labs-netsim-tools/). Everything else was just a pleasant side effect ;)

A bit of a background first:

* In the end, *netlab* collects all links in the **links** list before starting the data transformation process.
* Every entry in the **links** list is a dictionary. That dictionary can contain link attributes and must contain a list of **interfaces** connected to the link.
* Every **interface** must have a **node** (specifying the lab device it belongs to) and could contain additional interface attributes.
<!--more-->

The most concise way to define a link is with a string containing the hyphen-separated list of nodes you want connected to a link. For example:

```
links:
- r1               # stub link, only R1 is connected to it
- r1-r2            # R1 is connected to R2
- r1-r2-r3         # R1, R2, and R3 are connected to a LAN
```

As you could write a YAML list in a line (using the square bracket syntax), the shortest possible description of a three-router network with routers connected in a triangle becomes:

```
nodes: [ r1, r2, r3 ]
links: [ r1-r2, r1-r3, r2-r3 ]
```

It can't get any easier than that, right?

The hyphen-separated format breaks apart if you want to use hyphens in node names. In that case, you can use another shortcut: a link definition could be a *list of nodes*. The same 3-router network could be described as:

```
nodes: [ r-1, r-2, r-3 ]
links:
- [ r-1, r-2 ]
- [ r-1, r-3 ]
- [ r-2, r-3 ]
```

The moment you have to define *link attributes*, you can no longer use the shorthand formats, but even there, you have two options:

* You can specify nodes attached to the link as dictionary keys. For example, this is how you would describe the same triangle of links while setting the OSPF area on each link:

```
links:
- r-1:
  r-2:
  ospf.area: 0
- r-1:
  r-3:
  ospf.area: 1
- r-2:
  r-3:
  ospf.area: 1
```

* You can also use the fact that _netlab_ uses the node names in the link-as-dictionary format to create the **interfaces** list and specify the elements of that list:

```
links:
- interfaces: [ r-1, r-2 ]
  ospf.area: 0
- interfaces: [ r-1, r-3 ]
  ospf.area: 1
- interfaces: [ r-2, r-3 ]
  ospf.area: 1
```

Finally, you might have to specify the *interface parameters*. In that case, it's best to use the dictionary-based link definition and specify interface parameters under node keys. For example, you might decide to specify DR priority for the ABRs in area 1:

```
links:
...
- r-1:
    ospf.priority: 1
  r-3:
  ospf.area: 1
- r-2:
    ospf.priority: 1
  r-3:
  ospf.area: 1
```

Regardless of which format you find the most convenient, _netlab_ always ends with the same data model using the **interfaces** list to represent node-to-link attachments. For example, this is how the description of the first link in OSPF area 1 would look like:

```
- interfaces:
  - node: r-1
    ospf:
      priority: 1
  - node: r-3
  ospf:
    area: 1
```

As you can see, the **interfaces**-based link description is pretty hard to read. Its only use is to create links that connect a node back to itself (for example, [connecting two VRFs with a loopback connection](https://github.com/ipspace/netlab/blob/dev/tests/topology/input/vrf-leaking-loop.yml)).

{{<next-in-series page="/not/there">}}But wait, there's more to come (not one more thing, but four). In a follow-up blog post, we'll explore VLAN links, VRF links, links groups, and groups of links (yes, these are two different things ;){{</next-in-series>}}
