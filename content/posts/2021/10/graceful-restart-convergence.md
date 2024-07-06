---
date: 2021-10-12 06:35:00+00:00
ha-switching_tag: control
high-availability_tag: external
series:
- ha-switching
tags:
- IP routing
- high availability
- networking fundamentals
title: Graceful Restart and Routing Protocol Convergence
---
I'm always amazed when I encounter networking engineers who want to have a fast-converging network using Non-Stop Forwarding (which implies Graceful Restart). It's even worse than asking for smooth-running heptagonal wheels.

As we [discussed in the Fast Failover series](/2020/11/detecting-network-failure.html), any decent router uses a variety of mechanisms to detect adjacent device failure:

* Physical link failure;
* Routing protocol timeouts;
* Next-hop liveliness checks (BFD, CFM...)
<!--more-->
Dealing with **physical link failures** is easy: it doesn't make sense to pretend life is good if a link is down. Either we're dealing with a genuine link failure, or the adjacent device experienced a severe enough problem so that it cannot pretend to be alive any longer (power outage or linecard blowing up come to mind). The only sane way to deal with the situation is to run a regular routing protocol convergence[^1].

[^1]: Some implementations might treat physical link failure as a cause to start the *Graceful Restart* (at least [according to this Juniper document](https://www.juniper.net/documentation/en_US/junos/topics/concept/bgp-bfd-understanding.html)). Why anyone thinks that forwarding packets into a failed interface/link makes sense is beyond my comprehension.

How about **Hello timeouts**? It could be a genuine device failure with the physical link staying up due to a gazillion of weird reasons. It could also be a planned or unplanned restart of the remote device. In that case, and if the failed device advertised *Non-Stop Forwarding* capability, we shouldn't panic but follow *Graceful Restart* procedures.

What happens next depends on the routing protocol.

**BGP** advertises *Graceful Restart* capability in the BGP OPEN message. If a helper device wants to play along, it should wait for the *Restart Timer* interval (advertised in the same BGP OPEN message) until it flushes the BGP routes advertised by the failed neighbor and starts the convergence process. The default value of the *restart timer* on Cisco IOS XE is 120 seconds; the minimum sane value is the time it takes the remote device to recover. Regardless of the *restart timer* value, the helper device is in routing convergence limbo until that timer expires.

**Conclusion**: When using *Graceful Restart*, BGP convergence could take at least as long as it takes for the slowest device participating in this scheme to restart. The time to react to any topology changes that might have occurred in the meantime is even longer due to how BGP updates are processed when undergoing a *Graceful Restart* (see *[Graceful Restart 101](/2021/09/graceful-restart.html)* blog post for details).

**OSPF** starts the *Graceful Restart* procedure with an opaque LSA that has to be sent by the restarting device. When undergoing a planned restart, the restarting device specifies the desired timeout in the opaque LSA, but at least we know what's going on -- it's a planned procedure, not a device failure.

On the other hand, the only way for an OSPF network to survive an unplanned device failure is to ensure that the OSPF Hello timeout doesn't expire before the failed device restarts. Should you wish to support this scenario, you'll have a ridiculously slow-converging network no matter what.

**Summary**: Non-Stop Forwarding and fast convergence go together as well as oil and ~~water~~ bricks. You could have one or the other.
