---
date: 2009-11-17 06:52:00.002000+01:00
tags:
- OSPF
title: 'Challenge: OSPF Neighbor Changing State from DOWN to DOWN'
url: /2009/11/challenge-ospf-neighbor-changing-state.html
---
Here's an interesting behavior I was able to create in a lab connecting two routers with a serial link:

```
*19:34:42.765: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.1 on Serial1/0 from →
  EXSTART to DOWN, Neighbor Down: Too many retransmissions
*19:35:42.773: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.1 on Serial1/0 from →
  DOWN to DOWN, Neighbor Down: Ignore timer expired
```

The messages are repeated approximately every three minutes (using the default OSPF timers).

The challenge: what was going on and how was I able to produce these messages?
