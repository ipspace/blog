---
title: "Real-Life Network-as-a-Graph Examples"
date: 2021-06-09 06:26:00
tags: [ networking fundamentals ]
---
After reading the *[Everything Is a Graph](/2021/04/everything-is-a-graph.html)* blog post,  [Vadim Semenov](https://www.linkedin.com/in/vadim-semenov-1b538130/) sent me a long list of real-life examples (slightly edited):

---

I work in a big enterprise and in order to understand a real packet path across multiple offices via routers and firewalls (when **mtr** or **traceroute** don't work -- they do not show firewalls), I made OSPF network visualization based on LSDB output. The idea is quite simple -- save information about LSA1 and LSA2 (LSA5 optionally) and that will be enough in order to build a graph (use **show ip ospf database router/network** on Cisco devices).
<!--more-->
Another benefit of working with graphs, is that you can compare an OSPF network state after applying new redistribution rules (example: from BGP to OSPF), or after a software upgrade and rebooting a network device: build an OSPF graph before and right after the change, and then compare two graphs. It should return new BGP prefixes, redistributed into OSPF, in the first case and two graphs should be identical in the second case.

Another headache: when you manage OSPF link cost on link edges and try to predict what the backup path will be if a link or even a device goes down. **show ip route** command or its OSPF equivalent shows only current state of the network. In order to see backup paths, you have to shut down an OSPF interface and inspect the results... but obviously nobody will do it just for testing. However, when we have a graph of our OSPF domain we can remove the primary OSPF link between two nodes and see how our network/graph rebuilds -- try to build the shortest paths between two nodes in a graph across the investigated segment and make sure that the current path matches our assumptions about backup path.

The same logic works if we need to change OSPF cost, for instance from 10 to 8, and make sure that it will not result in a butterfly effect and faraway offices/sites starting to use the more preferred link with cost 8 =)

The final example of usefulness of graphs is finding asymmetric paths. I'm sure that this task is hard to solve manually without using graphs. In order to make sure that OSPF domain doesn't have asymmetric paths, we can go ever all neighbor nodes in a graph, take all edges between them and check that cost metrics are absolutely identical. It might take days in order to do it manually or it might flood our network with ssh sessions to each network device in order to execute a couple of commands using python/Ansible.

I thought that other network engineers might find my approach of working with OSPF domain using graphs helpful, I made my tools [open-sourced on GitHub](https://github.com/Vadims06/topolograph) under the name `Topolograph` -- now everyone can make a math graph from OSPF LSDB output from Cisco, Juniper, Huawei or Mikrotik 😊.
