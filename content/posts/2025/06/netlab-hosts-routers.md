---
title: "netlab 2.0: Routers, Hosts, Gateways and Bridges"
series_title: "Routers, Hosts, Gateways and Bridges"
date: 2025-06-11 08:20:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
In a previous blog post, I explained how you can [use *bridges* in a *netlab* topology to create custom LAN segments](/2025/05/netlab-custom-bridges/). Netlab supports two other [node roles](https://netlab.tools/node-roles/) (*host* and *router*), and we'll eventually add *gateways*.

*netlab* assumes that most network devices are *routers* (it considers a *firewall* to be a router in disguise), apart from Linux *hosts*, but you can always change what a node is with the **role** node attribute:
<!--more-->
* [**host** nodes](https://netlab.tools/node-roles/#hosts) do not *forward* packets[^IOS]. They usually don't have a loopback interface (but you can request one by setting the **loopback** node attribute to **true**) and use *static routing* toward an adjacent **router** node (or anycast/VRRP gateway) instead of routing protocols. Needless to say, they cannot serve as *default gateways* for other hosts.
* [**router** nodes](https://netlab.tools/node-roles/#routers-and-layer-3-switches) should do packet forwarding and advertise themselves as routers using IPv6 RA (if you decide to run IPv6 in your lab topology). They usually have a loopback interface, but you can tell _netlab_ not to create it; simply set the **loopback** node attribute to **false**. They are also supposed to run routing protocols, although you can decide to use static routing.
* **gateway** nodes will be somewhere between the two. Once I find time to write that bit of code, you'll be able to use gateway nodes for layer-3 firewalls.
* [**bridge** nodes](https://netlab.tools/node-roles/#bridges) perform layer-2 forwarding in one or more VLANs. They typically don't have IP addresses, except for the management IP address.

[^IOS]: Cisco IOS is a notable exception. All hell breaks loose if you turn off IPv4 packet forwarding with **no ip routing**.

In theory, any device supported by _netlab_ could be a _router_ if you can create a [loopback interface](https://netlab.tools/nodes/#loopbacks) on it[^ASA], a _host_ if it supports [static routing](https://netlab.tools/module/routing/#generic-routing-static), or a _bridge_ if it supports [VLANs](https://netlab.tools/module/vlan/). In practice, we test the devices (see the second half of the [*initial configuration* test coverage](https://tests.netlab.tools/_html/coverage.initial)) and limit the roles a device can take.

[^ASA]: Cisco ASAv is the only exception I'm aware of.

Does this all make sense? Trying to make a Linux VM or container into a router definitely does not; instead, you should use **bird** or **frr** devices. What about using a Cisco IOS or Arista EOS device as a host? That would give you more realistic [DHCP](https://netlab.tools/module/dhcp/) servers (for example) or single-uplink BGP route reflectors that do not use any other routing protocol but BGP. You can also use this functionality to use devices you're familiar with (for example, Arista cEOS containers or Cisco IOL containers) as end hosts when you need functionality that is not easily accessible on Linux (for instance, traceroute with MPLS labels).

Any other ideas? Please leave a comment!
