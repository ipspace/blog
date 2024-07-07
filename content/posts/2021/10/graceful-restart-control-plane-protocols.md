---
date: 2021-10-05 06:39:00+00:00
ha-switching_tag: control
high-availability_tag: external
series:
- ha-switching
tags:
- IP routing
- high availability
- networking fundamentals
title: Graceful Restart and Other Control Plane Protocols
---
In the [Graceful Restart 101](/2021/09/graceful-restart/) blog post, I promised to discuss the ugly parts of this concept in a follow-up post. It turns out we'll need more than one; today, we'll focus on other control plane protocols in an access network scenario.

Imagine an access router with multiple uplinks serving a bunch of non-redundantly-connected customers:

{{<figure src="/2021/09/GR-access-router.png" caption="Non-redundant access network">}}
<!--more-->
Graceful Restart solves routing protocol issues on the router-to-router links. It does not address the lack of other control plane protocols during the device restart period. The situation is functionally identical to controller failure in an OpenFlow network, so you might want to read the *[Impact of Controller Failures in Software-Defined Networks](/2019/06/impact-of-controller-failures-in/)* blog post first and follow the links.
 
To make a long story short:

* Adjacent devices might bring down port channels due to lack of LACP messages[^1]
* Adjacent devices might also time out entries from their ARP caches. There's nothing you can do on end hosts; I'm positive at least some vendors figured this one out and keep ARP caches intact when performing Graceful Restart (comments welcome).
* Any attached bridged network will also notice a lack of STP messages and go through a topology change process[^2]
* Devices using the access router as a DHCP server might lose their DHCP delegations.
* Anything else? Please write a comment.

Most of these issues are gone when you add Stateful Switchover (SSO) capability to the device (assuming it works as advertised, more details in [this blog post](/2021/09/stateful-switchover/)):

* ARP is trivial -- the second control plane instance does nothing more than sending an ARP reply with its IP and MAC address.
* LACP is easy to take over -- the second control plane instance keeps sending LACP messages.
* STP and DHCP require state sharing across control plane instances, but that's what SSO is supposed to be doing anyway.

**Conclusion**: Using Non-Stop Forwarding and Graceful Restart in a non-redundant access network might be better than nothing. While you can make the routing protocols survive a device restart, other control plane protocols might fail unless you're using access routers with redundant internal architecture[^3].

[^1]: Arista EOS schedules LACP messages in advance when performing [Smart System Upgrade](https://www.arista.com/en/um-eos/eos-leaf-smart-system-upgrade-leaf-ssu) -- see the [Non-Stop Forwarding](/2021/09/non-stop-forwarding/) blog post for details. That trick doesn't work when a device crashes; the proof is left as an exercise for the reader.

[^2]: Arista EOS Smart System Upgrade treats STP the same way it treats LACP. I'm positive there's a situation where you can get a nice forwarding loop due to the stale STP state in the restarting device.

[^3]: Keeping your fingers crossed to make sure SSO works, and making regular sacrifices to keep the gods of Byzantine Failures happy.
