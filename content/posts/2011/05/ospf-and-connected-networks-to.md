---
date: 2011-05-03 06:59:00+02:00
ospf_tag: config
tags:
- OSPF
title: 'OSPF and Connected Networks: To Redistribute or Not?'
url: /2011/05/ospf-and-connected-networks-to/
---
A few days ago, I was discussing a data center design with a seasoned network architect. During the MPLS discussions, he made an offhand remark "There are still some switches running OSPF and using **network 0.0.0.0** and **redistribute connected.**" My first thought was, "This can't be good," but I had no idea how bad it was until I ran a lab test.

The generic dilemma along the lines of "should I make connected interfaces part of my OSPF process (and make them passive) or should I redistribute them into OSPF" has no clear-cut answer (apart from the obvious "it depends") \... and Google will quickly find you tons of lengthy discussions.
<!--more-->
However, doing both is clearly harmful, as the router includes connected subnets as stub links in its Type-1 LSA (causing full SPF run every time an interface flaps) *and* generates Type-5 LSA for every connected subnet (and you know the pesky Type-5 LSAs will just whizz by any summarization boundary and plague the whole OSPF domain). To make matters even more complex, in some Cisco IOS releases, specifying the OSPF area on an interface (with the **ip ospf area** interface configuration command) *disables the generation of Type-5 LSA* whereas using the **network** statement does not.

The next printout shows the summary of the IP addressing/OSPF configuration I was using (I started a single router in one of the OSPF labs that you get as part of the [DMVPN -- From Basics to Scalable Networks](https://www.ipspace.net/DMVPN:_From_Basics_to_Scalable_Networks) webinar).

``` code
interface Loopback0
 ip address 10.0.1.5 255.255.255.255
 ip ospf 1 area 11
!
interface Tunnel0
 ip address 192.168.0.5 255.255.255.0
 ip ospf network broadcast
 ip ospf priority 0
!
interface Tunnel1
 ip address 192.168.1.5 255.255.255.0
 ip ospf network broadcast
 ip ospf priority 0
!
interface FastEthernet0/0
 ip address 172.16.11.1 255.255.255.0
 ip ospf 1 area 11
!
interface Serial1/0
 ip address 10.0.7.9 255.255.255.252
 encapsulation ppp
!
router ospf 1
 log-adjacency-changes
 redistribute connected subnets
 network 0.0.0.0 255.255.255.255 area 11
```

The router has five operational IP-enabled interfaces:

``` code
R2#show ip interface brief | include up
FastEthernet0/0       172.16.11.1     YES NVRAM  up          up
Serial1/0             10.0.7.9        YES NVRAM  up          up
Loopback0             10.0.1.5        YES NVRAM  up          up
Tunnel0               192.168.0.5     YES NVRAM  up          up
Tunnel1               192.168.1.5     YES NVRAM  up          up
```

OSPF is running on five interfaces (as expected), all of them covered by the **network** statement. OSPF area is specified on two of them with interface configuration commands:

``` code
R2#show ip ospf interface | include protocol|Area|Enabled
Loopback0 is up, line protocol is up
  Internet Address 10.0.1.5/32, Area 11
  Enabled by interface config, including secondary ip addresses
Tunnel1 is up, line protocol is up
  Internet Address 192.168.1.5/24, Area 11
Tunnel0 is up, line protocol is up
  Internet Address 192.168.0.5/24, Area 11
Serial1/0 is up, line protocol is up
  Internet Address 10.0.7.9/30, Area 11
FastEthernet0/0 is up, line protocol is up
  Internet Address 172.16.11.1/24, Area 11
  Enabled by interface config, including secondary ip addresses
```

The OSPF database has one Type-1 LSA (with five links) and three Type-5 LSAs:

``` code
R2#show ip ospf database

            OSPF Router with ID (10.0.1.5) (Process ID 1)

                Router Link States (Area 11)

Link ID         ADV Router      Age         Seq#       Checksum Link count
10.0.1.5        10.0.1.5        806         0x80000006 0x00C926 5

                Type-5 AS External Link States

Link ID         ADV Router      Age         Seq#       Checksum Tag
10.0.7.8        10.0.1.5        862         0x80000001 0x003644 0
192.168.0.0     10.0.1.5        812         0x80000001 0x00B670 0
192.168.1.0     10.0.1.5        808         0x80000001 0x00AB7A 0
```

The stub network links of the Type-1 LSA include all five directly connected interfaces:

``` code
R2#show ip ospf database router 10.0.1.5 | include Network
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.5
     (Link Data) Network Mask: 255.255.255.255
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 192.168.1.0
     (Link Data) Network Mask: 255.255.255.0
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 192.168.0.0
     (Link Data) Network Mask: 255.255.255.0
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.7.8
     (Link Data) Network Mask: 255.255.255.252
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 172.16.11.0
     (Link Data) Network Mask: 255.255.255.0
```

To summarize:

-   The router has five directly connected IP subnets; all of them are part of the OSPF routing protocol *and* redistributed into OSPF;
-   The Type-1 LSA has five stub networks (as expected)
-   Connected subnets are also inserted into the OSPF database as Type-5 LSAs (as expected)
-   However, only three connected subnets (those without **ip ospf area** interface configuration command) are redistributed into OSPF.

Weird? Absolutely. Confusing? You bet.

### Recommendation

Use one or the other mechanism, not both. If you decide to redistribute connected subnets into OSPF with the **redistribute connected subnets** command, don't use the **network**-based routing protocol configuration; use **ip ospf area** interface configuration commands on transit interfaces to minimize the number of Type-5 LSAs inserted into the OSPF database.
