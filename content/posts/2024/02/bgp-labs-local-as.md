---
title: "BGP Labs: Use Multiple AS Numbers on the Same Router"
series_title: "Use Multiple AS Numbers on the Same Router"
date: 2024-02-06 07:43:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/3-localas/
---
Can you use BGP to connect to the global Internet without having a public BGP AS number? Of course, assuming your Internet Service Provider is willing to run BGP with a network using a private AS number. But what happens if you want to connect to two ISPs? It's ridiculous to expect you'll be able to persuade them to use the same private AS number.

{{<figure src="https://bgplabs.net/session/topology-localas.png">}}

That's one of the many use cases for the **local-as** functionality available in most BGP implementations. You can practice it in the [Use Multiple AS Numbers on the Same Router](https://bgplabs.net/session/3-localas/) lab exercise.

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/session/3-localas/){{</jump>}}
