---
date: 2021-04-26 09:55:00+00:00
lastmod: 2021-05-01 17:44:00+02:00
networking-fundamentals_tag: graph
tags:
- networking fundamentals
title: Everything Is a Graph
---
One of the viewers of [Rachel Traylor](https://www.ipspace.net/Author:Rachel_Traylor)'s excellent *‌[Graph Algorithms in Networks](https://www.ipspace.net/Graph_Algorithms_in_Networks)* webinar sent me this feedback:

> I think it is too advanced for my needs. Interesting but difficult to apply. I love math and I find it interesting maybe for bigger companies, but for a small company it is not possible to apply it.

While a small company's network might not warrant a graph-focused approach (I might disagree, but let's not go there), keep in mind that almost everything we do in IT rides on top of some sort of graph:
<!--more-->
* Dependencies of software components
* Application dependencies
* Dependencies of application and infrastructure components: application stack on top of vSphere on top of data center fabric and using firewalls and load balancers which are also connected to switches, or virtualized, or... You get the idea.

Just drawing the graphs would help you understand the complexities of your infrastructure (see also: [visualizing IP multicast trees](/2017/12/create-ip-multicast-tree-graphs-from/))... but once you have the graphs in some machine-readable format, you could start using graph theory and related algorithms.

{{<note>}}Don't even think about creating those graphs by hand. The only sane way to create them is to gather the information (preferably using an automated script), and run it through a data-munging script. That process will also ensure the information is up-to-date or easy to update when you badly need it.{{</note>}}

Here's just one example of what you could do with a graph. You could find the *cut set* -- the most critical nodes that tie the graph together. Removing them results in a partitioned graph; not exactly something you'd like to see. BTW, if you did the network design right, then the critical node will be a database instance, not your core switch.

I'm positive you could find numerous other examples, and when you do, you're most welcome to write a comment. You might also want to explore the [extensive list of GraphOps resources](https://dave.dev/blog/2021/02/23-02-2021-graphops/) David Gee put together.

### Revision History

2021-05-01
: Added a link to David Gee's GraphOps resources page