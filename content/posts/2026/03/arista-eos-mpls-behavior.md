---
title: "Arista EOS MPLS P/PE-router Behavior"
date: 2026-03-19 08:03:00+0100
tags: [ MPLS ]
---
Something didn't feel right as I tried to check whether the [IPv4 ECMP](/2026/03/ecmp-arista-ceos/) I observed in the latest version of Arista cEOS containers works with my [MPLS/anycast scenario](/2021/11/anycast-mpls/). The forwarding tables seemed OK, but I wasn't getting MPLS labels in the ICMP replies (see [RFC 4950](https://datatracker.ietf.org/doc/html/rfc4950) for details), even though I know Arista EOS can generate them.

I decided to go down that rabbit hole and built the simplest possible BGP-free core (the addition of BGP will become evident in a few seconds) to investigate PE/P-router behavior:

{{<figure src="/2026/03/ldp-lfib-topo.png" caption="Lab topology">}}
<!--more-->
After starting the lab ([lab topology](https://github.com/ipspace/netlab-examples/blob/master/MPLS/ldp-lfib/topology.yml) in case you want to [reproduce the behavior](/2024/07/netlab-examples-codespaces/)), I started checking the usual data structures:

* LDP bindings seemed OK. However, like Junos, but unlike Cisco IOS, Arista EOS creates bindings only for the /32 IPv4 prefixes.

{{<cc>}}LDP bindings on PE1 running Arista EOS{{</cc>}}
```
pe1#show mpls ldp bindings
10.0.0.1/32
   Local binding:  Label: imp-null
   Remote binding: Peer ID: 10.0.0.3:0, Label: 100000
10.0.0.2/32
   Local binding:  Label: 116386
   Remote binding: Peer ID: 10.0.0.3:0, Label: 100002
10.0.0.3/32
   Local binding:  Label: 116384
   Remote binding: Peer ID: 10.0.0.3:0, Label: imp-null
10.0.0.4/32
   Local binding:  Label: 116385
   Remote binding: Peer ID: 10.0.0.3:0, Label: 100001
```

* Based on the LDP bindings, the LFIB looked OK:

{{<cc>}}LFIB on PE1 running Arista EOS{{</cc>}}
```
pe1#show mpls route
[...]
 116384  A[1]
                via M, 10.1.0.1, pop
                    EgressACL: apply
                    directly connected, Ethernet2
                    ca:f0:00:03:00:01, vlan 1007
 116385  A[1]
                via M, 10.1.0.1, swap 100001
                    EgressACL: apply
                    directly connected, Ethernet2
                    ca:f0:00:03:00:01, vlan 1007
 116386  A[1]
                via M, 10.1.0.1, swap 100002
                    EgressACL: apply
                    directly connected, Ethernet2
                    ca:f0:00:03:00:01, vlan 1007
```

* The root cause turned out to be the forwarding table. Contrary to Cisco IOS, which uses MPLS encapsulation for all prefixes with known LDP bindings from downstream routers, **Arista EOS performs MPLS encapsulation for BGP destinations**, but not for IGP destinations:

{{<cc>}}Forwarding table on PE1 running Arista EOS{{</cc>}}
```
pe1#show ip route | begin Gateway
Gateway of last resort is not set

 C        10.0.0.1/32
           directly connected, Loopback0
 I L2     10.0.0.2/32 [115/40]
           via 10.1.0.1, Ethernet2
 I L2     10.0.0.3/32 [115/20]
           via 10.1.0.1, Ethernet2
 I L2     10.0.0.4/32 [115/30]
           via 10.1.0.1, Ethernet2
 C        10.1.0.0/30
           directly connected, Ethernet2
 I L2     10.1.0.4/30 [115/20]
           via 10.1.0.1, Ethernet2
 I L2     10.1.0.8/30 [115/30]
           via 10.1.0.1, Ethernet2
 C        172.16.0.0/24
           directly connected, Ethernet1
 B I      172.16.1.0/24 [200/0]
           via 10.0.0.2/32, LDP tunnel index 3
              via 10.1.0.1, Ethernet2, label 100002
```

You might have noticed a few other weird details in the printouts:

* The **vlan 1007** in the LFIB printout is the [internal VLAN](/2025/03/routed-interfaces-layer-3-switches/) used for the layer-3 interface between PE1 and P1:

{{<cc>}}Internal VLAN usage on PE1 running Arista EOS{{</cc>}}
```
pe1#show vlan internal usage
1006  Ethernet1
1007  Ethernet2
```

* The LDP-assigned labels for the same prefix vary wildly between different devices. For example, PE1 assigns 116385 to 10.0.0.4/32, while its peer (running the same software and with the same settings) assigns 100001. The culprits are the default allocation ranges assigned by Arista EOS -- LDP gets the lowest labels *unless you configured BGP before it*. Changing the label ranges with the **mpls label range** command doesn't help either, as BGP and LDP use the same *dynamic* allocation pool.

{{<cc>}}Arista EOS MPLS label ranges on PE1 (BGP + LDP){{</cc>}}
```
pe1#show mpls label ranges
Start     End       Size      Usage
------------------------------------------------
0         15        16        reserved
16        99999     99984     static mpls
100000    116383    16384     bgp (dynamic)
116384    132767    16384     ldp (dynamic)
132768    362143    229376    free (dynamic)
362144    899999    537856    unassigned
900000    965535    65536     bgp-sr
900000    965535    65536     isis-sr
900000    965535    65536     ospf-sr
965536    1031071   65536     srlb
1031072   1032095   1024      l2evpn shared ethernet-segment
1032096   1036287   4192      unassigned
1036288   1048575   12288     l2evpn
```

{{<cc>}} Arista EOS MPLS label ranges on PE1 (LDP only){{</cc>}}
```
p1#show mpls label ranges
Start     End       Size      Usage
------------------------------------------------
0         15        16        reserved
16        99999     99984     static mpls
100000    116383    16384     ldp (dynamic)
116384    362143    245760    free (dynamic)
362144    899999    537856    unassigned
900000    965535    65536     bgp-sr
900000    965535    65536     isis-sr
900000    965535    65536     ospf-sr
965536    1031071   65536     srlb
1031072   1032095   1024      l2evpn shared ethernet-segment
1032096   1036287   4192      unassigned
1036288   1048575   12288     l2evpn
```
