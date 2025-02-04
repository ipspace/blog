---
title: "Group Similar Links in netlab Topologies"
series_title: Group Similar Links with the Dictionary of Links
date: 2025-02-06 08:39:00+0100
tags: [ netlab ]
netlab_tag: guidelines
---
In the [Concise Link Descriptions](/2025/01/netlab-link-definitions/) blog post, I described various data formats that you could use to concisely list nodes attached to a link. Today, we'll focus on a mechanism that helps you spot errors in your topology: *a dictionary of links*.

Imagine you have a large topology with dozens of links, and you get an error saying, "_there is this problem with `links[17]`_".  It must be great fun counting the links to find which one triggered the error, right?
<!--more-->
For example, the following topology creates an error because _netlab_ tries to use a /30 prefix on the last link and belatedly figures out it needs one more IP address for the VRRP first-hop gateway:

{{<cc>}}Netlab topology creating an out-of-addresses error{{</cc>}}
```
defaults.device: frr

module: [ gateway ]
gateway.protocol: vrrp

nodes: [ a1, a2, c1, c2 ]
addressing.p2p:
  ipv4: 10.0.42.0/28

links: 
- a1-c1
- a1-c2
- a2-c1
- a2-c2
- c1-c2
- a1:
  a2:
  gateway: True
```

{{<cc>}}The error netlab reports when you try to start the lab{{</cc>}}
```
% netlab up
[ERRORS]  Errors found in topology.yml
[VALUE]   links: Cannot use ipv4 prefix 10.1.0.20/30 to address 2 nodes plus first-hop gateway on links[6]
[DATA]    link data: {'_linkname': 'links[6]', 'gateway': {'id': -2, 'protocol': 'vrrp', 'anycast':
          {'mac': '0200.cafe.00ff', 'unicast': True}, 'vrrp': {'group': 1}, 'ipv4': '10.1.0.22/30'},
          'interfaces': [{'node': 'a1', 'gateway': {'ipv4': '10.1.0.22/30'}}, {'node': 'a2',
          'gateway': {'ipv4': '10.1.0.22/30'}}], 'linkindex': 6, 'node_count': 2, 'type': 'p2p',
          'prefix': {'ipv4': '10.1.0.20/30'}}
[HINT]    Use a custom pool with prefix /29 or shorter on links with default gateways
[FATAL]   Cannot proceed beyond this point due to errors, exiting
```

I'm pretty sure you have better things to do than counting which link is the sixth one.

{{<note>}}Let's ignore for the moment that it's pretty easy to spot the error in our sample topology as there's a single link using the **gateway** attribute.{{</note>}}

The *dictionary of links* feature allows you to group links with common functionality. For example, our topology has *core*, *access* and *edge* links:

{{<cc>}}Modified lab topology grouping links by their functionality{{</cc>}}
```
defaults.device: frr

module: [ gateway ]
gateway.protocol: vrrp

nodes: [ a1, a2, c1, c2 ]

links: 
  access:
  - a1-c1
  - a1-c2
  - a2-c1
  - a2-c2

  core:
  - c1-c2

  edge:
  - a1:
    a2:
    gateway: True
```

It's much easier to spot errors when using a structured dictionary of links as the link names include the groups you specified in the **links** data structure:

```
% netlab up
[ERRORS]  Errors found in topology.yml
[VALUE]   links: Cannot use ipv4 prefix 10.1.0.20/30 to address 2 nodes plus first-hop gateway on links.edge[1]
[DATA]    link data: {'_linkname': 'links.edge[1]', 'gateway': {'id': -2, 'protocol': 'vrrp',
          'anycast': {'mac': '0200.cafe.00ff', 'unicast': True}, 'vrrp': {'group': 1}, 'ipv4':
          '10.1.0.22/30'}, 'interfaces': [{'node': 'a1', 'gateway': {'ipv4': '10.1.0.22/30'}},
          {'node': 'a2', 'gateway': {'ipv4': '10.1.0.22/30'}}], 'linkindex': 6, 'node_count': 2,
          'type': 'p2p', 'prefix': {'ipv4': '10.1.0.20/30'}}
[HINT]    Use a custom pool with prefix /29 or shorter on links with default gateways
[FATAL]   Cannot proceed beyond this point due to errors, exiting
```

**To recap:**

* The **links** data structure in a netlab topology can be a list of links or a dictionary.
* The values of the **links** dictionary can be lists of links or further dictionaries.
* Very early in the topology transformation process, _netlab_ flattens the **links** dictionary into a list of links, retaining the dictionary keys in the `_linkname` element to ease troubleshooting.

**Similar topics:**

* [Concise Link Descriptions](/2025/01/netlab-link-definitions/)
* [Simplify netlab Topologies with Link Groups](/2023/05/netlab-link-groups/)
* [Using VLAN and VRF Links](/2023/04/netlab-vrf-vlan-links/)
