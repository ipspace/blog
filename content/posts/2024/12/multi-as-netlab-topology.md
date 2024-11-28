---
title: "Example: Multi-AS netlab Topology"
series_title: Multi-AS netlab Topology
date: 2024-12-02 07:12:00+0100
tags: [ netlab ]
netlab_tag: use
---
A few weeks ago, Urs Baumann [posted a nice example illustrating the power of netlab](https://www.linkedin.com/posts/ubaumannch_how-long-does-it-take-you-to-spin-up-a-new-activity-7260654329483735040-rmjF/): a 10-router topology running OSPF, IS-IS, and BGP:

{{<figure src="/2024/12/netlab-multias.png">}}

He didn't post the underlying topology file, so let's create a simple topology to build something similar.
<!--more-->
{{<printout>}}
defaults.device: frr
provider: clab
{{</printout>}}

* We'll use FRRouting-based routers (line 1) because we want to be able to run this thing in [GitHub Codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/).
* We'll have to run them in containers (line 2).

{{<printout start="3">}}
groups:
  _auto_create: True
  c_65000:
    module: [ bgp ]
    members: [ r01 ]
    bgp.as: 65000
  p_65100:
    module: [ ospf, bgp ]
    members: [ r02, r03, r04, r05 ]
    bgp.as: 65100
  p_65200:
    module: [ isis, bgp ]
    members: [ r06, r07, r08, r09 ]
    bgp.as: 65200
  c_65002:
    module: [ bgp ]
    members: [ r10 ]
    bgp.as: 65002
{{</printout>}}

The easiest way to create a large number of similar nodes is to use *[node groups](https://netlab.tools/groups/)*:

* [Group members will be created automatically](https://netlab.tools/groups/#create-nodes-from-group-members) (line 5)
* The first group (left customer) has a single member running BGP in BGP AS 65000 (line 6-9).
* The second group defines the left provider (lines 10-13). It has four members running OSPF and BGP in AS 651000.
* The rest of the above defines the right provider (lines 14-17) and the right customer (18-21)

We also need links between routers. Yet again, we'll use *[link groups](https://netlab.tools/links/#link-groups)* to create them:

{{<printout start="22">}}
links:
- group: p_65100
  prefix.ipv4: True
  members: [ 
    r02-r03, r02-r03, r02-r04, r02-r04, 
    r03-r05, r03-r05, r04-r05, r04-r05 ]
- group: p_65200
  prefix.ipv4: True
  members: [
    r06-r07, r06-r08, r07-r09, r08-r09 ]
- group: interas
  members: [
    r01-r02, r01-r03,
    r04-r06, r05-r07, 
    r08-r10, r09-r10 ]
{{</printout>}}

* The first group defines unnumbered IPv4 links within AS 65100 (lines 24-28). The member list is pretty long, as Urs wanted to have two parallel links between pairs of routers (and I love how one could write lists in YAML ;)
* The second group defines unnumbered IPv4 links within AS 65200 (lines 29-32). This group has only four members.
* The final group (lines 33-37) defines all links between autonomous systems.

That's it. Save the file as `topology.yml` and execute [`netlab up`](https://netlab.tools/netlab/up/). Don't want to invest time into [building your own netlab infrastructure](https://netlab.tools/install/)? Use GitHub Codespaces:

* [Start a new GitHub Codespace](https://github.com/codespaces/new/ipspace/netlab-examples)
* Change directory to `routing/multi-as`
* Execute **netlab up** and wait a bit
* Wait for another 30 seconds to get the routing protocols up and running.
* Connect to **r01** with **netlab connect r01** and execute a traceroute:

```
r01(bash)#traceroute -s 10.0.0.1 r10
traceroute to r10 (10.0.0.10) from 10.0.0.1, 30 hops max, 46 byte packets
 1  eth5.r02 (10.1.0.2)  0.003 ms  0.001 ms  0.001 ms
 2  r04 (10.0.0.4)  0.001 ms  0.001 ms  0.001 ms
 3  eth3.r06 (10.1.0.10)  0.001 ms  0.001 ms  0.001 ms
 4  r08 (10.0.0.8)  0.000 ms  0.000 ms  0.001 ms
 5  r10 (10.0.0.10)  0.001 ms  0.000 ms  0.001 ms
```

Not only did _netlab_ create a running network for you, but it also set up reverse DNS mappings to display the (numbered) interfaces your traceroute probes are traversing.
