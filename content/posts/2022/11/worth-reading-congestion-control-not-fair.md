---
title: "Congestion Control Algorithms Are Not Fair"
date: 2022-11-27 07:00:00
tags: [ QoS ]
---
Creating a mathematical model of queuing in a distributed system is hard ([Queuing Theory](https://www.ipspace.net/Queuing) was one of the most challenging ipSpace.net webinars so far), and so  instead of solutions based on control theory and mathematical models we often get what seems to be _promising stuff_.

Things that look _intuitively promising_ aren't always [what we expect them to be](https://www.explainxkcd.com/wiki/index.php/793:_Physicists), at least according to an MIT group that 
[analyzed delay-bounding TCP congestion control algorithms (CCA)](https://blog.apnic.net/2022/11/23/congestion-control-algorithms-are-not-fair/) and found that most of them result in unfair distribution of bandwidth across parallel flows in scenarios that diverge from [spherical cow in vacuum](https://en.wikipedia.org/wiki/Spherical_cow). Even worse, they claim that:

> [...] Our paper provides a detailed model and rigorous proof that shows how all delay-bounding, delay-convergent CCAs must suffer from such problems.

It seems QoS will remain [spaghetti-throwing black magic](https://archive.psg.com/051000.sigcomm-ivtf.pdf) for a bit longer...
