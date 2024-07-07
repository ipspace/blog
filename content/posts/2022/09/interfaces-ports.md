---
date: 2022-09-01 06:43:00+00:00
series:
- if_port
tags:
- switching
- IP routing
- networking fundamentals
title: Router Interfaces and Switch Ports
---
When I started implementing the [netlab VLAN module](https://netlab.tools/module/vlan/), I encountered (at least) three different ways of configuring physical interfaces and bridging domains even though the underlying packet forwarding operations (and sometimes even the forwarding hardware) are the same. That [confusopoly](https://en.wikipedia.org/wiki/Confusopoly) is guaranteed to make your head spin for years, and the only way to figure out what's going on behind the scenes is to go back to the fundamentals.
<!--more-->
As is often the case in networking, we got to this morass because vendors believe in "_doing more with less_"[^ML]. As they added bridging functionality to routers or routing functionality to bridges (devices often [called switches by product marketing](/2011/02/how-did-we-ever-get-into-this-switching/)), they rarely changed the terminology or configuration syntax, starting with the way we call those thingies into which we plug cables.

[^ML]: In reality: never refactor working code when an awkward kludge could do.

### Routers Have Interfaces

Decades ago, we called the thingy sitting between a computer and a cable an _interface_ because that's what it was -- an interface between software running on the computer and hardware transporting bits between computers.

If a node had more than one interface and could forward packets between those interfaces, we called it a router[^IBM]. Please note that router interfaces could use different layer-2 technologies, for example Ethernet and Token Ring for LAN connections and Frame Relay or ATM for WAN connections.



A firewall was just a router with more-or-less stateful packet filters inserted in the packet forwarding path, and we called load balancers proxy servers.

[^IBM]: If you're old enough, you might remember misconfiguring OSPF and turning an IBM mainframe into the most expensive router you've ever seen

Now you know why you're configuring _interfaces_ on hosts, routers, firewalls, and load balancers.

### Hubs and Bridges Had Ports

Life was simple (terminology-wise) as long as networking meant connecting your node to an external device that magically transported bits between two or more directly-connected nodes. Local area networks changed all that -- suddenly, you could [plug a cable](/2015/02/lets-get-rid-of-thick-yellow-cable/) directly into your node and start sending packets.

Those cables had physical limitations. For example, the [thin coax cable](https://en.wikipedia.org/wiki/10BASE2) used in early Ethernet networks could not be longer than 185 meters due to signal degradation across longer distances. At the same time, the maximum distance between two nodes on a single Ethernet network (dictated by the collision detection logic) could be significantly larger. A solution was obvious (and used for decades in telephony networks): use a repeater ([also called a hub](https://en.wikipedia.org/wiki/Ethernet_hub)) that would regenerate the signal. The [IEEE Ethernet standard](https://en.wikipedia.org/wiki/5-4-3_rule) allowed you to use up to four repeaters between two stations.

It made no sense to call the hub cable attachment points _interfaces_ because there was nothing behind them but a bit repeater, so we called them _ports_. Contrary to routers, hubs used the same layer-2 technology on all ports.

When DEC introduced bridges (one of the [worst decisions ever made in networking](/2010/07/bridges-kludge-that-shouldnt-exist/)), they decided to use the hub terminology -- bridges had ports.

### The Switching Confusion

Renaming _bridges_ to _switches_ was a pure marketing decision and never went beyond rebranding the devices and creating new marketing collaterals. The configuration mechanisms and the technical documentation didn't change a bit -- like bridges, the original (layer-2) switches had ports.

Eventually, someone implemented layer-3 forwarding in an ASIC, and the obvious way to market that device was to call it a [layer-3 switch](/2012/08/is-layer-3-switch-more-than-router/) even though it should have been called a router[^ABC]... but what do you call a cable attachment point on that device? Is it a port or an interface? Welcome to the switching terminology hell.

[^ABC]: At that point, the bridge vendors calling their devices _switches_ loudly sang the "_switching is good, routing is bad_" mantra for years. They couldn't possibly call their new gizmo a router.

A layer-2 switch (bridge) has _ports_. A layer-3 switch (a router) has interfaces, but it could do bridging and routing simultaneously, in which case it has both. That's why you have `switchport` configuration command in Cisco IOS, Nexus OS, and Arista EOS -- it means "_I want to treat this physical interface as a bridge port._" Likewise, the `no switchport` configuration command means "_I want to treat this physical interface as a router interface._" So far, so good, but why do we have SVI interfaces and VLAN subinterfaces?

To get there, we will have to walk through the strange land of routers doing bridging and take a detour through the VLAN Forest of Despair. Stay tuned.

{{<next-in-series page="/posts/2022/09/routers-bridges-crb-irb.md" />}}