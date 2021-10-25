---
title: "Creating BGP Multipath Lab with netsim-tools"
date: 2021-11-02 07:03:00
tags: [ BGP ]
series: netsim-tools
---
I was editing the *[BGP Multipathing](https://my.ipspace.net/bin/get/Net101/AR4.3%20-%20BGP%20Multipath%20Basics.mp4?download=yes)* video in the *[Advanced Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING)* section of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar, got to the diagram I used to explain the intricacies of IBGP multipathing and said to myself "*that should be easy (and fun) to set up with netsim-tools*".

{{<figure src="/2021/11/BGP-Multipath-Diagram.png">}}

Fifteen minutes later[^1d] I had the lab up and running and could verify that BGP works exactly the way I explained it in the webinar (at least on Cisco IOS).
<!--more-->
[^1d]: ... plus another day spent coding **netlab up/down** functionality because I wanted this blog post to be as cool as possible 🤷‍♂️

## Create Topology File

The mandatory first step when using *netsim-tools* to create your virtual lab[^install]: create a YAML file describing the lab topology.

[^install]: Assuming you [already installed everything you need](https://netsim-tools.readthedocs.io/en/latest/install.html), including [Vagrant images or Docker containers](https://netsim-tools.readthedocs.io/en/latest/install.html#building-the-lab-environment).

I decided to start my tests with IOSv (the fastest one to boot) and placed most of my routers in AS 65000. External router (Y) would be in AS 65100. The network runs OSPF as the internal routing protocol, and a combination of IBGP and EBGP.

```
module: [ bgp, ospf ]
defaults.device: iosv
bgp.as: 65000
```

{{<note>}}I hate the way you have to describe nested dictionaries in YAML, so I added a bit of code to post-YAML parsing that turns dotted notation into a hierarchy of dictionaries{{</note>}}

There will be six nodes in the network -- edge routers A through D, a route reflector, and an external router (Y). I had to set **bgp.rr** attribute on the route reflector, and I decided to use a static ID for that node so I'll be able to quickly identify it in the printouts.

```
nodes:
  a:
  b:
  c:
  d:
  rr:
    bgp.rr: True
    id: 1
```

The external router is in a different autonomous system and needs to originate a BGP prefix:

```
  y:
    bgp.as: 65100
    bgp.originate: [ 10.42.42.0/24 ]
```

As an aside: here's the corresponding data structure in pure YAML to illustrate what's going on behind the scenes:

```
  y:
    bgp:
      as: 65100
      originate: [ 10.42.42.0/24 ]
```
 
 Finally, we need the links connecting the routers. Here they are:
 
```
 links: [ a-b, a-c, b-d, c-d, b-rr, d-rr, c-x, d-x ]
```

## Validating the Topology

I used the graphing capabilities of *netsim-tools* together with *graphviz* to generate a diagram of the "physical" topology and BGP sessions. The diagrams were created with *graphviz* which has its own ideas how to place stuff. Their algorithms usually work well; for whatever reason my network diagrams always look messy.

{{<figure src="/2021/11/BGP-multipath-topo.png" caption="Lab topology created with **netlab create -o graph && dot graph.dot -T png -o topo.png**">}}

{{<figure src="/2021/11/BGP-multipath-sess.png" caption="BGP sessions -- created with **netlab create -o graph:bp && dot graph.dot -T png -o topo.png**">}}

## The Smoke Test

Deploying a virtual lab is a one-liner with *netsim-tools* release 0.9.3 or later. All it takes is **netlab up** and you get a configured lab a minute or two later[^NX].

[^NX]: Or a lunch break later if you decide to test a large topology built with Nexus 9000v.

I had to wait a few more minutes for BGP to start and announce the configured prefixes. After that, I used **netlab connect a** to connect to router A, and executed a few commands.

Let's look at the loopback addresses first (so you'll understand the **show** printouts):

```
a#show host | inc 10.0.0
a                         None  (perm, OK)  0   IP    10.0.0.2
b                         None  (perm, OK)  0   IP    10.0.0.3
c                         None  (perm, OK)  0   IP    10.0.0.4
d                         None  (perm, OK)  0   IP    10.0.0.5
rr                        None  (perm, OK)  0   IP    10.0.0.1
y                         None  (perm, OK)  0   IP    10.0.0.6
```

Now for the real test: the route toward 10.42.42.0/24.

```
a#show ip bgp 10.42.42.0
BGP routing table entry for 10.42.42.0/24, version 14
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  65100
    10.0.0.5 (metric 3) from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Originator: 10.0.0.5, Cluster list: 10.0.0.1
      rx pathid: 0, tx pathid: 0x0
```

As expected, the route is coming from the route reflector (10.0.0.1) and the next hop is 10.0.0.5 (D), even though it would be better for A to use C as the next hop.

### Revenge of the IGP

How about a simple brain-teaser? This is the **traceroute** printout from A to Y:

```
a#trace y source loop 0 probe 5
Type escape sequence to abort.
Tracing the route to y (10.0.0.6)
VRF info: (vrf in name/id, vrf out name/id)
  1 b (10.1.0.2) 2 msec
    c (10.1.0.6) 2 msec
    b (10.1.0.2) 3 msec
    c (10.1.0.6) 3 msec
    b (10.1.0.2) 3 msec
  2 y (10.1.0.26) 4 msec
    d (10.1.0.10) 4 msec *  5 msec
    y (10.1.0.26) 3 msec
```

As you can see, sometimes the probes reach Y in two hops, and sometimes the second hop happens to be D. What's going on? Write a comment!

## Arista EOS Works the Same Way

Another beauty of *netsim-tools* is the ease of changing network devices or virtualization providers. All I had to do to replace Cisco IOSv with Arista EOS was an extra parameter in the **netlab up** command:

```
netlab up --device eos
```

A few minutes later, I had an identically configured lab[^diff], this time running Arista EOS, and as expected got an almost identical printout[^shorter]:

[^diff]: Obviously using slightly different configuration -- Arista EOS is not a perfect clone of the _industry standard_ CLI.

[^shorter]: I removed *weight* and *received* parts of the route details from the printouts to make them fit into the main column.

```
a#sh ip bgp 10.42.42.0
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for 10.42.42.0/24
 Paths: 1 available
  65100
    10.0.0.5 from 10.0.0.1 (10.0.0.1)
      Origin INCOMPLETE, metric 0, localpref 100, IGP metric 30, valid, internal, best
      Originator: 10.0.0.5, Cluster list: 10.0.0.1
      Rx SAFI: Unicast
```

**Coming up next**: fixing suboptimal BGP routing with *additional paths* functionality.
