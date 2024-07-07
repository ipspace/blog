---
title: "Repost: State of Lisp Implementations (2024)"
date: 2024-05-07 08:21:00+0200
tags: [ LISP ]
---
You might remember [Béla Várkonyi's](https://www.linkedin.com/in/belavarkonyi/) use of LISP to build resilient ground-to-airplane networks from [last week's repost](/2024/05/repost-lisp-mobility/). It seems he's not exactly happy with the current level of LISP support, at least based on what he wrote as a response to [Jeff McLaughlin's](https://www.linkedin.com/in/ccie14023/) [claim](/2024/04/mobility-campus-networks-lisp-evpn/#2211) that "_I can tell you that our support for EVPN does not, in any way, indicate the retirement of LISP for SD-Access._":

---

Nice to hear the Cisco intends to support LISP. However, it is removed from IOS XR already. So it is not that clear...

If Cisco will stop supporting LISP, then we will be forced to create our own LISP routers, since we need it for extreme mobility environments.
<!--more-->
It would be still beneficial to have a second LISP router supplier. Unfortunately, the early LISP implementers stopped all development many years ago, so they are useless as alternative suppliers, since PUBSUB is not provided and some other features are also missing. ONOS and ODL implementations are also orphaned and useless.

In safety critical networks, we always need diversity in suppliers, too. However, now we are forced to work on technology diversity, so we have to find a way to make PMIPv6 to work reasonably well. It will be a challenging task.

We will have to present a combined mobility network with parallel LISP and PMIPv6 mobility backbones, where the end user would not see any functional limitations in multi-link mobility.

---

Béla is experiencing a common problem when trying to use a niche technology for a niche use case. You might be the only one doing it, so no vendor is interested in supporting you. After all, vendors have to justify R&D investments and will throw money at whatever is selling best, dropping technologies with insignificant adoption like hot potatoes (remember Cisco IOS Performance Routing?).

The only way to survive in this ridiculous world is to keep your network design as simple as possible and solve interesting challenges at the network edge using software you can control.
