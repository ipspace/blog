---
kb_section: OSPF
minimal_sidebar: true
pre_scroll: true
title: Type-1 (Router) LSA in OSPF Topology Database
url: /kb/tag/OSPF/Type-1-LSA/
tags: [ OSPF ]
ospf_tag: details
---
The OSPF type-1 (router) LSA describes an OSPF router, its stub interfaces and links to adjacent OSPF routers and transit networks in the same area. Every type-1 LSA describes numerous connections the router has:

* Point-to-point links to adjacent routers (type-1 link)
* Links to transit networks described by type-2 LSA (type-2 link)
* Stub interfaces (type-3 link)
* Virtual links (type-4 link)

An OSPF router originates a single type-1 LSA for each area that it belongs to. The type-1 LSA is flooded within a single area and never crosses an area boundary. Type-3 (summarization) LSA is used to advertise IP prefixes listed in a type-1 LSA into another area.

## Stub Interfaces

A type-3 (stub) link is added to the router LSA for each stub interface belonging to the OSPF process. A stub interface could be a loopback interface or any other point-to-point or multipoint interface on which there are no OSPF neighbors.

**Example \#1:** A router with a single loopback interface generates a type-1 LSA (even though it has no OSPF neighbors) with a single stub link.

{{<cc>}}Loopback interface in an OSPF process{{</cc>}}

```
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes 
```

{{<cc>}}OSPF-enabled interfaces{{</cc>}}

```
A1#show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Lo0          1     1               10.0.1.1/32        1     LOOP  0/0 
```

{{<cc>}}Contents of the router LSA{{</cc>}}

```
A1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 1)

  LS age: 34
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 80000001
  Checksum: 0x55B8
  Length: 36
  Number of Links: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1 
```

**Example \#2:** A router with a loopback interface and a multi-access (LAN) interface with no OSPF neighbors generates a type-1 LSA with two stub links, one describing the loopback interface, the other the LAN interface.

{{<cc>}}Two interfaces belonging to an OSPF process{{</cc>}}

```
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip ospf 1 area 1
!
interface FastEthernet0/1
 description LAN 1 (A2)
 ip address 10.2.1.1 255.255.255.0
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/1 
```

{{<cc>}}State of the OSPF interfaces{{</cc>}}

```
A1#show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Fa0/1        1     1               10.2.1.1/24        1     DR    0/0
Lo0          1     1               10.0.1.1/32        1     LOOP  0/0 
```

{{<cc>}}Router LSA with two stub links{{</cc>}}

```
A1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 1)

  LS age: 74
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 80000002
  Checksum: 0xD01E
  Length: 48
  Number of Links: 2

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.2.1.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1 
```

## Numbered Point-to-Point Interfaces

Two links are added to the router LSA for each point-to-point interface with an established OSPF adjacency:

-   A router (type-1) link describing the connection to the OSPF neighbor
-   A stub (type-3) link describing the subnet of the point-to-point interface.

The *router interface address* field in the *router link* is the local IP address assigned to the interface.

