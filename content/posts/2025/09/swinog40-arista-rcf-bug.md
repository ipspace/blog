---
title: "SwiNOG 40: When a Routing Control Functions Is Too Fresh"
date: 2025-09-17 07:33:00+0200
tags: [ BGP ]
---
During integration testing, I find [unexpected quirks in network devices](/tag/netlab/#quirks) way too often. However, that's infinitely better than experiencing them in production (even after thoroughly testing stuff) while discovering that your peers don't care about routing security, RPKI, and similar useless stuff.

For example, what happens if you define a new Routing Control Function (RFC) on Arista EOS and apply it to BGP routing updates *in the same configuration session*? You'll find out in the [Sorry We Messed Up](https://www.swinog.ch/wp-content/uploads/2025/06/Stefan-Funke-Inter.link-Sorry-we-messed-up.pdf) ([video](https://youtu.be/f1jF0zpMol0)) presentation Stefan Funke had at  [SwiNOG 40](/2025/06/swinog/) (note: the bug has been fixed in the meantime).