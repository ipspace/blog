---
title: "Worth Reading: Routing Protocol Implementation Evaluation"
date: 2023-01-15 07:09:00
tags: [ worth reading, IP routing]
---
In 2018 I tried to figure out whether the rush to deploy new routing protocols in leaf-and-spine fabrics is anything more than another blob of hype ([RIFT](/2018/03/data-center-routing-with-rift-on.html), [OpenFabric](/2018/04/openfabric-with-russ-white-on-software.html), [BGP](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on.html)), considering [OSPF got the job done for AWS](/2020/08/worth-reading-ospf-scales-well.html). Those discussions probably sounded like a bunch of smart kids trying to measure outside temperature with a moist finger, so the only recommendation I could give in 2021 was "*[use the best tool for the job, keeping in mind you're not Google or Microsoft](/2021/06/use-best-tool-for-job.html)*"

It's always better to measure than to have opinions, and a group of academics did just that. They developed [Sybil](https://compunet.ing.uniroma3.it/assets/publications/Caiazzi-Scazzariello-Sibyl.pdf) -- a tool to measure routing protocol performance in leaf-and-spine fabrics -- and Dip Singh used it to [compare BGP to IS-IS and OpenFabric](https://dipsingh.github.io/Sibyl-Routing-Protocol-Evaluation/).
