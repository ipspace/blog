---
title: "Interesting: Crafting Endless AS Paths in BGP"
date: 2024-07-31 07:53:00+0200
tags: [ worth reading ]
---
Vincent Bernat documented a quirk I hope you'll never see outside of a CCIE lab: [combining BGP confederations with AS-override can generate endless AS paths](https://vincent.bernat.ch/en/blog/2024-bgp-endless-aspath).

I agree entirely with his conclusions (avoid both features). However, I still think that replacing an AS within the confederation part of an AS path (which should belong to a single well-managed AS) is not exactly the most brilliant idea I've seen.
