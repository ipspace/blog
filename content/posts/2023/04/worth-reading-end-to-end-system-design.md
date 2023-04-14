---
title: "MUST READ: End-to-End Arguments in System Design"
date: 2023-04-23 07:46:00
tags: [ worth reading ]
---
In case you ever wondered how old the "_keep network simple and do complex stuff at the endpoints_" approach is, read the 
[End-to-End Arguments in System Design](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf) article from 1981.

For whatever reason (hint: profits), networking vendors [keep ignoring those arguments](https://blog.ipspace.net/2013/06/network-virtualization-and-spaghetti.html), turning the network into a kitchen sink of complexity.

**Fun tidbit**: the article describes a variant of [relying on layer-2 checksums will corrupt your data](https://blog.ipspace.net/2013/03/does-dedicated-iscsi-infrastructure.html). Some things never change.
