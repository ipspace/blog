---
title: "BGP Labs: Using Multi-Exit Discriminator (MED)"
series_title: "Using Multi-Exit Discriminator (MED)"
date: 2023-11-15 06:42:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/6-med/
---
In the previous labs, we used [BGP weights](https://bgplabs.net/policy/1-weights/) and [Local Preference](https://bgplabs.net/policy/5-local-preference/) to select the best link out of an autonomous system and thus change the outgoing traffic flow.

Most edge (end-customer) networks face a different problem -- they want to influence the incoming traffic flow, and one of the tools they can use is [BGP Multi-Exit Discriminator (MED)](https://bgplabs.net/policy/6-med/).

{{<figure src="https://bgplabs.net/policy/topology-med.png">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/policy/6-med/){{</jump>}}
