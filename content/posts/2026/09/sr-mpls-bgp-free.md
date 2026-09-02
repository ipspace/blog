---
title: "BGP-Free Core with SR-MPLS"
date: 2026-09-03 07:30:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
The beauty of SR-MPLS is that it's a drop-in replacement for the traditional (LDP- or RSVP-based) MPLS control plane. For example, you could replace LDP with [SR-MPLS](/2021/05/segment-routing-mpls-bgp-free-core/) in a network using MPLS to implement a [BGP-free transport core](/2012/01/bgp-free-service-provider-core-in/), and it just keeps working.

This scenario was the first "fun" scenario in the ITNOG10 [Segment Routing workshop](/2026/04/sr-mpls-workshop/). The core network uses the same topology as in the [previous examples](/tag/sr-mpls/#try); I added two hosts and BGP routing.

{{<figure src="/2026/09/sr-mpls-fun.png" caption="Simplest possible network using a BGP-free core">}}
<!--more-->

### Lab Topology {#lab}

I had to make significant changes to the [lab topology](https://github.com/ipspace/SR-workshop/blob/main/2-fun/1-bgp-free/topology.yml) to keep it structured.

I used **[groups](https://netlab.tools/groups/)** to apply the same set of attributes to similar nodes (hosts, PE routers, the core router). The `_auto_create` flag tells *netlab* to create the group members without them being listed in the **nodes** dictionary.

{{<printout caption="Using groups to define lab nodes">}}
groups:
  _auto_create: True
  core:
    members: [ p1 ]
    module: [ isis, sr ]
  edge:
    members: [ pe1, pe2 ]
    module: [ isis, bgp, sr ]
  hosts:
    members: [ ha, hb ]
    device: linux
{{</printout>}}

* The **core** router (P1) runs IS-IS and SR-MPLS
* The **edge** routers (PE1, PE1) run IS-IS, BGP, and SR-MPLS
* The **hosts** are Linux containers

Similarly, I used *[link groups](https://blog.ipspace.net/2023/05/netlab-link-groups/)* to apply consistent attributes to multiple links:

{{<printout caption="Using link groups">}}
- group: core
  members: [ pe1-p1, p1-pe2 ]
- group: edge
  isis: False
  bgp.advertise: True
  members: [ ha-pe1, hb-pe2 ]
{{</printout>}}

* _netlab_ automatically enables IS-IS on links between routers in the same BGP AS.
* It would also enable IS-IS on the edge (host-to-PE) links, so we have to disable IS-IS on those links (we want them advertised only in BGP).
* The edge links have to be advertised in BGP, so we're using the **bgp.advertise** flag to ensure they will be.

Finally, we have to specify the BGP AS we want to use with the **bgp.as** topology attribute. The full lab topology file is [here](https://github.com/ipspace/SR-workshop/blob/main/2-fun/1-bgp-free/topology.yml). 

### Exploring BGP-Free Core

After [setting up _netlab_](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md), changing into the `2-fun/1-bgp-free` directory, and executing **netlab up**, you'll have BGP running across an SR-MPLS network. You can do the same checks we did for the [original IS-IS lab](/2026/05/sr-mpls-intro/) and should get the same results. The fun starts when we look at the BGP routing table entries. These entries should have an MPLS label derived from SR-MPLS:

{{<printout highlight="yes" caption="BGP route with an SR-MPLS label observed on PE1 running on Arista EOS">}}
pe1#show ip route bgp | begin 172.16
 B I      172.16.1.0/24 [200/0]
           via 10.0.0.3/32, IS-IS SR tunnel index 1
              via 10.1.0.1, Ethernet1, <b>label 900003</b>
{{</printout>}}

Not surprisingly, once the PE routers have MPLS labels attached to the BGP routes, we get end-to-end connectivity even though the P router does not have the BGP routes in its routing table:

{{<printout highlight="yes" caption="End-to-end connectivity between hosts">}}
$ netlab connect ha
Connecting to container clab-bgpfree-ha, starting bash
ha:/# ping -c 3 hb
PING hb (172.16.1.5): 56 data bytes
64 bytes from 172.16.1.5: seq=0 ttl=61 time=2.872 ms
64 bytes from 172.16.1.5: seq=1 ttl=61 time=2.480 ms
64 bytes from 172.16.1.5: seq=2 ttl=61 time=2.777 ms

--- hb ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.480/2.709/2.872 ms
{{</printout>}}

{{<printout highlight="yes" caption="The routing table on P router running Arista EOS">}}
p1#show ip route | begin Gateway
Gateway of last resort is not set

 C        10.0.0.1/32
           directly connected, Loopback0
 I L2     10.0.0.2/32 [115/20]
           via 10.1.0.2, Ethernet1
 I L2     10.0.0.3/32 [115/20]
           via 10.1.0.6, Ethernet2
 C        10.1.0.0/30
           directly connected, Ethernet1
 C        10.1.0.4/30
           directly connected, Ethernet2
{{</printout>}}

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `2-fun/1-bgp-free`
* Execute **netlab up**
* Have fun
