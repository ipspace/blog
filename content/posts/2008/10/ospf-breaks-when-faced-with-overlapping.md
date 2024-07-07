---
date: 2008-10-17 06:37:00.001000+02:00
ospf_tag: details
tags:
- OSPF
- PPP
- WAN
title: OSPF Breaks When Faced With Overlapping IP Addresses
url: /2008/10/ospf-breaks-when-faced-with-overlapping/
---
A while ago [cciepursuit](http://cciepursuit.wordpress.com/) described his [problems with PPP-over-Frame Relay](http://cciepursuit.wordpress.com/2008/09/21/ios-error-with-ospf-point-to-multipoint-network-in-pppofr-hub-and-spoke-topology/). Most probably his problems were caused by a static IP address assigned to the virtual template interface (this address gets cloned to all virtual access interfaces and IOS allows you to have the same IP address on multiple WAN point-to-point links). I recreated a very similar (obviously seriously broken) scenario in my lab using point-to-point subinterfaces over Frame Relay to simplify the setup.

{{<note warn>}}This is not something you'd want to do in your production network.{{</note>}}
<!--more-->
The relevant parts of router configurations are included below:

``` code
S1#show run | section interface Serial
interface Serial1/0
 no ip address
 encapsulation frame-relay
!
interface Serial1/0.100 point-to-point
 description Link to C1
 ip address 10.0.8.2 255.255.255.240
 frame-relay interface-dlci 100

S2#show run | section interface Serial
interface Serial1/0
 no ip address
 encapsulation frame-relay
 frame-relay lmi-type ansi
!
interface Serial1/0.100 point-to-point
 description Link to C1
 ip address 10.0.8.3 255.255.255.240
 frame-relay interface-dlci 100

C1#show run | section interface Serial
interface Serial1/0
 no ip address
 encapsulation frame-relay
!
interface Serial1/0.100 point-to-point
 description Link to S1
 ip address 10.0.8.1 255.255.255.240
 frame-relay interface-dlci 100
!
interface Serial1/0.101 point-to-point
 description Link to S2
 ip address 10.0.8.1 255.255.255.240
 frame-relay interface-dlci 101
```

I expected the distance vector protocols to work flawlessly, as they track the next hop as well as the inbound interface over which the routing update was received. With the following RIP configuration on all three routers ...

``` code
router rip
 version 2
 network 10.0.0.0
 no auto-summary
```

... the routing table on C1 looked almost OK, apart from the weird entry for the 10.0.8.0/28 subnet:

``` code
C1#show ip route | begin Gateway
Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 5 subnets, 3 masks
C       10.0.8.0/28 is directly connected, Serial1/0.100
                    is directly connected, Serial1/0.101
R       10.0.0.2/32 [120/1] via 10.0.8.3, 00:00:01, Serial1/0.101
C       10.0.0.3/32 is directly connected, Loopback0
R       10.0.0.1/32 [120/1] via 10.0.8.2, 00:00:02, Serial1/0.100
```

The next routing protocol was EIGRP; the configuration was very similar to the RIP case:

``` code
router eigrp 1
 network 10.0.0.0
 no auto-summary
```

Yet again, the IP routing table looks as expected:

``` code
C1#show ip route | begin Gateway
Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C       10.0.8.0/28 is directly connected, Serial1/0.100
                    is directly connected, Serial1/0.101
D       10.0.0.2/32 [90/2297856] via 10.0.8.3, 00:02:33, Serial1/0.101
C       10.0.0.3/32 is directly connected, Loopback0
D       10.0.0.1/32 [90/2297856] via 10.0.8.2, 00:02:33, Serial1/0.100
```

OSPF also behaved as expected, producing weird results. I never got both remote routes in the IP routing table on C1; one of them (or even both of them) was missing. This is not surprising; OSPF builds the SPF tree from the topology database and gets totally confused when two interfaces have the same IP address.

The information in the topology database is correct; in my lab, C1 advertised that it could reach S1 and S2 (both of them appeared as router-to-router links in the router LSA) ...

``` code
C1#show ip ospf database router self-originate

            OSPF Router with ID (10.0.0.3) (Process ID 2)

                Router Link States (Area 1)

  LS age: 283
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.3
  Advertising Router: 10.0.0.3
  Number of Links: 5

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.3
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.2
     (Link Data) Router Interface address: 10.0.8.1
      Number of TOS metrics: 0
       TOS 0 Metrics: 64

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.8.0
     (Link Data) Network Mask: 255.255.255.240
      Number of TOS metrics: 0
       TOS 0 Metrics: 64

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.1
     (Link Data) Router Interface address: 10.0.8.1
      Number of TOS metrics: 0
       TOS 0 Metrics: 64

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.8.0
     (Link Data) Network Mask: 255.255.255.240
      Number of TOS metrics: 0
       TOS 0 Metrics: 64
```

... but OSPF got totally confused when trying to build the SPF tree, deciding that one (or both) of remote routers was unreachable:

``` code
C1#show ip ospf database router adv-router 10.0.0.1

            OSPF Router with ID (10.0.0.3) (Process ID 2)

                Router Link States (Area 1)

  Adv Router is not-reachable
  LS age: 356
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.1
  Advertising Router: 10.0.0.1
  Number of Links: 3

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.3
     (Link Data) Router Interface address: 10.0.8.2
      Number of TOS metrics: 0
       TOS 0 Metrics: 64

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.8.0
     (Link Data) Network Mask: 255.255.255.240
      Number of TOS metrics: 0
       TOS 0 Metrics: 64

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.1
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1
```

In my humble opinion, Cisco IOS could do better (the topology table has enough information to build the correct SPF tree), but this is nonetheless a broken design that a router should never be exposed to.

**Summary:** Virtual template interfaces should be unnumbered to prevent address overlap on virtual access interfaces. If you insist on using a fixed IP address on virtual template interfaces, don't expect OSPF to work.
