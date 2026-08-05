---
title: "Compress netlab Lab Topologies with Dot Notation"
date: 2026-08-11 07:55:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
_netlab_ is using the Python Box library to make the code easier to read[^CER]. When I started the project, I hated the way you fetch values from Python dictionaries with stuff like `node['ospf']['area']`; Python Box lets you write `node.ospf.area`. Even better[^OW], you can tell Python Box to create intermediate dictionaries as needed. `node.ospf.area = 1` will automatically create the `node.ospf` dictionary.

But wait, there's more (yes, we're getting to the topic of today's blog post): Box lets you use the same dotted notation in YAML files.
<!--more-->
[^CER]: As usual, some people [disagree with that](https://github.com/ipspace/netlab/discussions/3644) ([with good arguments](https://github.com/ipspace/netlab/discussions/3513)), but that ship has sailed years ago.

[^OW]: Or worse, it's a matter of personal opinion.

For example, imagine you want to have a simple topology with two BGP-speaking routers, each in its own autonomous system. This is how you could describe that in orthodox YAML:

```
defaults:
  device: eos
  
nodes:
  r1:
    bgp:
      as: 65000
  r2:
    bgp:
      as: 65002
```

Now let's introduce some shortcuts:

```
defaults.device: eos

nodes:
  r1:
    bgp.as: 65000
  r2:
    bgp.as: 65002
```

I'm sure you get the idea. The only thing you have to be careful about[^RHY]: don't mix the YAML dictionary notation with the shortcuts *for the same object*. I [opened an issue](https://github.com/cdgriffith/Box/issues/305) months ago. Jeroen [provided a fix](https://github.com/cdgriffith/Box/pull/306) soon after that, and we can only hope it will eventually get merged into the next release.

[^RHY]: And as always, Box gives you all the rope you need to hang yourself three times over.

Anyway, can we go any further? Of course. How about:

```
defaults.device: eos

nodes:
  r1.bgp.as: 65000
  r2.bgp.as: 65002
```

Finally, let's add a link with fixed IPv4 addresses to the topology, using the trick we just learned:

```
defaults.device: eos

nodes:
  r1.bgp.as: 65000
  r2.bgp.as: 65002

links:
- r1.ipv4: 10.1.0.1/24
  r2.ipv4: 10.1.0.2/24
```

OK, here's another one in case you don't like the hard-coded IP addresses (it uses a hard-coded IPv4 prefix, though):

```
defaults.device: eos

nodes:
  r1.bgp.as: 65000
  r2.bgp.as: 65002

links:
- prefix.ipv4: 10.1.0.0/24
  r1.ipv4: 1
  r2.ipv4: 2
```

Have fun ;) And if you create something cool with _netlab_, do let me know!
