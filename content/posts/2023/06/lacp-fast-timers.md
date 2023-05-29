---
title: "Are LACP Fast Timers Any Good?"
date: 2023-05-28 13:19:00
tags: [ switching ]
draft: True
---
anyone who has some advice on LACP fast rate? When and why should you use it instead of normal LACP?


Ivan Pepelnjak
  12:26 PM
Fast layer-2-only failure detection https://blog.ipspace.net/2012/09/do-we-need-lacp-and-udld.html. Gigabit Ethernet probably does a decent job detecting link failures, beyond that you need a control-plane protocol.

I still doubt if we really need LACP fast rate on 1Gbit UTP links. In my opinion, it's overkill and on our N9K switches, using LACP fast-rate makes ISSU upgrades impossible.

It depends on how fast you want to detect errors :wink: which obviously depends on how critical the workload is and how often the errors happen. Physical layer will probably detect almost all link-down events, so you rely on LACP only for the weirder stuff (MLAG cluster partitioning, control-plane bugs…)