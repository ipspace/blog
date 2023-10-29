---
title: "Using Default Route to Reach BGP Next Hops"
date: 2023-11-25 08:22:00
tags: [ BGP ]
draft: True
---
Check FRR 9.1

https://www.linkedin.com/posts/ton31337_frr-openstack-metallb-activity-7123609459964190720-CgYu/?

Also (by Eric Auerswald)

===

Well, I have experienced Arista EOS to follow the *default* route for recursive next-hop resolution of static routes.  Cisco IOS does not do that (just confirmed in the lab).  Someone from Arista was surprised, it might even have been a bug, but that was after the time when we had support contracts for Arista gear so I never opened a case (they took much too long to fix their bugs for us to continue to pay for this so called "support").

Cisco IOS does use a non-default static route for recursive next-hop resolution.  I have never used this in practice, and do not remember having seen that used somewhere.  This does suprise me, too (just tested in a lab).

ExtremeXOS does not follow static routes for recursive next-hop
resolution, it does not even accept the configuration of a next-hop outside a directly connected subnet (the directly connected subnet can be removed later, then recursive next-hop resolution can be tested, it does not happen).

===