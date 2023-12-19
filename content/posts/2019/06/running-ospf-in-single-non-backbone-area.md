---
date: 2019-06-13 07:42:00+02:00
ospf_tag: areas
tags:
- OSPF
title: Running OSPF in a Single Non-Backbone Area
url: /2019/06/running-ospf-in-single-non-backbone-area.html
---
One of my subscribers sent me an interesting puzzle:

> One of my colleagues configured a single-area OSPF process in a customer VRF customer, but instead of using **area 0**, he used **area 123 nssa**. Obviously it works, but I was thinking: "*What the heck, a single OSPF area MUST be in Area 0*"

Not really. OSPF behaves identically within an area (modulo stub/NSSA behavior) regardless of the area number. Even there, you could argue that the only difference between area 0 and other areas is that the standard (and all compliant implementations) doesn't allow you to set *stub* or *NSSA* bit in area 0.
<!--more-->
The fundamental difference between area 0 and other areas arises when you connect multiple areas. OSPF behaves like a distance-vector protocol across area boundaries, and the area number serves as a split-horizon mechanism; inter-area routes are not propagated across non-backbone areas.

{{<note info>}}
I explained that a long time ago in an article that's probably long gone from the face of the Internet. I will try to find the source text and republish it.
{{</note>}}

So yes, running OSPF in a single area is perfectly fine. Using area# 123 and making it an NSSA area is also okay. Does it make sense? There might be some other design requirement we're not aware of, but all other things being equal, I'd always prefer area 0 over anything else to keep things obvious.
