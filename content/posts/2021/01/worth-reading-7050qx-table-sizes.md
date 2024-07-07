---
title: "Worth Reading:  Understanding Table Sizes on the Arista 7050QX-32"
date: 2021-01-31 08:06:00
tags: [ fabric ]
---
Arista published a blog post describing the details of 
[forwarding table sizes on 7050QX-series switches](https://eos.arista.com/understanding-table-sizes-7050x/). The description includes the *base mode* (fixed tables), *unified forwarding tables* and even the IPv6 LPM details, and dives deep into what happens when the switch runs out of forwarding table entries.

Too bad they're describing an ancient Trident-2 ASIC (I last mentioned switches using it in 2017 [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics) update). Did [NDA](/2016/05/what-are-problems-with-broadcom/) expire on that one?
