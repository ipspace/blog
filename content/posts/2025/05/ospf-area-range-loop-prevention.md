---
title: "OSPF Loop Prevention with Area Range Summary LSAs"
date: 2025-05-06 08:17:00+0200
tags: [ OSPF ]
ospf_tag: areas
---
In a [previous blog post](/2025/04/ospf-summary-lsa-loop-prevention/), I described how OSPF route selection rules prevent a summary LSA from being inserted back into an area from which it was generated. That works nicely for area prefixes turned directly into summary LSAs, but how does the loop prevention logic work for summarized prefixes (what OSPF calls *area ranges*)?

**TL&DR:** It doesn't, unless... ;)
<!--more-->
We'll use the same sample network we used in the previous blog post, and use the **area range** configuration command to add inter-area summarization of the 192.168.0.x/32 prefixes into 192.168.0.0/24.

{{<figure src="/2025/04/ospf-summary-lsa-topo.png">}}

Let's configure the area range on A1 and inspect the contents of the OSPF database of the backbone area on A2. You should see the summary prefix (192.168.0.0/24) originated by A1 and the individual prefixes (192.168.0.1/32 and 192.168.0.2/32) originated by A2. You might also notice revoked[^ORV] individual prefixes in the summarized range that were previously originated by A1 but are not yet removed from the OSPF database.

[^ORV]: Their age is set to 3600, and because of that, they are no longer considered by the SPF algorithm.

