---
title: "Worth Reading: Redistributing Your Entire IS-IS Network By Mistake"
date: 2020-08-14 08:57:00
tags: [ IS-IS, worth reading ]
---
Here's an interesting factoid: when using default IS-IS configuration (running L1 + L2 on all routers in your network), every router inserts every IP prefix from anywhere in your network into L2 topology... at least on Junos. 

For more details read 
[this article by Chris Parker](https://www.networkfuntimes.com/redistributing-your-entire-is-is-network-by-mistake-beware-this-default-behaviour/). I also [wrote about that same problem in 2011](/2020/08/worth-reading-default-isis-configuration-prefix-bloat.html).