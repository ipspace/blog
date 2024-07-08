---
title: "BGP Labs: Remove Private AS from AS-Path"
series_title: "Remove Private AS from AS-Path"
date: 2024-02-22 07:49:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/4-removeprivate/
---
In a [previous BGP lab exercise](https://bgplabs.net/session/3-localas/), I described how an Internet Service Provider could run BGP with a customer without the customer having a public BGP AS number. The only drawback of that approach: the private BGP AS number gets into the AS path, and everyone else on the Internet starts giving you dirty looks (or drops your prefixes). 

{{<figure src="https://bgplabs.net/session/topology-removeprivate.png">}}

Let's fix that. Most BGP implementations have some **remove private AS** functionality that scrubs AS paths during outgoing update processing. You can practice it in the [Remove Private BGP AS Numbers from the AS Path](https://bgplabs.net/session/4-removeprivate/) lab exercise.
