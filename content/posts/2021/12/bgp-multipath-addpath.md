---
date: 2021-12-02 07:40:00+00:00
dcbgp_tag: interesting
netlab_tag: use
series:
- dcbgp
tags:
- BGP
- netlab
title: Optimal BGP Path Selection with BGP Additional Paths
---
A month ago I explained how [using a BGP route reflector in a large-enough non-symmetrical network could result in suboptimal routing](/2021/11/bgp-multipath-netsim-tools/) (or loss of path diversity or multipathing). I also promised to explain how *Advertisement of Multiple Paths in BGP*  functionality[^AP] solves that problem. Here we go...

I extended the [original lab](https://github.com/ipspace/netlab-examples/blob/master/BGP/Multipath/baseline.yml) with another router to get a scenario where one route reflector (RR) client should use equal-cost paths to an external destination while another RR client should select a best path that is different from what the route reflector would select.
<!--more-->
[^AP]: [RFC 7911](https://datatracker.ietf.org/doc/html/rfc7911), also know as *BGP Additional Paths* or *BGP AddPath*

The following diagrams show the "physical" lab topology and the BGP sessions:

{{<figure src="/2021/12/graph.topo-addpath.png" caption="Physical Lab Topology">}}

{{<figure src="/2021/12/graph.bgp-addpath.png" caption="BGP Sessions">}}

In the ideal world:

* Route Reflector (RR) would select RR-D-Y as the best path toward 10.42.42.0/24 (the prefix advertised by Y)
* A would select A-C-Y as the best path toward the same prefix
* M would use ECMP between M-C-Y and M-D-Y paths.

To get there, the route reflector has to advertise D-Y and C-Y paths to A and M, but the rules of BGP ([RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271)) prevent that. If RR advertises two paths to the same prefix, the second update overwrites the first one because they describe the same prefix. Back to the drawing board.

{{<note info>}}You'll find more details of equal/unequal-cost multipathing and BGP multipathing in _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.{{</note>}}

### Technology

[RFC 7911](https://datatracker.ietf.org/doc/html/rfc7911) extends the *advertised prefix* (Network Layer Reachability Information -- NLRI) with a *Path Identifier* to solve the *multiple updates of the same prefix* conundrum. Obviously one cannot just send the new data structures to an unsuspecting BGP neighbor; BGP neighbors must *negotiate* the new functionality [with BGP capabilities exchange](/2021/11/bgp-dynamic-capability/), usually bringing down the BGP session as an interesting side effect. 

RFC 7911 allows a BGP speaker to advertise that it's willing to *send* multiple paths, *receive* multiple paths or both. For a working solution, one of the neighbors must be willing to *receive* multiple paths, and the other one must be will to *send* them. Obviously it's also possible to have a two-way exchange.

Selecting the paths that are advertised to a neighbor willing to receive multiple paths is a local implementation decision. Implementations of *BGP Additional Paths* functionality have further nerd knobs that allow you to specify:

* Which alternate paths should be considered to be interesting;
* Which interesting alternate paths should be advertised to individual neighbors.

Any gotchas? Sure. The *path identifier* is a local variable and might not be preserved across [Graceful Restarts](/2021/09/graceful-restart/). In the words of RFC 7911:

> As the Path Identifiers are locally assigned, and may or may not be persistent across a control plane restart of a BGP speaker, an implementation SHOULD take special care so that the underlying forwarding plane of a "Receiving Speaker" as described in RFC4724 is not affected during the graceful restart of a BGP session.

I read that as _fun times, bugs ahead_; you might be more optimistic.

### Design

In small IBGP network, the route reflector(s) should *send* additional paths to the RR clients to enable multipathing or optimal path selection. There is no need for the clients to send multiple paths to the route reflector *assuming the clients change the next hop on IBGP updates*. The proof is left as an exercise for the reader.

In a larger network using multiple RR levels, you probably need a two-way exchange of multiple paths between route reflectors. 

Our network is not highly redundant (there are few alternate paths to every external prefix), so it's perfectly fine to send all additional paths to every RR client. You might want to reduce the number of additional paths sent to edge routers in larger networks -- it's always a tradeoff between memory/CPU utilization and path selection optimality.

### Lab Time

Of course I tried to wing it... and failed. RTFM helped; here's how to make *BGP additional paths* work on Cisco IOS:

* The *additional paths* functionality is configured within an address family.
* On the route reflector, I enabled it globally with the **bgp additional-paths send** address family configuration command... and lost all BGP sessions in a jiffy. You might want to schedule a maintenance window in a production network.
* On the RR clients I enabled the willingness to receive multiple paths with **neighbor additional-paths receive** configuration command... and lost the BGP session to the route reflector (but at least I wasn't surprised anymore).

And nothing happened. Configuring BGP sessions is not good enough, you have to specify which additional paths you want to consider with the **bgp additional-paths select** command. I decided to use **all** additional paths, and in a few seconds I could see a change in the BGP table on the route reflector (notice the **all** keyword next to the suboptimal path)

{{<cc>}}Additional paths are selected in the BGP table on the route reflector{{</cc>}}
```
rr(config-router-af)#bgp additional-paths select all
rr(config-router-af)#do show ip bgp 10.42.42.0
BGP routing table entry for 10.42.42.0/24, version 14
Paths: (2 available, best #2, table default)
  Path not advertised to any peer
  Refresh Epoch 1
  65100, (Received from a RR-client)
    10.0.0.4 (metric 3) from 10.0.0.4 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, valid, internal, all
      rx pathid: 0, tx pathid: 0x1
  Path advertised to update-groups:
     2          3
  Refresh Epoch 1
  65100, (Received from a RR-client)
    10.0.0.5 (metric 2) from 10.0.0.5 (10.0.0.5)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      rx pathid: 0, tx pathid: 0x0
```

Still, I could see no change on the RR client. There's another trick: you have to configure the willingness to send additional paths *for every neighbor* with **neighbor advertise additional-paths** configuration command. Interestingly, you could decide to select **all** alternate paths in the BGP table, but advertise only some of them to a neighbor[^NOORR]

[^NOORR]: This is NOT Optimal Route Reflection functionality, the per-neighbor parameter just limits which routes will be sent to the neighbor, and if you specify **best N**, it's best N routes *from the sender perspective*.

{{<cc>}}Configure additional path advertising for a BGP neighbor{{</cc>}}
```
rr(config-router-af)#neighbor 10.0.0.6 advertise additional-paths all
```

After that change (which *did not* bring down the IBGP session), the RR client got multiple paths to the same prefix from the route reflector:

{{<cc>}}Multiple paths to external prefix on a RR client{{</cc>}}
```
m#show ip bgp 10.42.42.0
BGP routing table entry for 10.42.42.0/24, version 25
Paths: (2 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  65100
    10.0.0.4 (metric 2) from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Originator: 10.0.0.4, Cluster list: 10.0.0.1
      rx pathid: 0x1, tx pathid: 0x0
  Refresh Epoch 1
  65100
    10.0.0.5 (metric 2) from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal
      Originator: 10.0.0.5, Cluster list: 10.0.0.1
      rx pathid: 0x0, tx pathid: 0
```

Final step: enable BGP multipath on the RR client with **maximum-paths** address family configuration command... and finally we can see C and D as the next hops in the IP routing table. Mission accomplished ;))

{{<cc>}}Multiple paths to the external prefix in the IP routing table on a RR client{{</cc>}}
```
Routing entry for 10.42.42.0/24
  Known via "bgp 65000", distance 200, metric 0
  Tag 65100, type internal
  Last update from 10.0.0.5 00:00:05 ago
  Routing Descriptor Blocks:
    10.0.0.5, from 10.0.0.1, 00:00:05 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65100
      MPLS label: none
  * 10.0.0.4, from 10.0.0.1, 00:00:05 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65100
      MPLS label: none
```

### Creating Configuration Templates

I plan to do further tests along the same lines, so I decided to convert the manual process into a configuration template:

{{<cc>}}Configuring BGP Additional Paths on IBGP sessions{{</cc>}}
```jinja2
router bgp {{ bgp.as }}
 address-family ipv4 unicast
{% if bgp.rr is defined %}
  bgp additional-paths select all
  bgp additional-paths send
{% else %}
  maximum-paths 16
  maximum-paths ibgp 16
{% endif %}
{% for n in bgp.neighbors if n.type == 'ibgp' %}
{%   if bgp.rr is defined %}
  neighbor {{ n.ipv4 }} advertise additional-paths all
{%   else %}
  neighbor {{ n.ipv4 }} additional-paths receive
{%   endif %}
{% endfor %}
```

Finally, I added the template as a [custom deployment template](/2021/11/netsim-groups-deployment-templates/) to the topology file. Now I can get a fully-configured lab with a simple **netlab up** command.

```
module: [ bgp, ospf ]
defaults.device: iosv
bgp.as: 65000

groups:
  net: 
    members: [ a,b,c,d,m,rr ]
    config: [ bgp-addpath.j2 ]
  ext: 
    members: [ y ]
    config: [ test-loopback.j2 ]
...
```

Want do to your own tests? [Install netlab](https://netlab.tools/install/), build your own [virtual lab environment](https://netlab.tools/install/#creating-the-lab-environment), and use [this set of configuration files](https://github.com/ipspace/netlab-examples/tree/master/BGP/Multipath).

Want to learn more? Explore [BGP-related blog posts](/tag/bgp/) and _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.
