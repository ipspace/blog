---
title: "BGP Labs: Graceful Shutdown"
series_title: "BGP Graceful Shutdown"
date: 2024-05-30 08:22:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/challenge/03-graceful-shutdown/
---
Using the typical default router configurations, it can take minutes between a failure of an inter-AS link and the convergence of BGP routes. You can [fine-tune that behavior with BGP timers and BFD](https://bgplabs.net/basic/7-bfd/) (and still get [pwned by Graceful Restart](/2021/10/graceful-restart-convergence.html)). While you can't influence link failures, you could drain the traffic from a link before starting maintenance operations on it, and it would be a shame not to do that considering there's a standard way to do that -- the GRACEFUL_SHUTDOWN BGP community defined in [RFC 8326](https://www.rfc-editor.org/rfc/rfc8326.html). That's what you'll [practice in the next BGP lab exercise](https://bgplabs.net/challenge/03-graceful-shutdown/). 

{{<figure src="https://bgplabs.net/challenge/topology-graceful-shutdown.png" width="400">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/challenge/03-graceful-shutdown/){{</jump>}}
