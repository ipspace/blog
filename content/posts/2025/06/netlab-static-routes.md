---
title: "Static Routes in netlab Lab Topologies"
series_title: Static Routes
date: 2025-06-23 07:50:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
As much as we'd love everything in our networks to be dynamic, auto-configured, or software-defined, reality often intervenes and forces us to use *static routes*, so we needed a mechanism to specify them in _netlab_ lab topologies.

A static route has two components: the destination prefix and the next hop -- the device that we hope knows how to reach that destination. The next hop is usually specified as an IPv4 or IPv6 address, but may also include outgoing interface information[^DSR].
<!--more-->
[^DSR]: Please allow me to ignore the static routes pointing to interfaces and hoping Some Magic will intervene and [make it all work](https://blog.ipspace.net/2009/10/follow-up-interface-default-route/).

One of the beauties of _netlab_ is that it takes over the IPAM chores; link subnets and interface addresses are assigned automatically. Our static route data structures had to reflect this; we couldn't expect you to assign static IP addresses to node interfaces just to be able to specify them as next hops in static routes.

{{<long-quote>}}
The static routes are part of the [generic routing](https://netlab.tools/module/routing/) configuration module. They were introduced in release 1.9.3, with **gateway** support added in release 1.9.6 and **discard** next hop added in release 25.06.

You can use static routes on a [dozen different platforms](https://netlab.tools/module/routing/#id7). Some of those platforms have challenges with inter-VRF static routes; see the [integration test results](https://release.netlab.tools/_html/coverage.routing) (the bottom of the page) for more information.
{{</long-quote>}}

A _netlab_ [static route](https://netlab.tools/module/routing/#static-routes) thus has [these components](https://netlab.tools/module/routing/#configuring-static-routes):

* The destination prefix, which can be specified as **ipv4** or **ipv6** prefix, but also as an address **pool**, a [named **prefix**](https://netlab.tools/prefix/#named-prefixes) or a **node** loopback interface.
* The next hop (specified within the **nexthop** dictionary), which can also be an **ipv4** or **ipv6** address (in case you really want to use static addresses), the next hop **node**, or the default **gateway**. A static route can also be a **discard** route (pointing to *null* interface).
* Optional VRF information -- the **vrf** in which the static route should be installed and the **nexthop.vrf** if you want to do inter-VRF static routing. 

The static routes are specified for individual **[nodes](https://netlab.tools/nodes/)** (or **[groups of nodes](https://netlab.tools/groups/)**) in the **routing.static** attribute[^GSR] 

[^GSR]: We'll talk about [global static routes](https://netlab.tools/module/routing/#global-static-routes) in another blog post.

For example, this is all you have to do if you want R1 to have a default route pointing to R2.

{{<printout>}}
module: [ routing ]

nodes:
  R1:
    routing.static:
    - ipv4: 0.0.0.0/0
      nexthop.node: R2
  R2:
  
links: [ R1-R2 ]
{{</printout>}}

**Notes:**

* Static routes are part of the [generic routing configuration module](https://netlab.tools/module/routing/) that has to be active on the node(s) using the static routes (line 1)
* We didn't have to specify the IP address of R2 or the outgoing interface; _netlab_ takes care of that automatically (line 7)

If you want to do the same for a bunch of hosts, you can define static routing for a group of nodes. It's worth noting that even though every host has to use a different IP address as the next hop (each host is in a different subnet), _netlab_ takes care of that behind the scenes; all you need to know is the node name of the next hop.

```
nodes: [ H1, H2, H3, R ]

groups:
  hosts:
    members: [ H1, H2, H3 ]
    device: linux
    module: [ routing ]
    routing.static:
    - ipv4: 0.0.0.0/0
      nexthop.node: R

links: [ H1-R, H2-R, H3-R ]
```

How about a static route toward a default gateway? Absolutely not a problem if you're using the [first-hop gateway](https://netlab.tools/module/gateway/) on the LAN segment. In the following lab topology[^LI], S1 and S2 have an anycast gateway, and the host (H) is using it as the next hop of the default route:

[^LI]: Read [this blog post](/2025/01/netlab-link-definitions/) if you're wondering what the **interfaces** list is doing in the link definition.

```
nodes:
  H:
    module: [ routing ]
    routing.static:
    - ipv4: 0.0.0.0/0
      gateway: True
  S1:
    module: [ gateway ]
  S2:
    module: [ gateway ]

links:
- interfaces: [ H, S1, S2 ]
  gateway.protocol: anycast
```

Finally, how about a typical Internet access scenario where the customer and the ISP use static routing? We don't have an elegant answer for this one yet[^R2506]; you have to specify a static IPv4 prefix on the customer LAN subnet and use that prefix in the static route on the ISP router[^NP]:

[^R2506]: As of release 25.06. Stay tuned ;)

[^NP]: You could use named prefixes, but that just adds another layer of indirection.

{{<printout>}}
module: [ routing ]
defaults.device: eos
provider: clab

nodes:
  ce:
    routing.static:
    - ipv4: 0.0.0.0/0
      nexthop.node: pe
  pe:
    routing.static:
    - ipv4: 192.168.42.0/24
      nexthop.node: ce

links:
- pe-ce
- ce:
  prefix.ipv4: 192.168.42.0/24
{{</printout>}}

**Note:**

* The implementation of static routes in _netlab_ release 25.06 does not allow you to refer to a link prefix (unless you're using **named prefixes**). We have to specify a static IPv4 prefix for the CE LAN subnet (line 18) and use that prefix as the destination prefix on the PE-router (line 12)
