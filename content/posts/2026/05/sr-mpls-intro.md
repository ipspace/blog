---
title: "Hands-On Introduction to SR-MPLS"
date: 2026-05-13 08:16:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
The [second demo](https://github.com/ipspace/SR-workshop/tree/main/1-intro/2-netlab)[^FD] I did during the [Segment Routing workshop](/2026/04/sr-mpls-workshop/) @ ITNOG10 illustrated how easy it is to set up and explore a small SR-MPLS network with _netlab_. The lab topology described a small three-router network (you need three routers to see "true" labels besides the [penultimate-hop popping](/2011/07/penultimate-hop-popping-php-demystified/) ones):

{{<figure src="/2026/05/sr-mpls-intro.png">}}
<!--more-->
[^FD]: The first demo showed the difference between _containerlab_ and _netlab_. More about that in another blog post.

### Lab Topology {#lab}

As part of the presentation, I also wanted to explain how to build [_netlab_](https://netlab.tools/) [topology files](https://netlab.tools/topology-overview/) from zero to pretty complex scenarios. Reality (= lack of time) intervened, so let's fix it. Here's the [topology file](https://github.com/ipspace/SR-workshop/blob/main/1-intro/2-netlab/topology.yml) I used:

{{<printout>}}
provider: clab
defaults.device: eos
module: [ isis, sr ]

nodes: [ pe1, p, pe2 ]
links: [ pe1-p, p-pe2 ]
{{</printout>}}

It would be hard to make it any easier; here's what it means:

* The lab is using containers (line 1)
* The routers are running Arista EOS[^WAE] (line 2)
* All nodes run [IS-IS](https://netlab.tools/module/isis/) and [SR-MPLS](https://netlab.tools/module/sr-mpls/) (line 3)
* There are three [nodes](https://netlab.tools/nodes/) in the lab topology (line 5)
* The nodes are connected with [two links](https://netlab.tools/links/) (line 6), specified using the simplified [link description format](https://netlab.tools/example/link-definition/).

[^WAE]: For a very good reason: I can run the labs on an x86 server, in a GitHub Codespaces container, or on a MacBook Pro (on an ARM CPU). The only other device with comparable flexibility is SR Linux, but it requires a license to run SR-MPLS. Unfortunately, you cannot run MPLS on FRRouting containers in GitHub Codespaces because you cannot load the Linux drivers that the containers expect to use.

### Exploring the SR-MPLS Setup {#results}

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first.

Approximately a minute after executing **netlab up** (depending on your CPU speed), you'll have a working SR-MPLS network and can start exploring[^DS]

[^DS]: Here's the [script](https://github.com/ipspace/SR-workshop/blob/main/autopilot/2-netlab.yml) I used during the demo

For example, do we get SR-MPLS TLVs advertised in IS-IS LSPs?

{{<cc>}}PE1 IS-IS LSP displayed on Arista EOS{{</cc>}}
```
pe1#show isis database pe1.00-00 detail
IS-IS Instance: Gandalf VRF: default
  IS-IS Level 2 Link State Database
    LSPID                   Seq Num  Cksum  Life Length IS  Received LSPID        Flags
    pe1.00-00                     3  40705   924    149 L2  0000.0000.0001.00-00  <>
      LSP generation remaining wait time: 0 ms
      Time remaining until refresh: 624 s
      NLPID: 0xCC(IPv4)
      Hostname: pe1
      Area addresses: 49.0001
      Interface address: 10.1.0.2
      Interface address: 10.0.0.1
      IS Neighbor          : p.00                Metric: 10
        IPv4 Neighbor Address: 10.1.0.1
        IPv4 Interface Address: 10.1.0.2
        Adj-sid: 100000 flags: [L V] weight: 0x0
      Reachability         : 10.1.0.0/30 Metric: 10 Type: 1 Up
      Reachability         : 10.0.0.1/32 Metric: 10 Type: 1 Up
        SR Prefix-SID: 1 Flags: [N] Algorithm: 0
      Router Capabilities: Router Id: 10.0.0.1 Flags: []
        SR Local Block:
          SRLB Base: 965536 Range: 65536
        Area leader priority: 250 algorithm: 0
        Maximum SID depth:
          Base MPLS imposition (MSD type 1):  6
        SR Capability: Flags: [I]
          SRGB Base: 900000 Range: 65536
```

Looks good:

* The local router is advertising its Segment Routing capabilities and the SR local block in Router Capabilities TLV
* It also advertises SR Prefix-SID as a sub-TLV of IPv4 reachability TLV

What about the state of IS-IS segment routing on PE1?

```
pe1#show isis segment-routing
System ID: pe1			Instance: Gandalf
SR supported Data-plane: MPLS			SR Router ID: 10.0.0.1
SR Global Block( SRGB ):
Base            Size
900000          65536           
Total SRGB Size: 65536           

Adj-SID allocation mode: SR-adjacencies
Adj-SID allocation pool: Base: 100000     Size: 16384

All Prefix Segments have    : P:0 E:0 V:0 L:0
IS-IS Reachability Algorithm : SPF (0)
Proxy-node segment attached flag: ignored

Number of IS-IS segment routing capable nodes excluding self: 2

Self-Originated Segment Statistics:
Node-Segments       : 1
Prefix-Segments     : 0
Proxy-Node-Segments : 0
Adjacency Segments  : 1
```

As expected. Segment routing is enabled in IS-IS, and IS-IS advertises the SR-MPLS data plane.

Let's look at the prefix segments advertised by SR-MPLS routers:

```
pe1#show isis segment-routing prefix-segments
System ID: pe1			Instance: 'Gandalf'
SR supported Data-plane: MPLS			SR Router ID: 10.0.0.1

Node: 3      Proxy-Node: 0      Prefix: 0       Total Segments: 3

Flag Descriptions: R: Re-advertised, N: Node Segment, P: no-PHP
                   E: Explicit-NULL, V: Value, L: Local, A: Proxy-Node attached
Segment status codes: * - Self originated Prefix, L1 - level 1, L2 - level 2, ! - SR-unreachable,
                      # - Some IS-IS next-hops are SR-unreachable
   Prefix                      SID   Label Type       Flags                        System ID       Level Protection           Algorithm   
   ------------------------- ----- ------- ---------- ---------------------------- --------------- ----- -------------------- -------------
*  10.0.0.1/32                   1  900001 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe1             L2    unprotected          SPF         
   10.0.0.2/32                   2  900002 Node       R:0 N:1 P:0 E:0 V:0 L:0      p               L2    unprotected          SPF         
   10.0.0.3/32                   3  900003 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe2             L2    unprotected          SPF         
```

Each router advertises a single global SID for its loopback prefix.

Based on that information, we should see a few entries in the MPLS forwarding table (LFIB) on PE1:

```
pe1#show mpls route
MPLS forwarding table (Label [metric] Vias) - 3 routes 
MPLS next-hop resolution allow default route: False
Metric Codes:
          A - Active metric
Via Type Codes:
          M - MPLS via, LP - LDP pseudowire via,
          I - IP lookup via, V - VLAN via,
          VA - EVPN VLAN aware via, ES - EVPN ethernet segment via,
          VF - EVPN VLAN flood via, AF - EVPN VLAN aware flood via,
          NG - Nexthop group via, BP - BGP pseudowire via,
          VP - VPWS pseudowire via, MSP - Static pseudowire via,
          EL - EVPN E-Tree Leaf Label via

 100000  A[1]
                via M, 10.1.0.1, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
 900002  A[1]
                via M, 10.1.0.1, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
 900003  A[1]
                via M, 10.1.0.1, swap 900003
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
```

Two entries in the LFIB are derived from the global SIDs of other routers[^NNL]. The label for the SID advertised by the P router is mapped to the "pop" action (penultimate-hop popping), while the label for the PE2 SID maps to the same label -- an expected result when all nodes in an SR-MPLS network use the same SR Global Block (SRGB), 

[^NNL]: There is no need for an entry for the router's own global SIDs, as the network uses penultimate-hop popping.

### Try It Out

Why don't you:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it[^EIGH] ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `1-intro/2-netlab`
* Execute **netlab up**
* Have fun

[^EIGH]: If only there was an easier way to do it... Nokia mastered it with SR-Linux; Arista is still dragging its feet.
