---
date: 2008-11-04 11:43:00+01:00
ospf_tag: adj
tags:
- OSPF
title: 'Mixing Numbered and Unnumbered OSPF Interfaces: Solution'
url: /2008/11/ospf-challenge-2-final-results/
---
I've received almost a dozen responses to the [second OSPF challenge](/2008/10/ospf-challenge-2-mixing-numbered-and/), most of them correct. The key to the solution is the way OSPF checks the neighbor's IP address on point-to-point links ([we already know that the subnet mask is ignored](/2008/10/ospf-challenge-1-final-results/)):

-   If the interface is unnumbered, the router ignores the source IP address in the OSPF hello packets.
-   If there's an IP address configured on the interface, the router checks that the neighbor's IP address (the source IP address in the OSPF hello packets) belongs to the same subnet. If the source IP address is not in the same subnet, the OSPF hello packet is ignored.
<!--more-->
R1 and R2 ([the router configuration can be found in the challenge](/2008/10/ospf-challenge-2-mixing-numbered-and/)) would establish adjacency only if the source IP address of the packets sent by R1 would be in the same subnet as the IP address on R2. Since the serial interface on R1 is unnumbered, R1 would use the IP address of the loopback interface in the OSPF hello packets. IP address of the loopback interface on R1 thus has to be in the 10.1.2.0/29 subnet, giving you five choices (you cannot use the 10.1.2.0, 10.1.2.7 and 10.1.2.3).

However, as Yuri pointed out in his response, the routers do establish adjacency (so the challenge is solved) but do not build valid routing tables. The reason is the weird IP address used in the *Link Data* field of each unnumbered point-to-point link. According to RFC 2328, the router should [use the MIB-II ifIndex as the IP address of an unnumbered interface](http://tools.ietf.org/html/rfc2328). IOS performs subnet checks on the SPF tree as well as on the OSPF hello packets, and therefore, R2 declares that R1 is not reachable. The following printout shows the R1's router LSA as seen on R2:

``` {.code}
R2#show ip ospf data router 10.1.2.4

            OSPF Router with ID (10.1.2.3) (Process ID 1)

                Router Link States (Area 1)

  Adv Router is not-reachable
  LS age: 758
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.1.2.4
  Advertising Router: 10.1.2.4
  LS Seq Number: 80000016
  Checksum: 0x296B
  Length: 48
  Number of Links: 2

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.1.2.4
     (Link Data) Network Mask: 255.255.255.255
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.3
     (Link Data) Router Interface address: 0.0.0.6
      Number of TOS metrics: 0
       TOS 0 Metrics: 64
```
