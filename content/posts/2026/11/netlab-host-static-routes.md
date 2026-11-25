---
title: "netlab: Static Routes on Host Nodes"
date: 2026-11-30 07:18:00+0100
tags: [ netlab ]
netlab_tag: guidelines
series_title: "Static Routes on Host Nodes"
---
[Ievgen Bondarenko](https://github.com/ibondarenko1) published an [interesting conundrum](https://github.com/ipspace/netlab/discussions/4098) in a GitHub discussion: _netlab_ does not configure the required static routes on Linux containers if you use custom IP prefixes. Here's the gist of his lab topology ([read this first](/2026/08/netlab-compress-lab-topology/) if you can't figure out why the following YAML works):

```
provider: clab

nodes:
  rtr.device: frr
  h1.device: linux
  h2.device: linux

links:
- h1.ipv4: 10.231.31.10/24
  rtr.ipv4: 10.231.31.1/24
- h2.ipv4: 10.231.32.1/24
  rtr.ipv4: 10.231.32.10/24
```

After starting the lab, H1 cannot reach H2, but if you change h1/h2 device type to `eos` (while setting `role: host`), everything works.
<!--more-->
The details of this seemingly bizarre behavior are described in the *[hosts](https://netlab.tools/node/roles/#hosts)* part of netlab documentation:

* Hosts get static routes toward the nearest gateway (router). H1 and H2 will get static routes with the adjacent RTR IP address as the next hop.
* Hosts with a management VRF get a default route.
* Hosts that do not use VRFs (for example, Linux containers) already have a default route pointing to the management network default gateway. You might need that default route to install additional software or communicate with outside servers or clients, so we decided not to touch it.
* Having no better idea, *netlab* configures static routes *for all address pools* on Linux hosts (and other host devices without a management VRF).
* This limitation applies only to IPv4. _netlab_ removes the IPv6 default route from the management network and relies on in-lab RA messages to generate the IPv6 default route.

Based on the above rules, it's no surprise that H1 gets a set of static routes pointing to RTR (one per address pool), plus the default route created by *containerlab* and pointing to the "outside" default gateway:

{{<printout caption="Static routes on H1 (Linux container)">}}
h1:/# ip route
default via 192.168.121.1 dev eth0
10.0.0.0/24 via 10.231.31.1 dev eth1
10.1.0.0/16 via 10.231.31.1 dev eth1
10.2.0.0/24 via 10.231.31.1 dev eth1
10.231.31.0/24 dev eth1 scope link  src 10.231.31.10
172.16.0.0/16 via 10.231.31.1 dev eth1
192.168.121.0/24 dev eth0 scope link  src 192.168.121.102
{{</printout>}}

In case you're wondering where the above IP prefixes came from: these are the default (predefined) _netlab_ pools:

| Pool | IPv4 | Prefix | Other |
|---|--:|--:|---|
| **l2only** |   |   | L2 only |
| **lan** | 172.16.0.0/16 | 24 |   |
| **loopback** | 10.0.0.0/24 | 32 |   |
| **mgmt** | 192.168.121.0/24 | 24 | start: 100, mac: CA-FE-00-00-00-00 |
| **p2p** | 10.1.0.0/16 | 30 |   |
| **router_id** | 10.0.0.0/24 | 32 |   |
| **vrf_loopback** | 10.2.0.0/24 | 32 |   |
{.fmtTable}

Next, let's change the definition of H1 to be an EOS device acting as a host:

{{<printout caption="H1 is an Arista EOS device running as an IP host">}}
nodes:
  h1:
    device: eos
    role: host
{{</printout>}}

As cEOS has a management VRF, *containerlab* adds a default route into the *management* VRF on H1, and _netlab_ adds a default route pointing to RTR in the global routing table:

{{<printout caption="VRF and global IP routing table on H1 running Arista cEOS">}}
h1#show vrf
Maximum number of VRFs allowed: 1024
   VRF              Protocols       State         Interfaces
---------------- --------------- ---------------- ----------
   default          IPv4            no routing    Et1
   default          IPv6            no routing
   management       IPv4            no routing    Ma0
   management       IPv6            no routing    Ma0
...
h1#show ip route vrf management | begin Gateway
Gateway of last resort:
 S        0.0.0.0/0 [1/0]
           via 192.168.121.1, Management0
...
h1#show ip route | begin Gateway
Gateway of last resort:
 S        0.0.0.0/0 [1/0]
           via 10.231.31.1, Ethernet1
...
{{</printout>}}

OK, now that we know what's going on, how do we make H1 reach H2 in our initial topology? Apart from creating a management VRF on Linux hosts (which _netlab_ doesn't do at the moment), we have three options:

### Option A: Use the routing Module

You can use the *[routing](https://netlab.tools/module/routing/)* module on H1 and H2 and add user-defined [static routes](https://netlab.tools/module/routing/#static-routes). I created a *[node group](https://netlab.tools/groups/)* (to make the same settings apply to both hosts) and defined a static route for a supersubnet (if that's a word) of the two IP prefixes [pointing](https://netlab.tools/module/routing/#configuring-static-routes) to whatever the default gateway is:

{{<printout caption="A node group defining the static route for the Linux containers">}}
groups:
  linux_hosts:
    members: [ h1, h2 ]
    module: [ routing ]
    routing.static:
    - ipv4: 10.231.0.0/16
      nexthop.gateway: True
{{</printout>}}

When the *routing* module is used on hosts, _netlab_ does not create automatic static routes. What we have in the IP routing table is what we defined in the lab topology (plus the default route added by *containerlab*):

{{<printout caption="Static routes configured by the routing module">}}
$ netlab connect h1 ip route
Connecting to container clab-X-h1, executing ip route
default via 192.168.121.1 dev eth0
10.231.0.0/16 via 10.231.31.1 dev eth1
10.231.31.0/24 dev eth1 scope link  src 10.231.31.10
192.168.121.0/24 dev eth0 scope link  src 192.168.121.102
{{</printout>}}

### Option B: Use a Custom Address Pool

_netlab_ creates automatic static routes for all [address pools](https://netlab.tools/addressing/) defined in the lab topology. If we define an extra address pool, we'll automatically get another static route:

{{<printout caption="Defining a custom address pool in the lab topology">}}
addressing:
  static.ipv4: 10.231.0.0/16
{{</printout>}}

Here's the resulting IP routing table on H1

```
$ netlab connect h1 ip route
Connecting to container clab-X-h1, executing ip route
default via 192.168.121.1 dev eth0
10.0.0.0/24 via 10.231.31.1 dev eth1
10.1.0.0/16 via 10.231.31.1 dev eth1
10.2.0.0/24 via 10.231.31.1 dev eth1
10.231.0.0/16 via 10.231.31.1 dev eth1
10.231.31.0/24 dev eth1 scope link  src 10.231.31.10
172.16.0.0/16 via 10.231.31.1 dev eth1
192.168.121.0/24 dev eth0 scope link  src 192.168.121.102
```

### Option C: Redefine an Existing Pool

This is what Ievgen decided to do. He modified the definition of the LAN pool (because all his LAN subnets have static IPv4 addresses):

{{<printout caption="Redefining the IPv4 prefix of the LAN address pool">}}
addressing:
  lan.ipv4: 10.231.0.0/16
{{</printout>}}

As expected, the IP routing table on H1 has the 10.231.0.0/16 prefix but not the 172.16.0.0/16 one (which was previously used for the **lan** pool):

```
$ c h1 ip route
Connecting to container clab-X-h1, executing ip route
default via 192.168.121.1 dev eth0
10.0.0.0/24 via 10.231.31.1 dev eth1
10.1.0.0/16 via 10.231.31.1 dev eth1
10.2.0.0/24 via 10.231.31.1 dev eth1
10.231.0.0/16 via 10.231.31.1 dev eth1
10.231.31.0/24 dev eth1 scope link  src 10.231.31.10
192.168.121.0/24 dev eth0 scope link  src 192.168.121.102
```
