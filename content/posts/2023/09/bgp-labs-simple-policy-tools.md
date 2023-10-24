---
title: "BGP Labs: Simple Routing Policy Tools"
date: 2023-09-04 06:26:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: edu
---
The first set of [BGP labs](https://bgplab.github.io/bgplab/) covered [the basics](/2023/08/bgp-labs-basic-setup.html), the next four will help you master simple routing policy tools (BGP weights, AS-path filters, prefix filters) using real-life examples:

* [Use BGP weights](https://bgplab.github.io/bgplab/policy/1-weights/) to prefer one of the upstream providers
* [Prevent route leaking between upstream providers](https://bgplab.github.io/bgplab/policy/2-stop-transit/) with an AS-path filter
* [Filter prefixes advertised by your autonomous system](https://bgplab.github.io/bgplab/policy/3-prefix/) with a prefix list
* [Minimize the size of your BGP table](https://bgplab.github.io/bgplab/policy/4-reduce/) with inbound filters

The labs are best used with _[netlab](https://netlab.tools/)_ (it [supports BGP on almost 20 different devices](https://netlab.tools/platforms/#platform-routing-support)), but you could use any system you like (including GNS3 and CML/VIRL). If you're stubborn enough it's possible to make them [work with the physical gear](https://bgplab.github.io/bgplab/external/), but don't ask me for help. For more details, read the [Installation and Setup](https://bgplab.github.io/bgplab/1-setup/) documentation.