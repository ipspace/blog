---
title: "Setting Source IP Address on Traffic Started by a Multihomed Host"
date: 2023-09-28 11:20:00
tags: [ IP routing, TCP ]
draft: True
---
https://blog.ipspace.net/2023/05/failure-detection-server-dual-homing.html#1855

One annoyance is what IP address gets used by default by the system for outbound traffic. It would be nice to have a generic OS-level way to say "this IP on lo0 should be default for outbound IP traffic unless to the connected link subnet itself".

Obviously some software allows you to specify the source IP to use, but again more complexity in config. And some doesn't. I've solved it before with an iptables/nft SNAT rule for everything not on the connected subnet, but again it's messier than one would like.