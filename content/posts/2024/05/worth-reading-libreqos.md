---
title: "Worth Exploring: LibreQoS"
date: 2024-05-08 08:46:00+0200
tags: [ worth reading, QoS ]
---
Erik Auerswald pointed me to an interesting open-source project. 
[LibreQoS](https://libreqos.io/) implements decent QoS using software switching on many-core x86 platforms. It's implemented as a bump-in-the-wire software solution, so you should be able to plug it into your network just before a major congestion point and let it handle the packet dropping and prioritization.

Obviously, the concept is nothing new. I wrote about a [similar problem in xDSL networks](/2009/06/adsl-qos-basics.html) in 2009.
