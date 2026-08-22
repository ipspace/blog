---
title: "Multivendor SR-MPLS"
date: 2026-08-25 07:44:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
Summer is almost over, and it's time to resume regular programming with the next example from the [Segment Routing workshop](/2026/04/sr-mpls-workshop/) I had at ITNOG10: [multi-vendor SR-MPLS](https://github.com/ipspace/SR-workshop/tree/main/1-intro/6-multivendor). I used the same lab topology as in the [previous examples](/tag/sr-mpls/#try) but deployed Arista EOS on PE1, FRRouting on P, and SR Linux on PE2[^NL] 

{{<figure src="/2026/05/sr-mpls-intro.png">}}
<!--more-->
[^NL]: SR Linux needs a license file to run MPLS-related protocols like SR-MPLS.

### Lab Topology {#lab}

I had to change two details in the [initial lab topology](/2026/05/sr-mpls-intro/#lab):

* The definition of **nodes**: I had to tell _netlab_ which device type to use for each node.
* I also had to specify the default license file and device model (type) for the SR Linux node.

The full lab topology file is [here](https://github.com/ipspace/SR-workshop/blob/main/1-intro/6-multivendor/topology.yml). 

{{<printout caption="Multivendor changes to the original IS-IS lab topology">}}
defaults.devices.srlinux.clab.node:
  license: ~/.netlab/license_srlinux.txt
  type: ixr6

nodes:
  pe1:
    device: eos
  p:
    device: frr
  pe2:
    device: srlinux
{{</printout>}}

### Exploring Multi-Vendor SR-MPLS

After [setting up _netlab_](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md), changing into the `1-intro/6-multivendor` directory, and executing **netlab up**, you'll have an SR-MPLS network across three vendors. You can do the same checks we did for the [original IS-IS lab](/2026/05/sr-mpls-intro/) and should get (mostly) the same results.

The only significant difference is the Segment Routing Global Block (SRGB) advertised by the three devices. The lab topology does not specify the SRGB values; each device is thus using vendor[^NLD] defaults:

[^NLD]: Or _netlab_ in case of SR Linux

{{<printout highlight="yes" caption="Default Segment Routing Global Blocks observed on PE1 running on Arista EOS">}}
pe1#<b>show isis segment-routing global-blocks</b>

c - conflicting SR capability TLV, processed first advertisement
System ID: pe1                  Instance: Gandalf
SR supported Data-plane: MPLS                   SR Router ID: 10.0.0.1
SR Global Block( SRGB ) Size: 65536

Number of IS-IS segment routing capable nodes excluding self: 2

           SystemId         Base     Size
------- -------------- ------------ -----
   *            pe1       900000    65536
                  p        24000     8000
                pe2        16000    10000
{{</printout>}}

Likewise, the prefix segments (displayed as SID + SRGB start) reflect different SRGB ranges:

{{<printout highlight="yes" caption="SR-MPLS prefix segments observed on PE1 running Arista EOS">}}
pe1#<b>show isis segment-routing prefix-segments</b>

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
   10.0.0.2/32                   2   24002 Node       R:0 N:1 P:0 E:0 V:0 L:0      p               L2    unprotected          SPF
   10.0.0.3/32                   3   16003 Node       R:0 N:1 P:1 E:0 V:0 L:0      pe2             L2    unprotected          SPF
{{</printout>}}

{{<note warn>}}
Using default SRGB values in a multi-vendor network is a perfect recipe for confusion. Configure the same SRGB values on all devices in your network. Admittedly, that might be a bit of a juggling act considering the widely different default ranges.
{{</note>}}

As expected, the [device-specific SRGB ranges](/2021/05/segment-routing-ids-mpls-labels/) are reflected in the MPLS LFIB. For example, PE1 (Arista EOS) expects to receive label 900003 to forward traffic to 10.0.0.3/32 (SID 3 advertised by PE2), while P (FRRouting) expects label 24003. The MPLS LFIB entry for 900003 on Arista EOS thus swaps the label with 24003:

{{<printout caption="MPLS LFIB entry for PE2 loopback displayed on PE1 running Arista EOS" highlight="yes">}}
pe1#<b>show mpls lfib route 900003 | begin 900003</b>
 IP    900003   [1], 10.0.0.3/32
                via M, 10.1.0.1, swap 24003
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet1
{{</printout>}}

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Import the SR Linux license file into the GitHub Codespace
* Change directory to `1-intro/6-multivendor`
* Edit the location of the SR Linux license file in `topology.yml`
* Execute **netlab up**
* Have fun