[RFC 6860](https://tools.ietf.org/html/rfc6860) (Hiding Transit-Only Networks in OSPF) modifies this rule -- a router can omit the type-3 link from router LSA. You can configure this functionality on a router running Cisco IOS with **prefix-suppression** router configuration command (applicable to all interfaces in the selected OSPF process) or **ip ospf prefix-suppression** interface configuration command.

**Example \#3:** A router with a loopback interface and a point-to-point WAN link generates a type-1 LSA with two stub links (one describing the loopback interface, the other the point-to-point WAN subnet) and a router link (describing the connection to the OSPF neighbor).

{{<cc>}}OSPF is configured on a WAN interface{{</cc>}}

```
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip ospf 1 area 1
!
interface Serial1/0
 ip address 10.0.7.5 255.255.255.252
 encapsulation ppp
 ip ospf cost 100
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes 
```

{{<cc>}}State of the OSPF interfaces{{</cc>}}

```
A1#show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Se1/0        1     1               10.0.7.5/30        100   P2P   1/1
Lo0          1     1               10.0.1.1/32        1     LOOP  0/0 
```

{{<cc>}}Router LSA describing a point-to-point link and a loopback interface{{</cc>}}

```
A1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 1)

  LS age: 67
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 80000004
  Checksum: 0x24C8
  Length: 60
  Number of Links: 3

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 10.0.7.5
      Number of MTID metrics: 0
       TOS 0 Metrics: 100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.7.4
     (Link Data) Network Mask: 255.255.255.252
      Number of MTID metrics: 0
       TOS 0 Metrics: 100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1 
```


## Unnumbered Point-to-Point Interfaces

A point-to-point (type-1) link is added to the router LSA for each OSPF neighbor reachable across an unnumbered point-to-point interface. No stub link is added to the router LSA as the interface does not have a stub subnet.

The *router interface address* field in the *router link* is an internal interface number (not necessary equal to the SNMP index of the local interface as required by RFC 2328).

**Example \#4:** A router with a loopback interface and an unnumbered point-to-point WAN link generates a type-1 LSA with a stub link (describing the loopback interface) and a router link (describing the connection to the OSPF neighbor).

{{<cc>}}OSPF running over an unnumbered interface{{</cc>}}

```
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip ospf 1 area 1
!
interface Serial1/0
 ip unnumbered Loopback0
 encapsulation ppp
 ip ospf cost 100
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes 
```

{{<cc>}}OSPF interface state{{</cc>}}

```
A1#show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Se1/0        1     1               0.0.0.0/30         100   P2P   1/1
Lo0          1     1               10.0.1.1/32        1     LOOP  0/0 
```

{{<cc>}}Router LSA has a single router link and a single stub link{{</cc>}}

```
A1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 1)

  LS age: 459
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 80000006
  Checksum: 0x67C
  Length: 48
  Number of Links: 2

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.4
     (Link Data) Router Interface address: 0.0.0.5
      Number of MTID metrics: 0
       TOS 0 Metrics: 100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1 
```

The contents of the *Router Interface address* field in the *router link* in the router LSA do not necessarily match the SNMP interface index (displayed below).

{{<cc>}}SNMP interface index of the WAN interface{{</cc>}}

```
A1#show snmp mib ifmib ifindex Serial1/0
Interface = Serial1/0, Ifindex = 3 
```

## Links to Transit Multi-Access Interfaces

Router LSA contains a *link to transit network* (type-2 link) for each transit broadcast or NBMA interface. The *transit network* referred to in the router LSA is the type-2 LSA originated by the designated router selected on the interface.

{{<note note>}}A *transit* interface is a multi-access interface with at least one OSPF neighbor.{{</note>}}

The router advertises a multi-access interface as a stub link as long as it has no OSPF neighbors reachable through the interface. When the adjacency to the first OSPF neighbor reaches the FULL state, the router LSA is changed: one of the routers originates the network (type-2) LSA and the *stub link* is replaced by a *transit link*.

**Example \#5:** A router with a loopback interface and a transit Ethernet interface generates a type-1 LSA with a stub link (describing the loopback interface) and link to a transit network (the type-2 LSA originated by the DR).

{{<cc>}}Relevant parts of the router configuration{{</cc>}}

```
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip ospf 1 area 1
!
interface FastEthernet0/0
 ip address 10.2.2.1 255.255.255.0
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes 
```

The **show ip ospf interface** command shows a single OSPF neighbor on the Fast Ethernet interface. A1 is the backup DR (the *State* column in the printout), therefore the other router must be the DR.

{{<cc>}}OSPF interface state{{</cc>}}

```
A1#show ip ospf interface brief
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Fa0/0        1     1               10.2.2.1/24        1     BDR   1/1
Lo0          1     1               10.0.1.1/32        1     LOOP  0/0 
```

The router LSA has two links: a stub link and a link to the type-2 LSA originated by the DR.

{{<cc>}}Router LSA describing a connection to a transit network{{</cc>}}

```
A1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.1.1) (Process ID 1)

                Router Link States (Area 1)

  LS age: 545
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 8000000A
  Checksum: 0x874D
  Length: 48
  Number of Links: 2

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.2.2.3
     (Link Data) Router Interface address: 10.2.2.1
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1 
```
