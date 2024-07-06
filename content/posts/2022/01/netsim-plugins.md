---
date: 2022-01-19 07:09:00+00:00
netlab_tag: extend
pre_scroll: true
tags:
- netlab
title: Introducing netlab Plugins
---
Remember the [BGP anycast lab](/2021/12/bgp-anycast-lab.html) I described in December 2021? In that blog post I briefly mentioned a problem of extraneous IBGP sessions and promised to address it at a later date. Let's see how we can fix that with a *netlab* plugin.

We always knew that it's impossible to implement every nerd knob someone would like to have when building their labs, and extending the tool with Python plugins seemed like the only sane way to go. We added [custom plugins](https://netlab.tools/plugins/) to *netlab* in late 2021, but I didn't want to write about them because we had to optimize the internal data structures first.
<!--more-->
{{<note>}}Even though you don't need to know anything about the internal *netlab* functions to write plugins, your code has to modify the lab topology data model, and we had to get that stabilized, which we hopefully managed to do over the [New Year break](/2022/01/netsim-tools-1.1.html).{{</note>}}

Back to the original challenge. In the BGP anycast lab I wanted to have BGP sessions set up like this:

{{<figure src="/2022/01/anycast-ibgp-plugin.png" caption="Desired BGP sessions">}}

However, *netlab* tries to do *the right thing* and creates IBGP full mesh  within an AS[^RR]. The configured BGP sessions within my lab looked like this:

{{<figure src="/2022/01/anycast-ibgp-sessions.png" caption="Actual BGP sessions">}}

The IBGP sessions within AS 65101 were never established as the loopback addresses of A1...A3 were not advertised into BGP and thus the anycast routers had no way to reach each other (there are no direct links between them). The lab worked as expected, but I still didn't like the results.

{{<cc>}}BGP sessions on one of the anycast routers{{</cc>}}
```
a1#show ip bgp summary | begin Neighbor
Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.0.0.6        4        65101       0       0        1    0    0 never    Idle
10.0.0.7        4        65101       0       0        1    0    0 never    Idle
10.1.0.14       4        65000      30      25        7    0    0 00:20:05        4
```

[^RR]: Or a hub-and-spoke topology if you define route reflector(s)

I could see three solutions to that conundrum:

* Remain unhappy with the way the lab works and move on. Not an option.
* Implement a **bgp.peering.ibgp** (or something similar) nerd knob to enable/disable IBGP sessions. Doable, but we'd have to change all device configuration templates and forever keep track of which devices support this nerd knob. Sounds like a lot of technical debt to solve an edge case.
* Write a plugin that removes unneeded IBGP sessions once the lab topology transformation is complete.

The plugin turned out to be remarkably simple. I imported [Python Box](https://github.com/cdgriffith/Box)[^MYPY] and *netlab* API modules[^NS].

```
from box import Box
from netsim import api
```

[^NS]: The Python modules used by *netlab* are within *netsim* namespace for historical reasons.

Next, I added **anycast** attribute to the list of allowed BGP node attributes in the plugin initialization code. I could do that in the topology file, but I wanted to end with a self-contained module (more about that in a week or so).

{{<cc>}}Add a custom BGP attribute to topology defaults{{</cc>}}
```
def init(topo: Box) -> None:
  topo.defaults.bgp.attributes.node.anycast = { 'type': 'ipv4', 'use': 'prefix' }
```

{{<note>}}
* Python Box module makes deeply nested dictionaries a pleasure to work with -- imagine having to do the same with traditional hodgepodge of square brackets and quotes.
* BGP anycast attribute is explained in the [Building a BGP Anycast Lab](/2021/12/bgp-anycast-lab.html) blog post.
{{</note>}}

Finally, I wanted to modify the lists of BGP neighbors once the [topology transformation](https://netlab.tools/dev/transform/) has been complete. **post_transform** seemed the perfect [hook to use](https://netlab.tools/plugins/), and all I had to do was to:

* Find the nodes with **bgp.anycast** attribute
* Set **bgp.advertise_loopback** to *False* (so I can further simplify the topology file)
* Keep only those BGP neighbors where the BGP session type is not `ibgp`

{{<cc>}}Adjust the BGP attributes and BGP neighbors for nodes with **bgp.anycast** attribute{{</cc>}}
```
def post_transform(topo: Box) -> None:
  for name,node in topo.nodes.items():
    if 'anycast' in node.get('bgp',{}):
      node.bgp.advertise_loopback = False
      node.bgp.neighbors = [ n for n in node.bgp.neighbors if n.type != 'ibgp' ]
```

Let's unpack that code:

* All plugin hooks are called with a single parameter -- current lab topology. When the **init** hook is called, you'll be working with the original topology definition, at the **post_transform** stage the data model has been extensively modified.
* Lab devices are described in the [**nodes** dictionary](https://netlab.tools/nodes/) with the lab topology.
* Each node is a dictionary that contains numerous parameters, including [configuration module](https://netlab.tools/modules/) settings (another dictionary).
* Python Box module is a wonderful tool when you need to traverse deep hierarchies, but it does have a few side effects. With the default *netlab* settings, Python Box automatically creates empty dictionaries when needed. That's awesome in 90% of the cases, but sometimes I don't want to get extra dictionaries, so I have to be a bit careful -- instead of `if node.bgp.anycast:` (which would work even if the node had no BGP parameters), I decided to do a check that would never auto-create empty data structures.
* If the **node.bgp.anycast** attribute is set, it's safe to work with BGP parameters, so we can assume that we can set **advertise_loopback** and that the node has a list of BGP neighbors in **node.bgp.neighbors** (even if that list happens to be empty).
* Every BGP session described in **node.bgp.neighbors** includes session type in **type** attribute, and the value of that parameter could be `ibgp` or `ebgp`. The list comprehension I used selects all list elements that are not IBGP sessions.

Want to do something similar? It's not too hard once understand the *netlab* data structures. Here's how you can get there:

* Build a [lab topology](https://netlab.tools/topology-reference/)
* Run `netlab create -o yaml` to get the final data model. You can also [limit the output to individual components of the data model](https://netlab.tools/outputs/yaml-or-json/).
* Explore the data structures and figure out what needs to be modified.

You can also open a discussion in [*netlab* GitHub repository](https://github.com/ipspace/netlab/) or ask a question in [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in [networktocode Slack team](https://networktocode.slack.com) and we'll do our best to help you.

[^MYPY]: I had to import the Box module to keep **mypy** happy. If you don't care about static type checks (but you should), you could skip this step.

### Revision History

2023-03-02
: Updated the plugin code to work with _netlab_ release 1.5.
