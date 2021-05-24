---
title: "Intricate AWS IPv6 Direct Connect Challenges"
date: 2021-06-13 08:19:00
tags: [ AWS, IPv6 ]
---
In his _[Where AWS IPv6 networking fails](https://www.oasys.net/posts/where-aws-ipv6-networking-fails/)_ blog post, Jason Lavoie documents an intricate consequence of [2-pizza-teams not talking to one another](https://www.lastweekinaws.com/blog/new-ceo-onboarding-at-aws/): it's really hard to get IPv6 in AWS VPC working with Transit Gateway and Direct Connect in large-scale multi-account environment due to the way IPv6 prefixes are propagated from VPCs to Direct Connect Gateway. 

It's one of those IPv6-only little details that you could never spot before stumbling on it in a real-life deployment... and to make it worse, it works well in IPv4 if you did proper address planning (which you can't in IPv6).
