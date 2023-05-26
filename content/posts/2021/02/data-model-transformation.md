---
title: "Data Model Transformations in Network Automation Solutions"
date: 2021-02-18 07:47:00
tags: [ automation ]
series: [ ssot ]
ssot_tag: details
---
Last year I wrote an article describing data model optimization going from a simple *[this is what we need to configure individual devices](/kb/DataModels/index.html)* to a highly polished high-level *[network nodes and links](/kb/DataModels/40-Link%20Prefixes.html)* model. Not surprisingly, as [Jeremy Schulman](https://www.ipspace.net/Author:Jeremy_Schulman) was quick to point out, the latter one had Jinja2 templates you wouldn't want to debug. Ever. You can't run away from complexity... but you can manage it.

Many successful network automation solutions (example: Cisco NSO) solve the "*we'd love to work with high-level data models but hate complex templates*" challenge with *data transformation*: operators work with an abstracted data model describing services, nodes and links, and the device configuration templates use low-level data derived from the abstracted data models through a series of *business logic* rules or lookups (aka *network design*). 
<!--more-->
{{<figure src="dm-magic.png" caption="High-level overview of the process">}}

{{<note>}}Some vendors love to call this approach *[intent-based networking](/tag/intent-based-networking.html)* because it sounds sexier than *network automation done right*.{{</note>}}

The multi-level data model approach might look unnecessarily complex until you're trying to implement a multi-vendor solution, or a solution that could be adapted to multiple network designs. Whenever you have to deal with multiple abstractions (at the top) or multiple target platforms (at the bottom), using a standardized device-/node-level data model that is as close to device configuration as possible is the only way to stay sane.

{{<figure src="dm-multi-platform.png" caption="Multi-platform automation solution">}}

Sounds too abstract? No worries, here are the details: I extended the original *[data model optimization](/kb/DataModels/index.html)* article with an *[overview of data model transformation concepts](/kb/DataModels/65-Data-Transformation.html)*, and a *[data transformation example](/kb/DataModels/66-Transformation-Example.html)* (the [source code is on GitHub](https://github.com/ipspace/ansible-examples/tree/master/Data-Models/Transformation)).

{{<jump>}}[Keep reading](/kb/DataModels/65-Data-Transformation.html){{</jump>}}
