---
date: 2008-10-07 06:56:00+02:00
eigrp_tag: deploy
tags:
- EIGRP
title: Leak Map Confusion
url: /2008/10/leak-map-confusion.html
---
A short question I\'ve got from Shahid Rox:

> Today I read your article about scaling EIGRP using stub routers. I was wondering whether you can use the **leak map** *only* for routes learned from other EIGRP neighbors? Is it also usable to filter connected routes?

**Leak-map** controls what its name implies: the leakage of routes received from EIGRP neighbors to other EIGRP neighbors. To filter connected prefixes redistributed into EIGRP, use the **route-map** on **redistribute connected** command. The only way I\'ve figured out to filter announcements of directly connected networks that are part of the EIGRP process is the **distribute-list out** command.
