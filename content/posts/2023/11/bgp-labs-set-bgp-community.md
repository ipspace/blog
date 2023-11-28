---
title: "BGP Labs: Set BGP Communities on Outgoing Updates"
series_title: "Set BGP Communities on Outbound Updates"
date: 2023-11-29 07:21:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
It's hard to influence the behavior of someone with strong opinions (just ask any parent with a screaming toddler), and trying to persuade an upstream ISP not to send the traffic over a backup link is no exception -- sometimes even AS path prepending is not a strong enough argument.

An easy solution to this problem was proposed in 1990s -- what if we could attach [some extra attributes](https://www.rfc-editor.org/rfc/rfc1997.html) (called *communities* just to confuse everyone) to BGP updates and use them to [tell adjacent autonomous systems to lower their BGP local preference](https://www.rfc-editor.org/rfc/rfc1998.html)? You can practice doing that in the _[Attach BGP Communities to Outgoing BGP Updates](https://bgplabs.net/policy/8-community-attach/)_ lab exercise.

{{<figure src="https://bgplabs.net/policy/topology-community-attach.png">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/policy/8-community-attach/){{</jump>}}
