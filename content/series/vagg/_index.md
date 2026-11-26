---
title: Optimizing the Size of the BGP Table
sidebar_box: rb
layout: custom
---
If you want to implement redundant Internet connectivity with multiple upstream Internet Service Providers, you don't have to accept the entire global (Default-Free) BGP table. You could select a subset of (locally important) BGP routes and use default routes to reach the rest of the Internet.

I described that idea in several blog posts:

{{<series-listing year="sure" tag="basics">}}

One of the most important details in that concept is the default route generation. You should not accept an unconditional default route advertised by your ISP; the ISP might keep advertising it even if their network is broken. For more details, read these blog posts:

{{<series-listing year="sure" tag="default">}}

Finally, you could optimize just the forwarding resources. For example, BGP routes that use the same next hop as the default route do not have to be installed in the forwarding table; an old concept known as *virtual aggregation*

{{<series-listing year="sure" tag="vagg">}}

Alternatively, you could install just the important BGP prefixes  (those with enough traffic) into the BGP table -- the approach taken by David Barroso in his SDN Internet Router project (you'll find further links in the podcast episode pages):

{{<series-listing year="sure" tag="sdn">}}

{{<series-listing notag="sure" title="Posts I Forgot to Classify">}}
