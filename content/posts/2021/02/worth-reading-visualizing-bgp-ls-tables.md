---
title: "Worth Reading: Visualizing BGP-LS Tables"
date: 2021-02-07 08:04:00
tags: [ BGP, SDN ]
---
When I'd first seen BGP-LS I immediately thought: "_it would be cool to use this to fetch link state topology data from the network and build a graph out of it_". In those days the only open-source way I could find to do it involved Open DayLight controller's BGP-LS-to-REST-API converter, and that felt like deploying an aircraft carrier to fly a kite.

Things have improved dramatically since then. In [Visualizing BGP-LS Tables](https://hbristoweu.wordpress.com/2021/01/13/visualising-bgp-ls-tables-python-gobgp-grpc-networkx/), *HB* described how he solved the challenge with GoBGP, gRPC interface to GoBGP, and some Python code to parse the data and draw the topology graph with NetworkX. Enjoy!
