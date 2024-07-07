---
date: 2021-10-19 06:51:00+00:00
ha-switching_tag: control
high-availability_tag: external
series:
- ha-switching
tags:
- IP routing
- high availability
- networking fundamentals
title: Graceful Restart and BFD
---
The whole *High Availability Switching* series started with a question along the lines of "*does it make sense to run BFD together with Graceful Restart*". After *[Non-Stop Forwarding 101](/2021/09/non-stop-forwarding/)*, *[Graceful Restart 101](/2021/09/graceful-restart/)*, and *[Graceful Restart and Convergence Speed](/2021/10/graceful-restart-convergence/)* we finally have enough information to answer that question.

**TL&DR**: Most probably not.

A more nuanced answer depends (as always) on a gazillion implementation details.
<!--more-->
**BFD implemented in forwarding hardware**. This is the best option -- BFD detects data plane failures, and routing protocol(s) detect control plane failures. BFD failure should trigger regular routing protocol convergence, and routing protocol timeouts should trigger *Graceful Restart* procedures.

**BFD sharing fate with the control plane**. A control plane failure (which would trigger *Graceful Restart*) would also result in BFD session failure. BFD failure *could* be used to enter *Graceful Restart* procedure (and start the *Restart Timer*) before the routing protocol detects a neighbor failure. However, BFD failure **should not** be used to flush the forwarding tables or start the routing protocol convergence.

You'll find more details in *[Generic Application of BFD](https://datatracker.ietf.org/doc/html/rfc5882)* (RFC 5882).

### Moving from Theory to Practice

If you insist on using BFD with Graceful Restart, get reliable answers to these questions (or do the tests yourself):

* Can the helper nodes decouple BFD and routing protocol failure detection and start an unconditional convergence or *Graceful Restart*  as needed?
* Is the behavior following a BFD failure configurable?
* Does the helper node use the *Control Plane Independent* bit in BFD control messages to change its behavior?

I tried to find out the implementation details of *Graceful Restart* and BFD interactions. The closest I got was:

* [This Junos document](https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/task/graceful-restart-for-routing-protocols-configuring.html) which totally confused me
* [Cisco IOS XE BGP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16-12/irg-xe-16-12-book/bgp-nonstop-forwarding-awareness.html) saying "*‌Configuring both Bidirectional Forwarding Detection (BFD) and BGP graceful restart for NSF on a device running BGP may result in suboptimal routing.*" which supports my TL&DR conclusions ;)
* An Arista EOS document (behind a regwall) effectively saying "*Our Stateful Switchover is fast enough that a BFD session doesn't go down. You can therefore use BFD with BGP Graceful Restart*."

Hands-on experience would be highly appreciated -- please write a comment!
