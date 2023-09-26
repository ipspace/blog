---
title: "Worth Reading: Single-Port LAGs"
date: 2023-09-30 06:01:00
tags: [ switching ]
---
Lindsay Hill described an excellent idea: [all ports on your ~~switches~~ routers should be in link aggregation groups](https://lkhill.com//why-single-port-lag/) even when you have a single port in a group. That approach allows you to:

* Upgrade the link speed without changing any layer-3 configuration
* Do link maintenance without causing a routing protocol flap

It also proves RFC 1925 rule 6a, but then I guess we're already used to that ;)
