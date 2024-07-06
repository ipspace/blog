---
date: 2021-10-26 06:52:00+00:00
high-availability_tag: external
series:
- ha-switching
tags:
- IP routing
- high availability
title: Interactions Between BFD and Graceful Restart
---
_We have school holidays this week, so I'm reposting wonderful comments that would otherwise be lost somewhere in the page margins. Today: Dmitry Perets on the [interactions between BFD and GR](/2021/10/graceful-restart-bfd.html#804)_.

---

Well, assuming that the C-bit is set honestly (will be funny if not) and assuming that the Helper is using this bit correctly (and I think it's pretty well defined what "correctly" means - see section 4.3 in RFC 5882), the answer is pretty clear.
<!--more-->
IF you do not have any alternative path, then the only reason to use BFD is to show off; so grow up and stop using it.

IF you do have an alternative path, but the device in question sends C=0, then it means that BFD on that device is sharing fate with the control plane. Hence, from the Helper perspective, if BFD is lost, it means nothing. The Helper has no way of knowing whether it should flush the routes (forwarding plane failure) or start the GR (control plane failure). Juniper SRX (and I think also QFX) is an example of this: BFD is handled by the Routing Engine there, and hence it is not CP-independent. And they honestly set C=0. So what will Helper choose to do, when BFD goes down - will it flush the routes or will it start helping GR? A few Helper implementations I saw (including Juniper) will opt for the latter, because otherwise GR would never be able to work - almost surely, BFD will go down before the restarting router manages to send a new BGP Open, as it normally should. BUT... starting GR unconditionally, of course, means that now BFD will never be able to work. Lose-lose situation. In the Juniper document that was shared in the blog post, they describe "dont-help-shared-fate-bfd-down" option, which was apparently added at some point (I never used it), and it seems to control exactly this: choosing between GR-that-never-works and BFD-that-never-works. This way or another - BGP + GR + BFD_C=0 sounds like a bad idea.

IF you do have an alternative path and the device in question proudly sends C=1, then you are lucky. Juniper MX is such an example, because they support "Distributed BFD" and "Inline BFD", both of which are implemented on the line cards and can survive Routing Engine reboot. So, any well-implemented Helper should now be able to distinguish between forwarding plane failure (BFD goes down => flush all routes) and control plane failure (BFD stays up => start helping GR as usual). Hence, BGP + GR + BFD_C=1 sounds like not a bad idea to me...

