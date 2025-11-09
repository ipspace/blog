---
title: "netlab: Test IPv6 IGP Deployment"
series_title: "Test IPv6 IGP Deployment"
date: 2025-11-10 07:45:00+0100
tags: [ netlab ]
netlab_tag: use
---
Imagine you have an IPv4-only network[^EL] and want to try out how to deploy a routing protocol for IPv6. _netlab_ is a pretty good tool for the job as it:

* Creates an addressing scheme for you
* Designs a routing protocol deployment ([OSPF](https://netlab.tools/module/ospf/), [IS-IS](https://netlab.tools/module/isis/)) based on just a few bits of information
* Deploys ready-to-run router configurations to a virtual lab.

[^EL]: Not exactly a rare sight on planet Enterprise, even though IPv6 is almost exactly 30 years old.
<!--more-->
If you're focused on testing a routing protocol deployment, you wouldn't want to waste time configuring IPv6 addressing, so you should adjust the addressing pools to include IPv6 prefixes:

```
addressing:
  loopback.ipv6: 2001:db8:cafe::/48    # Routers are always debating stuff
  p2p.ipv6: True                       # Use LLA-only P2P links
  lan.ipv6: 3fff:1::/48                # Hey, we got RFC 9637
```

However, when you deploy OSPF (for example) in your network, _netlab_ tries to be extra helpful and configures both OSPFv2 and OSPFv3.

Let's use this simple topology with the above addressing pools:

```
defaults.device: eos
provider: clab
module: [ ospf ]

nodes: [ r1, r2 ]
links: [ r1, r1-r2, r2 ]
```

{{<figure src="/2025/11/ospf-topo.png" caption="Lab topology">}}

After starting the lab, R1 gets the following OSPF-related configuration:

{{<cc>}}OSPF-related configuration _netlab_ deployed on R1 running Arista EOS{{</cc>}}
```
interface Ethernet1
   description r1 -> stub [stub]
   ip address 172.16.0.1/24
   ipv6 address 3fff:1::1/64
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
   ipv6 ospf network point-to-point
   ipv6 ospf 1 area 0.0.0.0
!
interface Ethernet2
   description r1 -> r2
   ip address 10.1.0.1/30
   ipv6 enable
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
   ipv6 ospf network point-to-point
   ipv6 ospf 1 area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.1/32
   ipv6 address 2001:db8:cafe:1::1/64
   ip ospf area 0.0.0.0
   ipv6 ospf 1 area 0.0.0.0
!
router ospf 1
   router-id 10.0.0.1
   interface unnumbered hello mask tx 0.0.0.0
   passive-interface Ethernet1
   max-lsa 12000
   timers spf delay initial 100 200 500
   timers lsa rx min interval 100
   timers lsa tx delay initial 100 200 500
!
ipv6 router ospf 1
   router-id 10.0.0.1
   passive-interface Ethernet1
   timers spf delay initial 100 200 500
   timers lsa rx min interval 100
   timers lsa tx delay initial 100 200 500
```

Not exactly what we wanted -- we'd love to have OSPFv2 configured, but not OSPFv3.

Other _netlab_ users tried to solve a similar problem in the past, so we added [support for configurable IGP address families](https://netlab.tools/module/routing_protocols/#routing-af) a while ago. All we have to do to deploy OSPFv2, but not OSPFv3, is a single global parameter:

```
ospf.af: [ ipv4 ]
```

Here's the OSPF-related configuration deployed to R1 after we limited OSPF deployment to IPv4:

```
interface Ethernet1
   description r1 -> stub [stub]
   ip address 172.16.0.1/24
   ipv6 address 3fff:1::1/64
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2
   description r1 -> r2
   ip address 10.1.0.1/30
   ipv6 enable
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.1/32
   ipv6 address 2001:db8:cafe:1::1/64
   ip ospf area 0.0.0.0
!
router ospf 1
   router-id 10.0.0.1
   interface unnumbered hello mask tx 0.0.0.0
   passive-interface Ethernet1
   max-lsa 12000
   timers spf delay initial 100 200 500
   timers lsa rx min interval 100
   timers lsa tx delay initial 100 200 500
```

_netlab_ configured IPv4 and IPv6 addresses, but not OSPFv3. Mission Accomplished.

### Kicking the Tires

You can try out this example in your own _netlab_ environment ([installation guide](https://netlab.tools/install/) or in free [GitHub Codespaces](/2024/07/netlab-examples-codespaces/).

If you set up your own netlab environment, execute `netlab up https://github.com/ipspace/netlab-examples/blob/master/OSPF/ipv4-only/topology.yml` in an empty directory. If you didn't install Arista cEOS containers, add `-d frr` to the command.

In a GitHub Codespace:

* Install [Arista cEOS container image](https://blog.ipspace.net/2024/07/arista-eos-codespaces/)
* Change directory to `OSPF/ipv4-only`
* Execute **netlab up**, or **netlab up -d frr** to use FRRouting if you didn't install the Arista cEOS container image.
