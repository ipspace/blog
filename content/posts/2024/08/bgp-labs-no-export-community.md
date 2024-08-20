---
title: "Using No-Export Community to Filter Transit Routes"
date: 2024-08-23 08:00:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/d-no-export/
---
The very first [BGP Communities RFC](https://www.rfc-editor.org/rfc/rfc1997.html) included an interesting idea: let's tag paths we don't want to propagate to other autonomous systems. For example, the prefixes received from one upstream ISP should not be propagated to another upstream ISP (sadly, [things don't work that way in reality](https://blog.ipspace.net/2019/07/rant-some-internet-service-providers/)).

Want to try out that concept? Start the [Using No-Export Community to Filter Transit Routes](https://bgplabs.net/policy/d-no-export/) lab in [GitHub Codespaces](https://bgplabs.net/4-codespaces/).

{{<figure src="https://bgplabs.net/policy/topology-no-export.png">}}
