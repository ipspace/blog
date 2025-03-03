---
date: 2022-01-17 07:04:00+00:00
series:
- unnumbered-interfaces
tags:
- IS-IS
title: Running IS-IS over Unnumbered Ethernet Interfaces
short_summary: |
  OSPFv2 can run over unnumbered point-to-point links. Some IS-IS implementations are better than that and can run over unnumbered multi-access segments (for example, Carrier Ethernet E-LAN service).
---
Last time we figured out that we [cannot run OSPF over unnumbered interfaces](/2022/01/ospf-unnumbered/) that are not point-to-point links because OSPF makes assumptions about interface IP addresses. IS-IS makes no such assumptions; IPv4 and IPv6 prefixes are just a bunch of TLVs exchanged between routers over a [dedicated layer-3 protocol](/2009/06/is-is-is-not-running-over-clnp/) with ridiculously long network addresses. 

Could we thus build a totally unnumbered IP network with IS-IS even when the network contains multi-access segments? It depends:
<!--more-->
* It works like a charm on Arista EOS and Cisco IOS XE.
* Cisco NXOS [has a few quirks](#addendum-nxos-quirks).
* Junos vSRX works well with unnumbered IPv4 P2P links. IPv6 works like a charm (no surprise there due to link-local addresses).

We'll use the following lab topology to run our tests. All devices run the same network operating system. All physical interfaces are unnumbered -- the only IP addresses in the lab are assigned to loopback interfaces. P2P links have cost 10, the LAN link has cost 5.

{{<figure src="/2022/01/unnumbered-ospf-topology.png" caption="Lab topology">}}

Once I fixed the IS-IS network type (**point-to-point** network type should be used on P2P links but not on multi-access links), the adjacencies came up almost immediately (Gi3 is the multi-access interface):

```
r1#show isis neighbors

Tag Gandalf:
System Id       Type Interface     IP Address      State Holdtime Circuit Id
r2              L2   Gi2           10.0.0.2        UP    23       02
r2              L2   Gi3           10.0.0.2        UP    21       r3.01
r3              L2   Gi3           10.0.0.3        UP    8        r3.01
```

The IS-IS database has a pseudonode LSP (r3.01-00) confirming that one link in the topology works as a multi-access link:

```
r1#show isis database

Tag Gandalf:
IS-IS Level-2 Link State Database:
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
r1.00-00            * 0x00000006   0x1A38                1009/*         0/0/0
r2.00-00              0x00000006   0x8499                1006/1200      0/0/0
r3.00-00              0x00000006   0x4DF8                1006/1197      0/0/0
r3.01-00              0x00000002   0xDCDC                1007/1199      0/0/0
```

All three routers are connected to the pseudonode LSP:

```
r1#show isis database r3.01-00 detail

Tag Gandalf:

IS-IS Level-2 LSP r3.01-00
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
r3.01-00              0x00000002   0xDCDC                 987/1199      0/0/0
  Metric: 0          IS-Extended r3.00
  Metric: 0          IS-Extended r1.00
  Metric: 0          IS-Extended r2.00
```

Mission accomplished. We got our network up and running over unnumbered interfaces.

Not so fast. Does IP routing work? Let's inspect the IP routing table:

```
r1#show ip route | begin Gateway
Gateway of last resort is 192.168.121.1 to network 0.0.0.0

S*    0.0.0.0/0 [254/0] via 192.168.121.1
      10.0.0.0/32 is subnetted, 3 subnets
C        10.0.0.1 is directly connected, Loopback0
i L2     10.0.0.2 [115/15] via 10.0.0.2, 00:17:05, GigabitEthernet3
i L2     10.0.0.3 [115/15] via 10.0.0.3, 00:16:39, GigabitEthernet3
```

Looks good. Loopback interfaces of other routers are reachable over GigabitEthernet3... but the next hop is the loopback IP address itself, so we need some ARP glue ([more details](/2021/06/unnumbered-ethernet-interfaces/)). Do we have it?

```
r1#show arp 10.0.0.0 255.0.0.0
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.0.0.1                -   5254.00ff.e287  ARPA   GigabitEthernet2
Internet  10.0.0.1                -   5254.00d3.58b7  ARPA   GigabitEthernet3
Internet  10.0.0.2               20   5254.00b1.edb0  ARPA   GigabitEthernet2
Internet  10.0.0.2               18   5254.00d9.55ec  ARPA   GigabitEthernet3
Internet  10.0.0.3               18   5254.007d.f1e5  ARPA   GigabitEthernet3
```

All the expected ARP glue entries are there. The final test: pinging remote loopback.

```
r1#ping r3
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.3, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

OK, now we know it works 👍

Long story short: use IS-IS 😁

## Addendum: NXOS Quirks

Cisco NXOS is different. Not only does it need an incredible amount of time to boot, it doesn't like multi-access unnumbered IPv4 links... but you can still persuade it to use them (sort of).

{{<note>}}Before someone starts yelling at me that I'm writing about irrelevant details: I know that. Most data center links are point-to-point links. It's still interesting to see how different implementations behave though.{{</note>}}

Here's the full story:

* To use **ip unnumbered** on NXOS you have to configure **medium p2p**
* **medium p2p** seems to trigger point-to-point IS-IS links. With three NXOS switches connected to the same segment (R1, R2 and R3 are connected to Ethernet1/2) you get all the expected IS-IS adjacencies:

```
r1# show isis adjacency
IS-IS process: Gandalf VRF: default
IS-IS adjacency database:
Legend: '!': No AF level connectivity in given topology
System ID       SNPA            Level  State  Hold Time  Interface
r2              N/A             2      UP     00:00:31   Ethernet1/1
r2              N/A             2      UP     00:00:23   Ethernet1/2
r3              N/A             2      UP     00:00:23   Ethernet1/2
```

However, the IS-IS topology database does not contain the pseudonode LSP:

```
r1# show isis database
IS-IS Process: Gandalf LSP database VRF: default
IS-IS Level-1 Link State Database
  LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T

IS-IS Level-2 Link State Database
  LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T
  r1.00-00            * 0x00000009   0x1E07    967        0/0/0/3
  r2.00-00              0x00000009   0x72FD    1181       0/0/0/3
  r3.00-00              0x00000007   0xC0F9    1153       0/0/0/3
```

Also, the LSP generated by R1 contains P2P links to R2 and R3 instead of a link to the pseudonode LSP:

```
r1# show isis database detail r1.00-00
IS-IS Process: Gandalf LSP database VRF: default
IS-IS Level-1 Link State Database
  LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T

IS-IS Level-2 Link State Database
  LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T
  r1.00-00            * 0x00000009   0x1E07    921        0/0/0/3
    Instance      :  0x00000009
    Area Address  :  49.0001
    NLPID         :  0xCC 0x8E
    Router ID     :  10.0.0.1
    IP Address    :  10.0.0.1
    MT TopoId     : TopoId:2 Att: 0 Ol: 0
                    TopoId:0 Att: 0 Ol: 0
    Hostname      :  r1                 Length : 2
    TopoId: 2
    MtExtend IS   :  r3.00              Metric : 5
                     r2.00              Metric : 5
                     r2.00              Metric : 10
    Extended IS   :  r2.00              Metric : 5
    Extended IS   :  r3.00              Metric : 5
    Extended IS   :  r2.00              Metric : 10
    Extended IP   :        10.0.0.1/32  Metric : 1           (U)
    MT-IPv6 Prefx :  TopoId : 2
                    2001:db8:1:1::/64  Metric : 1           (U/I)
    Digest Offset :  0
```

While a network of Nexus switches works as expected, I wouldn't expect a multi-vendor segment to work as everyone else insists on a different view of the world.
