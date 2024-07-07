---
date: 2021-09-20 07:07:00+00:00
netlab_tag: overview
series_title: Network Topology Graphs
tags:
- netlab
title: netlab Network Topology Graphs
---
A [*netlab*](https://netlab.tools) user sent me an intriguing question: "*Would it be possible to get network topology graphs out of the tool?*"

{{<note info>}}Please note that we're talking about *creating graphs out of network topology described as a YAML data structure*, not a generic GUI or *draw my network* tool. If you're a GUI person, this is not what you're looking for.{{</note>}}

I [did something similar a long while ago](https://my.ipspace.net/bin/list?id=Ansible#SAMPLES) for a simple network automation project (and [numerous networking engineers built really interesting stuff](https://www.ipspace.net/NetAutSol/Solutions#Network_Diagrams) while attending the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) course), so it seemed like a no-brainer. As always, things aren't as easy as they look.
<!--more-->
Creating a data structure that describes the network as a graph of nodes and links is trivial; the hard part is auto-placement -- how do you position the nodes to make the graph look decent. While there are several tools that can take graph description in JSON or YAML format and even use networking icons to draw switches and routers, I haven't found one (in that category) that would be able to solve the placement problem, so I had go back to the granddaddy of graphing tools: [graphviz](https://graphviz.org/).

I used graphviz earlier, and used Jinja2 templates to generate graph descriptions in DOT language. It was a royal pain. This time, I decided to do it with Python (much easier) and created a whole framework within *netlab* in case you want to expand the functionality (and hopefully contribute it back to the project).

So far, *netlab* can create two types of graphs:

* Topology (nodes and links), optionally clustering nodes into autonomous systems;
* BGP autonomous systems and sessions.

To create the graphs you have to:

* Install *graphviz*
* Run *[netlab create](https://netlab.tools/netlab/create/)* to create a graph description (.dot file)
* Run one of the *graphviz* commands to create a graph in desired output format (they support over a dozen formats)
* Enjoy the end results.

For example, I was using the network topology from [one of my BGP examples](https://github.com/ipspace/netlab-examples/tree/master/BGP/LocPref-Prepend) to create a simple network topology graph:

```
netlab create -o graph
dot graph.dot -T png -o netsim-graph-topo.png
```

{{<figure src="/2021/09/netsim-graph-topo.png" caption="Lab topology (nodes and links)">}}

**Notes:**

* **netlab create** uses *topology.yml* as the default lab topology description and creates *graph.dot* as the default graph description. You can change both with CLI options.
* **dot** is one of the *graphviz* graph drawing commands. You have to specify the graph description (*graph.dot*), output format (png) and output file name.

Changing the graph type to BGP (by using **graph:bgp** CLI parameter with **netlab create**) creates a graph of IBGP and EBGP sessions:

```
netlab create -o graph:bgp
dot graph.dot -T png -o netsim-graph-bgp.png
```

{{<figure src="/2021/09/netsim-graph-bgp.png" caption="BGP sessions">}}

For more details, please read the [netlab documentation](https://netlab.tools/), in particular the [graph output module](https://netlab.tools/outputs/graph/) page.

