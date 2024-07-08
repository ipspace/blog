---
title: "BGP Labs: Use BGP Communities in a Routing Policy"
series_title: "Use BGP Communities in a Routing Policy"
date: 2023-12-13 07:50:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/9-community-use/
---
A [previous BGP lab](https://bgplabs.net/policy/8-community-attach/) focused on the customer side of BGP communities: adding them to BGP updates to influence upstream ISP behavior. [Today's lab](https://bgplabs.net/policy/9-community-use/) focuses on the ISP side of the equation: using BGP communities in a routing policy to implement [RFC 1998-style behavior](https://www.rfc-editor.org/rfc/rfc1998.html).

{{<figure src="https://bgplabs.net/policy/topology-community-use.png">}}
