---
title: "BGP Labs: Stop the Fat-Finger Incidents"
series_title: "Stop the Propagation of Configuration Errors"
date: 2024-03-21 09:04:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/challenge/04-block-fat-fingers/
---
Last time, we discussed the first line of defense against fat finger incidents: [limiting the number of BGP prefixes your router accepts from a BGP neighbor](https://bgplabs.net/basic/b-max-prefix/). However, you can do much more without deploying customer-specific filters (which might require a customer database) or ROV/RPKI.

You can practice the default filters you should always deploy on EBGP sessions with your customers in the [Stop the Propagation of Configuration Errors](https://bgplabs.net/challenge/04-block-fat-fingers/) lab exercise.

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/challenge/04-block-fat-fingers/){{</jump>}}
