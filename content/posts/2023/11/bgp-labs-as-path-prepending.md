---
title: "BGP Labs: AS-Path Prepending"
series_title: "AS-Path Prepending"
date: 2023-11-23 07:43:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/7-prepend/
---
In the previous lab, you learned how to use [BGP Multi-Exit Discriminator (MED)](https://bgplabs.net/policy/6-med/) to influence incoming traffic flow. Unfortunately, MED works only with parallel links to the same network. In a typical *Redundant Internet Connectivity* scenario, you want to have links to two ISPs, so you need a bigger hammer: [AS Path Prepending](https://bgplabs.net/policy/7-prepend/).

{{<figure src="https://bgplabs.net/policy/topology-prepend.png">}}
