---
title: "SR-MPLS over Unnumbered Interfaces"
date: 2026-06-01 08:03:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
After the [simple SR-MPLS demo](/2026/05/sr-mpls-intro/) and the [dual-stack SR-MPLS setup](/2026/05/sr-mpls-dual-stack/), it was time for the next obvious question: Does SR-MPLS work over unnumbered IPv4 interfaces[^Uv6], assuming the implementation of the underlying routing protocol supports them? Of course it does; let's go through the details, using the same topology I used throughout the [Segment Routing workshop](/2026/04/sr-mpls-workshop/) @ ITNOG10.

{{<figure src="/2026/05/sr-mpls-intro.png">}}
<!--more-->
[^Uv6]: Unnumbered IPv6 interfaces (more precisely, IPv6 interfaces using only link-local IPv6 addresses) are boring; most IGP routing protocols use them as next hops anyway.

### Lab Topology {#lab}

The unnumbered IPv4 setup required a single change to the  [initial lab topology](/2026/05/sr-mpls-intro/#lab) -- I had to tell _netlab_ to use unnumbered IPv4 on point-to-point links (the full lab topology file is [here](https://github.com/ipspace/SR-workshop/blob/main/1-intro/4-unnumbered/topology.yml)):

{{<printout>}}
addressing.p2p.ipv4: True
{{</printout>}}

### Exploring the SR-MPLS Setup

After [setting up _netlab_](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md), changing into the `1-intro/4-unnumbered` directory, and executing **netlab up**, you'll have an SR-MPLS network using unnumbered IPv4 P2P interfaces. Let's do the usual checks:

Do we get SR-MPLS TLVs advertised in IS-IS LSPs?

{{<printout highlight="yes" caption="PE1 IS-IS LSP displayed on Arista EOS">}}
pe2#<b>show isis database detail pe1.00-00</b>
Legend:
H - hostname conflict
U - node unreachable

IS-IS Instance: Gandalf VRF: default
  IS-IS Level 2 Link State Database
    LSPID                   Seq Num  Cksum  Life Length IS  Received LSPID        Flags
    pe1.00-00                     3  58379  1185    136 L2  0000.0000.0001.00-00  <>
      LSP generation remaining wait time: 0 ms
      Time remaining until refresh: 885 s
      NLPID: 0xCC(IPv4)
      Hostname: pe1
      Area addresses: 49.0001
      Interface address: 10.0.0.1
      IS Neighbor          : p.00                Metric: 10
        IPv4 Neighbor Address: 10.0.0.2
        IPv4 Interface Address: 10.0.0.1
        Adj-sid: 100000 flags: [L V] weight: 0x0
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
{{</printout>}}

Compared to the previous examples (numbered IPv4, dual-stack), the IS-IS TLV is somewhat smaller; it has the IS Neighbor TLV, but not the Reachability TLVs for the P2P subnets (obviously). The adjacency SID is attached to the IS Neighbor TLV, so we can still use it for the segment-by-segment traffic engineering.

Because the loopback interfaces and associated SIDs are in the IS-IS TLVs, we should see the prefix segments of all nodes (and we do):

{{<printout caption="IS-IS SR-MPLS prefix table on PE2 running Arista EOS" highlight="yes">}}
pe2#<b>show isis segment-routing prefix-segments</b>
System ID: pe1                  Instance: 'Gandalf'
SR supported Data-plane: MPLS                   SR Router ID: 10.0.0.1

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
{{</printout>}}

Not surprisingly, the MPLS forwarding table is identical to the simple SR-MPLS example:

{{<printout caption="MPLS forwarding table on PE2 running Arista EOS" highlight="yes">}}
pe2#<b>show mpls route</b>
...
 100000  A[1]
                via M, 10.0.0.2, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
 900002  A[1]
                via M, 10.0.0.2, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
 900003  A[1]
                via M, 10.0.0.2, swap 900003
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:01, vlan 1006
{{</printout>}}

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `1-intro/4-unnumbered`
* Execute **netlab up**
* Have fun
