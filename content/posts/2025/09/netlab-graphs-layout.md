---
title: "Changing the Layout of netlab Topology Graphs"
date: 2025-09-30 07:26:00+0200
tags: [ netlab ]
netlab_tag: graph
---
After I published the updated [netlab topology graphs](/2021/09/netsim-tools-graphs/) article, [Samuel K. Lam](https://www.linkedin.com/in/samuel-k-lam/) quickly made a comment along the lines of *now we know how the [graph](/2023/06/bgp-leak-lab/) representing the following topology was made*, adding a nice ASCII art that illustrated the point I was trying to make much better than my graphs:

{{<figure src="/2025/09/bl-topology.png" caption="ASCII art representing the BGP leak lab">}}

Let's see how close we can get to that ideal topology diagram with GraphViz and D2 graphs.
<!--more-->
Here's the GraphViz lab topology diagram created from the [original lab topology](https://github.com/ipspace/netlab-examples/blob/master/BGP/Route-Leaks/topology.yml):

{{<figure src="/2025/09/bl-original.png" caption="GraphViz graph created from the original lab topology">}}

The graph could help you understand the network topology[^MB], but it's all wrong from the perspective of what matters. The transit ISPs should be at the top, followed by access ISPs and customers. Welcome to the wonderful world of auto-placement algorithms.

[^MB]: At least it would do a better job than some of the hand-drawn graphs I've seen in the early days of telekoms trying to become ISPs. In one of the meetings, someone literally pulled the heavily folded network diagram out of his back pocket. I'm pretty sure that was the only copy of the network topology of that particular (pretty large) ISP wannabe.

GraphViz and D2 do a pretty good job placing graph elements on a page, but they can't possibly know what matters to you. They use two clues to figure out which graph elements should be placed first (in the top-left corner):

* The order of nodes listed in the graph description file. All else being equal, nodes defined earlier have a better chance of getting closer to the top-left corner than other nodes[^DPA].
* The order of nodes in edge definitions. If the graph description has an "A-B" edge, A has a better chance of being in the top-left corner than if the graph has a "B-A" edge.

[^DPA]: Using the default top-left-to-bottom-right placing algorithm. Both tools have a nerd knob that can be used to place the nodes in the left-to-right direction ([example](/2021/11/bgp-multipath-netsim-tools/#off-topic-nicer-looking-graphs))

*netlab* creates topology graph description files straight from the lab topology:

* The order of nodes in the graph description file is the same as the order of **nodes** keys -- usually the order in which you list your devices in the **nodes** dictionary (Python preserves key ordering) unless you use [auto-create groups](https://netlab.tools/groups/#create-objects-from-group-members).
* The order of interfaces in the elements of the **links** list -- the order in which you list the nodes in a link *dictionary*, the order in which you specify them in the **interfaces** list, or the order in which the nodes are listed in a string describing a link ([more details](https://blog.ipspace.net/2025/01/netlab-link-definitions/)).

After this brief detour into how things work, let's look at the BGP leak lab [topology file](https://github.com/ipspace/netlab-examples/blob/master/BGP/Route-Leaks/topology.yml). Every single link has the node that should be lower in the diagram listed first, for example:

```
- cust_a:
    bgp.role: customer
  isp_a:
    bgp.role: provider
    bgp.locpref: 200
- cust_ab:
    bgp.role: customer
  isp_a:
    bgp.locpref: 200
    bgp.role: provider
```

No wonder the customers are placed at the top of the diagram. Let's change the order of nodes in link definitions. The above links would become (the whole topology file is on GitHub):

```
- isp_a:
    bgp.role: provider
    bgp.locpref: 200
  cust_a:
    bgp.role: customer
- isp_a:
    bgp.locpref: 200
    bgp.role: provider
  cust_ab:
    bgp.role: customer
```

Not surprisingly, the diagram generated from [that topology file](https://github.com/ipspace/netlab-examples/blob/master/BGP/Route-Leaks/nice-graph.yml) is closer to what we want to have:

{{<figure src="/2025/09/bl-top-down.png" caption="GraphViz graph created from the original lab topology">}}

Can we get any closer to our goal? I couldn't find a way to nudge GraphViz in the right direction. Ultimately, I gave up and added GraphViz [**rank** directives](https://graphviz.org/docs/attrs/rank/) to the **graph.dot** file:

```
graph {
  newrank=true;
...
 { rank=same; trans_1; trans_2 }
 { rank=same; isp_a; isp_b; isp_c; }
}
```

The result is probably as close as one can get to an ideal diagram with an auto-placement tool and a few hints and nudges:

{{<figure src="/2025/09/bl-rank.png" caption="Using GraphViz ranks to create layers of autonomous systems">}}

However, wouldn't it be nice if we didn't have to tweak the **graph.dot** file? Couldn't _netlab_ provide that functionality? Glad you asked (or at least got to here 😉). The **graph.rank** attribute is coming in _netlab_ release 25.10[^ABAJ]. Here's how you could use it to generate an almost-perfect graph without rearranging the links ([complete topology file](https://github.com/ipspace/netlab-examples/blob/master/BGP/Route-Leaks/graph-rank.yml)):

{{<cc>}}Addition to the original topology file{{</cc>}}
```
groups:
  transit:
    members: [ trans_1, trans_2 ]
    graph.rank: 1
  access:
    members: [ isp_a, isp_b, isp_c ]
    graph.rank: 2
```

The **graph.rank** node attribute does two things:

* It generates the **rank=same** directives in the GraphViz graph description file.
* It rearranges the order of nodes in edge (link) descriptions (this works for GraphViz and D2 graph descriptions).

[^ABAJ]: If you're reading this before release 25.10 ships: I know I'm almost as bad as Juniper's Data Center BU that published the "_this is how VXLAN works on Juniper switches_" video on YouTube as soon as they got it to work in an engineering image. However, there are two tiny differences: you can [already run the new code](https://netlab.tools/install/clone/) without begging your SE, and the feature will ship in weeks, not months.

### Kicking The (Free) Tires

Want to try out these examples? Use the procedure I described in the [Changing Colors and Line Styles in netlab Graphs](/2025/09/netlab-graphs-colors-lines/#trygraphs) blog post using the examples from the `BGP/Route-Leaks` directory.
