---
title: "Worth Reading: Faster than Dijkstra?"
date: 2026-03-03 07:43:00+0100
tags: [ worth reading ]
---
Bruce Davie published a nice article explaining why 
[it makes little sense](https://systemsapproach.org/2026/02/09/faster-than-dijkstra/) to use an algorithm that's [supposedly faster than Dijkstra's](https://www.quantamagazine.org/new-method-is-the-fastest-way-to-find-the-best-routes-20250806/) in link-state routing protocols.

Other interesting data points from the article (and linked presentations):

* People are running (a few) thousands of routers in a single area
* Running Dijkstra's algorithm on an emulated network with 2000 nodes took 100 msec... in 2003 (page 18 of [this NANOG presentation](https://archive.nanog.org/meetings/nanog29/presentations/filsfils.pdf)).

It turns out (as I expected) that all the noise about the [need for new routing protocols](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on/) we were experiencing a few years ago was either due to bad implementations or coming from nerds looking for new toys to play with.