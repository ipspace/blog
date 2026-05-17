---
title: "Dual-Stack SR-MPLS"
date: 2026-05-21 08:16:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
After the [introduction to SR-MPLS demo](/2026/05/sr-mpls-intro/) I did during the [Segment Routing workshop](/2026/04/sr-mpls-workshop/) @ ITNOG10, we moved to dual-stack SR-MPLS -- can we assign node segment identifiers (SIDs) to IPv4 *and* IPv6 prefixes? The demo used the same three-router network as the previous one, with IPv4 SIDs starting at one and IPv6 SIDs starting at 101:

{{<figure src="/2026/05/sr-mpls-intro.png">}}
<!--more-->
### Lab Topology {#lab}

I had to make a single change to the [previous lab topology](/2026/05/sr-mpls-intro/#lab) -- I had to define the IPv6 component of the address pools[^v4o]. I also used that opportunity to showcase[^sc] a few addressing options:

[^v4o]: The _netlab_ package defaults result in an IPv4-only network, but if you're an IPv6 fan, it's really easy to [change](https://netlab.tools/addressing/) that with [user- or system defaults](https://netlab.tools/defaults/).

[^sc]: Vendor-speak for *look how awesome our product is*

{{<printout>}}
addressing:
  loopback:
    ipv4: 10.0.42.0/24
    ipv6: 2001:db8::/48
    prefix6: 128
  core:
    ipv4: 192.168.42.0/24
    prefix: 31
    ipv6: 2001:db8:cafe::/48
{{</printout>}}

**Notes:**

* By default, _netlab_ assigns /32 IPv4 prefixes to loopback interfaces.
* If you want to have IPv6 loopback prefixes, you have to specify the **addressing.loopback.ipv6** parameter.
* I believed too much in the "/64 everywhere" gospel, so _netlab_ assigns /64 IPv6 prefixes to loopbacks. You can change that with the **addressing.loopback.prefix6** parameter, and you MUST change it to /128 if you want SR-MPLS to work on Arista EOS.
* Based on the above lab topology, the loopback interfaces in our lab will get IPv4 /32 prefixes from the 10.0.42.0/24[^b42] address space (starting with subnet one, not zero) and IPv6 /128 prefixes from the 2001:db8::/48 address space
* The *core* links (we'll get to what that pool is in a bit) will use /31 IPv4 prefixes from the 192.168.42.0/24 space, and /64 IPv4 prefixes from the 2001:db8:cafe::/48[^lxc] space.

[^b42]: Because 42 is the [ultimate answer](https://www.youtube.com/watch?v=aboZctrHfK8)

[^lxc]: I love having fun with hex characters ;)

On the topic of *showcasing*[^sbso], the topology uses a *[link group](https://blog.ipspace.net/2023/05/netlab-link-groups/)* using a *[custom address pool](https://netlab.tools/links/#links-custom-pools)*:

[^sbso]: Sounds so much better than *showing off*, right?

{{<printout>}}
links:
- group: core
  pool: core
  members: [ pe1-p, p-pe2 ]
{{</printout>}}

The [complete lab topology](https://github.com/ipspace/SR-workshop/blob/main/1-intro/3-ds/topology.yml) is in the [SR-MPLS workshop GitHub repository](https://github.com/ipspace/SR-workshop), and here's the addressing _netlab_ generated based on our pool/link definitions:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **pe1** |  10.0.42.1/32 | 2001:db8::1/128 | Loopback |
| Ethernet1 | 192.168.42.1/31 | 2001:db8:cafe::2/64 | pe1 -> p |
| **p** |  10.0.42.2/32 | 2001:db8::2/128 | Loopback |
| Ethernet1 | 192.168.42.0/31 | 2001:db8:cafe::1/64 | p -> pe1 |
| Ethernet2 | 192.168.42.2/31 | 2001:db8:cafe:1::1/64 | p -> pe2 |
| **pe2** |  10.0.42.3/32 | 2001:db8::3/128 | Loopback |
| Ethernet1 | 192.168.42.3/31 | 2001:db8:cafe:1::2/64 | pe2 -> p |
{.fmtTable}

### Exploring the SR-MPLS Setup

After [setting up _netlab_](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md), changing into the `1-intro/3-ds` directory, and executing **netlab up**, you'll have a working dual-stack SR-MPLS network and can start exploring.[^DS]

[^DS]: Here's the [script](https://github.com/ipspace/SR-workshop/blob/main/autopilot/3-ds.yml) I used during the demo

For example, do we get SR-MPLS TLVs advertised in IS-IS LSPs?

{{<printout highlight="yes" caption="PE1 IS-IS LSP displayed on Arista EOS">}}
pe2#<b>show isis database detail pe1.00-00</b>
Legend:
H - hostname conflict
U - node unreachable

IS-IS Instance: Gandalf VRF: default
  IS-IS Level 2 Link State Database
    LSPID                   Seq Num  Cksum  Life Length IS  Received LSPID        Flags
    pe1.00-00                     3  35182  1123    261 L2  0000.0000.0001.00-00  <>
      LSP received time: 2026-05-17 08:50:21
      Remaining lifetime received: 1199 s Modified to: 1200 s
      NLPID: 0xCC(IPv4) 0x8E(IPv6)
      Hostname: pe1
      Area addresses: 49.0042
      Topology: 2 (IPv6)
      Topology: 0 (IPv4)
      Interface address: 192.168.42.1
      Interface address: 10.0.42.1
      Interface address: 2001:db8:cafe::2
      Interface address: 2001:db8::1
      IS Neighbor          : p.00                Metric: 10
        IPv4 Neighbor Address: 192.168.42.0
        IPv4 Interface Address: 192.168.42.1
        Adj-sid: 100000 flags: [L V] weight: 0x0
      IS Neighbor (MT-IPv6): p.00                Metric: 10
        Adj-sid: 100001 flags: [L V F] weight: 0x0
      Reachability         : 192.168.42.0/31 Metric: 10 Type: 1 Up
      <b>Reachability         : 10.0.42.1/32 Metric: 10 Type: 1 Up</b>
      <b>  SR Prefix-SID: 1 Flags: [N] Algorithm: 0</b>
      Reachability (MT-IPv6): 2001:db8:cafe::/64 Metric: 10 Type: 1 Up
      <b>Reachability (MT-IPv6): 2001:db8::1/128 Metric: 10 Type: 1 Up</b>
      <b>  SR Prefix-SID: 101 Flags: [N] Algorithm: 0</b>
      Router Capabilities: Router Id: 10.0.42.1 Flags: []
        SR Local Block:
          SRLB Base: 965536 Range: 65536
        Area leader priority: 250 algorithm: 0
        Maximum SID depth:
          Base MPLS imposition (MSD type 1):  6
        SR Capability: Flags: [I V]
          SRGB Base: 900000 Range: 65536
{{</printout>}}

The IS-IS TLV is picture-perfect:

* It contains Segment Routing capabilities and the SR local block in Router Capabilities TLV
* It also contains Extended IP Reachability and multi-topology Extended IPv6 Reachability TLVs, each of them with a SR Prefix-SID sub-TLV.

The IPv6 SIDs are in the IS-IS segment routing prefix table:

{{<printout caption="IS-IS SR-MPLS prefix table on PE2 running Arista EOS" highlight="yes">}}
pe2#<b>show isis segment-routing prefix-segments</b>

System ID: pe2                  Instance: 'Gandalf'
SR supported Data-plane: MPLS                   SR Router ID: 10.0.42.3

Node: 6      Proxy-Node: 0      Prefix: 0       Total Segments: 6

Flag Descriptions: R: Re-advertised, N: Node Segment, P: no-PHP
                   E: Explicit-NULL, V: Value, L: Local, A: Proxy-Node attached
Segment status codes: * - Self originated Prefix, L1 - level 1, L2 - level 2, ! - SR-unreachable,
                      # - Some IS-IS next-hops are SR-unreachable
   Prefix                      SID   Label Type       Flags                        System ID       Level Protection           Algorithm
   ------------------------- ----- ------- ---------- ---------------------------- --------------- ----- -------------------- -------------
   10.0.42.1/32                  1  900001 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe1             L2    unprotected          SPF
   10.0.42.2/32                  2  900002 Node       R:0 N:1 P:0 E:0 V:0 L:0      p               L2    unprotected          SPF
*  10.0.42.3/32                  3  900003 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe2             L2    unprotected          SPF
   2001:db8::1/128             101  900101 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe1             L2    unprotected          SPF
   2001:db8::2/128             102  900102 Node       R:0 N:1 P:0 E:0 V:0 L:0      p               L2    unprotected          SPF
*  2001:db8::3/128             103  900103 Node       R:0 N:1 P:0 E:0 V:0 L:0      pe2             L2    unprotected          SPF
{{</printout>}}

Not surprisingly, the MPLS forwarding table contains entries for IPv4 and IPv6 SIDs:

{{<printout caption="MPLS forwarding table on PE2 running Arista EOS" highlight="yes">}}
pe2#<b>show mpls route</b>
...
 900001  A[1]
                via M, 192.168.42.2, swap 900001
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:02, vlan 1006
 900002  A[1]
                via M, 192.168.42.2, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:02, vlan 1006
 900101  A[1]
                via M, fe80::c8f0:ff:fe02:2, swap 900101
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:02, vlan 1006
 900102  A[1]
                via M, fe80::c8f0:ff:fe02:2, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    ca:f0:00:02:00:02, vlan 1006
{{</printout>}}

The previous blog post goes into more detail, and [explains](/2026/05/sr-mpls-intro/#results) why we see MPLS labels for SIDs advertised by PE1 and P, but not by PE2, in the PE2 MPLS table.

### The Dirty Details

Most [devices I could test with _netlab_](https://netlab.tools/module/sr-mpls/) implement dual-stack SR-MPLS[^SRL] except for Cisco IOS XE, which cannot assign SIDs to IPv6 prefixes[^lvig]. 

[^SRL]: Getting dual-stack SR-MPLS on SR Linux to work with FRRouting was quite a journey (details in a follow-up blog post if I remember that I have to write it ;). The results will be shipped in the _netlab_ release 26.06 (or whichever release comes after 26.05) because I started digging into this can of worms a few hours after shipping the 26.05 release 🤷🏻‍♂️.

[^lvig]: At least in the most recent version I got, but then I'm not surprised considering super-aggressive push into SRv6 by some of Cisco's Fellows.

However, while FRRouting, Junos, and Nokia SR Linux assign IPv6 node SID to whatever IPv6 prefix you configure on the loopback interface, Arista EOS and Cisco IOS XR advertise the loopback prefix with the SR-MPLS SID sub-TLV *only when the loopback IPv6 prefix is a /128*. Nokia SR-OS rejects a loopback IPv6 prefix that is not a /128 anyway.

If you were duped by the "use /64 everywhere argument", you'll waste countless hours trying to troubleshoot the behavior (like I did). Making it worse, neither of these two generates any obvious error messages, and Cisco IOS XR makes it even more confusing because it assigns the SID (and MPLS label) to the /64 IPv6 loopback but does not advertise it in IS-IS:

{{<printout caption="IS-IS SR-MPLS label table on PE1 (running IOS XR) with a /64 loopback IPv6 prefix" highlight="yes">}}
RP/0/RP0/CPU0:pe1#show isis segment-routing label table
Sat May 16 17:13:32.616 UTC

IS-IS Gandalf IS Label Table
Label         Prefix                   Algorithm    Interface
----------    ----------------         ---------    ---------
16001         10.0.42.1/32             SPF          Loopback0
16002         10.0.42.2/32             SPF
16003         10.0.42.3/32             SPF
<b>16101         2001:db8:0:1::1/64       SPF          Loopback0</b>
16102         2001:db8:0:2::/64        SPF
16103         2001:db8:0:3::/64        SPF
{{</printout>}}

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `1-intro/2-ds`
* Execute **netlab up**
* Have fun