{{<note info>}}If you want to reproduce my results, [follow the instructions from the previous blog post to start a lab](/2025/04/ospf-summary-lsa-loop-prevention/#netlab), then use the `netlab config area_range --limit a1` command to configure inter-area summarization on A1.{{</note>}}

{{<cc>}}Summary LSAs in the backbone area on A2 (edited to remove router link states){{</cc>}}
```
a2# show ip ospf data
...
                Summary Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum  Route
10.0.0.5       10.0.0.3         222 0x80000001 0xae88 10.0.0.5/32
10.0.0.6       10.0.0.4         231 0x80000001 0x9e96 10.0.0.6/32
192.168.0.0    10.0.0.3          49 0x80000001 0x16bc 192.168.0.0/24
192.168.0.1    10.0.0.3        3600 0x80000001 0xa734 192.168.0.1/32
192.168.0.1    10.0.0.4         221 0x80000001 0x06ca 192.168.0.1/32
192.168.0.2    10.0.0.3        3600 0x80000001 0x02ce 192.168.0.2/32
192.168.0.2    10.0.0.4         221 0x80000001 0x9742 192.168.0.2/32
```

A2 knows nothing about the *area range* configured on A1 and happily inserts the 192.168.0.0/24 summary LSA back into area 1:

{{<cc>}}Summary LSAs in area 1 on S1 (edited to remove router link states){{</cc>}}
```
s1# show ip ospf database summary 192.168.0.0

       OSPF Router with ID (192.168.0.1)


                Summary Link States (Area 0.0.0.1)

  LS age: 71
  Options: 0x2  : *|-|-|-|-|-|E|-
  LS Flags: 0x6
  LS Type: summary-LSA
  Link State ID: 192.168.0.0 (summary Network Number)
  Advertising Router: 10.0.0.4
  LS Seq Number: 8000000c
  Checksum: 0x5e5e
  Length: 28

  Network Mask: /24
        TOS: 0  Metric: 30
```

Configuring **area range** on A2[^NLC] obviously solves this discrepancy. A1 and A2 generate the summary LSA for 192.168.0.0/24, and they do not reinsert it back into area 1. The loop prevention works, but why?

[^NLC]: Use the **netlab config area_range -l a2** command if you're running a _netlab_-powered lab with Arista EOS, Cisco IOS/IOS-XE/IOL, or FRRouting.

The answer is hidden deep within the bowels of [RFC 2328](https://datatracker.ietf.org/doc/html/rfc2328#page-168); bullet 3 in the section 16.2 (Calculating the inter-area routes) says:

> If [...] collection of destinations described by the summary-LSA equals one of the router's configured area address ranges (see Section 3.5), and the particular area address range is active, then the summary-LSA should be ignored. "Active" means that there are one or more reachable (by intra-area paths) networks contained in the area range.

OSPF implementations usually use *discard* entries to implement the required behavior. For example, if we inspect the selected OSPF routes on A2 running FRR, we'll see the *discard inter-area* entry for the summarized prefix 192.168.0.0/24.

{{<cc>}}Selected OSPF routes on A2{{</cc>}}
```
a2# show ip ospf route
============ OSPF network routing table ============
N    10.0.0.3/32           [10] area: 0.0.0.0
                           via 10.0.0.3, eth1
N    10.0.0.4/32           [0] area: 0.0.0.0
                           directly attached to lo
N IA 10.0.0.5/32           [20] area: 0.0.0.0
                           via 10.0.0.3, eth1
N    10.0.0.6/32           [10] area: 0.0.0.3
                           via 10.0.0.6, eth3
D IA 192.168.0.0/24        Discard entry
N    192.168.0.1/32        [515] area: 0.0.0.1
                           via 192.168.0.2, eth2
N    192.168.0.2/32        [505] area: 0.0.0.1
                           via 192.168.0.2, eth2
```

### Double-Checking Our Conclusions

Let's double-check our conclusions. Remember the "_and the particular area address range is active_" part of the RFC rule I quoted? If we shut down the link between S2 and A2, A2 loses intra-area routes 192.168.0.x/32, and the area range 192.168.0.0/24 should no longer be active. We should therefore see the summary LSA 192.168.0.0/24 in the OSPF data for area 1 on A2 (but not anywhere else, as area 1 partitions when we shut down the S2-A2 link).

That's precisely how Cisco IOS works. The configured area range becomes *passive* and no longer affects the summary LSAs.

{{<cc>}}Overview of area status on A2 (running Cisco IOL) after the link S2-A2 is shut down{{</cc>}}
```
a2#show ip ospf topology-info

            OSPF Router with ID (10.0.0.4) (Process ID 1)


		Base Topology (MTID 0)

 Topology priority is 64
 Router is not originating router-LSAs with maximum metric
 Number of areas transit capable is 0
 Initial SPF schedule delay 50 msecs
 Minimum hold time between two consecutive SPFs 200 msecs
 Maximum wait time between two consecutive SPFs 5000 msecs
    Area BACKBONE(0.0.0.0)
	SPF algorithm last executed 00:04:27.060 ago
	SPF algorithm executed 8 times
	Area ranges are
    Area 0.0.0.1
	SPF algorithm last executed 00:02:22.112 ago
	SPF algorithm executed 7 times
	Area ranges are
	   192.168.0.0/24 Passive Advertise
    Area 0.0.0.3
	SPF algorithm last executed 00:04:27.060 ago
	SPF algorithm executed 4 times
        Area ranges are
```

Consequently, the summary LSA advertised by A1 becomes the best route for 192.168.0.0/24, and the corresponding summary LSAs are advertised into areas 1 and 3.

{{<cc>}}Best OSPF routes on A2 running Cisco IOL{{</cc>}}
```
a2#show ip ospf rib

            OSPF Router with ID (10.0.0.4) (Process ID 1)


		Base Topology (MTID 0)

OSPF local RIB
Codes: * - Best, > - Installed in global RIB

*>  10.0.0.3/32, Intra, cost 11, area 0.0.0.0
      via 10.0.0.3, Ethernet0/1
*   10.0.0.4/32, Intra, cost 1, area 0.0.0.0, Connected
      via 10.0.0.4, Loopback0
*>  10.0.0.5/32, Inter, cost 21, area 0.0.0.0
      via 10.0.0.3, Ethernet0/1
*>  10.0.0.6/32, Intra, cost 11, area 0.0.0.3
      via 10.0.0.6, Ethernet0/3
*>  192.168.0.0/24, Inter, cost 21, area 0.0.0.0
      via 10.0.0.3, Ethernet0/1
```

{{<cc>}}The contents of OSPF database for area 1 on A2 running Cisco IOL{{</cc>}}
```
a2#show ip ospf 1 0.0.0.1 database

            OSPF Router with ID (10.0.0.4) (Process ID 1)

		Router Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
10.0.0.3        10.0.0.3        428         0x80000003 0x003E61 1
10.0.0.4        10.0.0.4        298         0x80000004 0x007DA5 0
192.168.0.1     192.168.0.1     428         0x80000007 0x002716 3
192.168.0.2     192.168.0.2     427         0x80000006 0x002F0C 3

		Summary Net Link States (Area 0.0.0.1)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.3        10.0.0.3        438         0x80000001 0x00869B
10.0.0.3        10.0.0.4        427         0x80000001 0x00E432
10.0.0.4        10.0.0.3        429         0x80000001 0x00E036
10.0.0.4        10.0.0.4        436         0x80000001 0x0076A9
10.0.0.5        10.0.0.3        429         0x80000001 0x00D63F
10.0.0.5        10.0.0.4        427         0x80000001 0x0035D5
10.0.0.6        10.0.0.3        428         0x80000001 0x0031D9
10.0.0.6        10.0.0.4        426         0x80000001 0x00C64D
192.168.0.0     10.0.0.4        298         0x80000001 0x003878
```

{{<note info>}}
The OSPF database on A2 still contains router LSAs advertised by S1, S2, and A1, even though they're no longer reachable (the link S2-A2 is down). It takes up to an hour to purge an unreachable LSA from the OSPF database.
{{</note>}}

Unfortunately, it seems that FRRouting developers didn't read the OSPFv2 RFC as carefully as Cisco IOS developers did (Arista EOS is exhibiting similar symptoms). After the S2-A2 link is shut down, A2 loses its only neighbor in area 1, and consequently, all LSAs originated by other routers in area 1 become unreachable.

A2 reacts to the topology change and revokes its summary LSA for 192.168.0.0/24 from the backbone area and area 3 (so far, so good).

{{<cc>}}Summary link states in OSPF database on A2 running FRRouting{{</cc>}}
```
a2# show ip ospf database
...
                Summary Link States (Area 0.0.0.0)

Link ID         ADV Router      Age  Seq#       CkSum  Route
10.0.0.5       10.0.0.3          47 0x80000001 0xae88 10.0.0.5/32
10.0.0.6       10.0.0.4          46 0x80000001 0x9e96 10.0.0.6/32
192.168.0.0    10.0.0.3          47 0x80000001 0x16bc 192.168.0.0/24
192.168.0.0    10.0.0.4        3600 0x80000001 0x10c1 192.168.0.0/24
...
                Summary Link States (Area 0.0.0.1)

Link ID         ADV Router      Age  Seq#       CkSum  Route
10.0.0.3       10.0.0.3          63 0x80000001 0x5ee4 10.0.0.3/32
10.0.0.3       10.0.0.4          56 0x80000001 0xbc7b 10.0.0.3/32
10.0.0.4       10.0.0.3          58 0x80000001 0xb87f 10.0.0.4/32
10.0.0.4       10.0.0.4          61 0x80000001 0x4ef2 10.0.0.4/32
10.0.0.5       10.0.0.3          49 0x80000001 0xae88 10.0.0.5/32
10.0.0.5       10.0.0.4          46 0x80000001 0x0d1f 10.0.0.5/32
10.0.0.6       10.0.0.3          49 0x80000001 0x0923 10.0.0.6/32
10.0.0.6       10.0.0.4          46 0x80000001 0x9e96 10.0.0.6/32
...
                Summary Link States (Area 0.0.0.3)

Link ID         ADV Router      Age  Seq#       CkSum  Route
10.0.0.3       10.0.0.4          56 0x80000001 0xbc7b 10.0.0.3/32
10.0.0.4       10.0.0.4          61 0x80000001 0x4ef2 10.0.0.4/32
10.0.0.5       10.0.0.4          46 0x80000001 0x0d1f 10.0.0.5/32
192.168.0.0    10.0.0.4        3600 0x80000001 0x10c1 192.168.0.0/24
```

Even though the **area range** is now inactive (A2 has no information about prefixes within 192.168.0.0/24), A2 neither creates a discard route nor uses the backbone summary LSA for 192.168.0.0/24. Consequently, area 3 loses reachability with area 1.

{{<cc>}}Best OSPF routes on A2 running FRRouting{{</cc>}}
```
a2# show ip ospf route
============ OSPF network routing table ============
N    10.0.0.3/32           [10] area: 0.0.0.0
                           via 10.0.0.3, eth1
N    10.0.0.4/32           [0] area: 0.0.0.0
                           directly attached to lo
N IA 10.0.0.5/32           [20] area: 0.0.0.0
                           via 10.0.0.3, eth1
N    10.0.0.6/32           [10] area: 0.0.0.3
                           via 10.0.0.6, eth3
```

However, after the router link states in the OSPF database on A2 age out, A2 generates the expected summary LSAs for the now-inactive area range. It looks like FRRouting OSPF implementation determines whether an area range is *active* based on the presence of LSAs in the OSPF database, not on whether (yet again quoting RFC 2328, this time [section 11.1](https://datatracker.ietf.org/doc/html/rfc2328#page-111)):

> The range contains one or more networks **reachable** by intra-area paths.

### Reproducing the Results

The _netlab_ topology I used to create the blog post is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/OSPF/area-range/topology.yml) ([details](/2025/04/ospf-summary-lsa-loop-prevention/#netlab)). You can start it (immediately and free-of-charge) in a [GitHub Codespace container](/2024/07/netlab-examples-codespaces/) -- change the directory within the Codespace container to `OSPF/area-range` and execute **netlab up**. Have fun.
