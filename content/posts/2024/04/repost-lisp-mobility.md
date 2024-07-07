---
title: "Repost: The Real LISP Mobility Use Case"
date: 2024-04-30 07:59:00+0200
tags: [ LISP ]
---
[Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/) is working on an interesting challenge: building ground-to-airplane(s) networks providing multilink mobility. Due to its relative simplicity, he claims [LISP works much better than BGP in that environment](/2024/04/mobility-campus-networks-lisp-evpn/#2218).

---

In some newer routers BGP would not be such a big bottleneck, but you need a lot of knob turning in BGP to get it right, while in LISP it is quite simple.

If you have many thousands concurrent airplanes with multi-link and max. 16 subnets with different routing policies on each, and the radio links are going up and down, then you have a large number of mobility events.
<!--more-->
This is where LISP with PUBSUB is excellent. BGP is not designed for mobility and in such an extreme environment would be a serious bottleneck, potentially making impossible to fulfill the safety performance requirements.

Victor Moreno published once an exercise with moving robots in factory environment where similar mobility performance was required. LISP was the right fit for that.

It is a totally different use case of LISP than most people would think about. Valid only with PUBSUB. Still some points are missing to make this solution complete. Reliable transport shall be standardized. We need subnetwork mobility support in MS/MR. Some LCAF extension and implementation would be handy.

However, I see no good alternative. PMIPv6 is a candidate, but it has no support for full multilink with policies yet. For me LISP is the best mobility protocol, a replacement for PMIPv6, not a replacement for BGP. Actually, in the RLOC space underlay you would typically have a telco network with a lot of BGP.

---

He also provided some [interesting details about anchorless mobility](/2024/04/mobility-campus-networks-lisp-evpn/#2203) (mobile IP solution without a home gateway):

---

You assume anchored mobility for option one. This is unacceptable for safety critical networks. You should have mobility without an anchor point. Exactly that is what LISP provides for you. A fully distributed data plane without any single point of failure. The control plane is centralized logically, but could be fully distributed, even geo-redundant physically. You might say that single point of failures are not an issue in most networks. But in other networks this might be not acceptable.

For option two, with BGP you cannot reach the same speed of mobility and scale, because of the complex BGP path selection algorithm. On the same CPU LISP will be always much faster. Cisco once did an in-house race on this issue. LISP was the clear winner against the best BGP experts available inside Cisco. BTW, Boeing Connexion failed miserably many years ago with BGP based mobility.

If mobility is not an issue, you might be happy with option one, then EVPN might be good enough. If you need distributed anchorless mobility, than LISP will be always better by architecture.

LISP is especially a good fit for parallel active multilink mobility using Priority and Weight. PMIPv6 cannot do the same. BGP also does not have anything standardized for such scenarios. Few networks would need that today, but probably in the future all moving vehicles will have higher safety and security requirements. Then LISP is an easy natural solution. While all other protocols has to be redefined and implemented new. Even 3GPP does not have a comparable mobility solution yet.
