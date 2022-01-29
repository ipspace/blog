---
title: "BGP Route Reflector Myths"
date: 2022-02-08 07:54:00
draft: True
tags: [ BGP ]
---
Here's an I encountered two BGP route reflector myths in the last few weeks:

* You don't need IBGP sessions between BGP route reflectors
* In a redundant design, you should use Route Reflector Cluster ID to avoid loops.

Time for another myth-busting blog post (aka [Duty Calls](https://xkcd.com/386/)).

### IBGP Sessions Between BGP Route Reflectors

