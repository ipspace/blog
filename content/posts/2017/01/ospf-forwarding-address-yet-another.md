---
date: 2017-01-19 09:06:00+01:00
ospf_tag: fa
tags:
- OSPF
title: 'OSPF Forwarding Address: Yet Another Kludge'
url: /2017/01/ospf-forwarding-address-yet-another/
---
One of my readers sent me an interesting NSSA question (more in a future blog post) that sent me chasing for the reasons behind the OSPF Forwarding Address (FA) field in type-5 and type-7 LSAs.

This is the typical scenario for OSPF FA that I was able to find on the Internet:
<!--more-->
{{<figure src="/2017/01/s500-OSPF_FA_1.png">}}

Two OSPF ASBRs are connected to the same external network. Only one runs the external routing protocol (BGP in my diagram) and redistributes external prefixes into OSPF. You'd want to send the traffic toward external destinations through both ASBRs, but you can't do that as only one ASBR advertises the external routes.

Here are the relevant parts for E1 and E2 configuration. BGP (and redistribution into OSPF) is configured on E1 but not E2.

{{<cc>}}OSPF and BGP configuration on E1{{</cc>}}
``` code
interface Loopback0
 description Loopback
 ip address 192.168.0.1 255.255.255.255
 ip ospf 1 area 1
!
interface GigabitEthernet0/1
 description to C1
 ip address 10.0.128.1 255.255.255.252
 ip ospf 1 area 1
 ip ospf cost 1
!
interface GigabitEthernet0/2
 description to External_LAN
 ip address 10.0.0.1 255.255.128.0
!
router ospf 1
 redistribute bgp 65000 subnets
 passive-interface Loopback0
!
router bgp 65000
 bgp log-neighbor-changes
 redistribute ospf 1
 neighbor 10.0.0.2 remote-as 65001
```

{{<cc>}}OSPF configuration on E2{{</cc>}}
``` code
interface Loopback0
 description Loopback
 ip address 192.168.0.4 255.255.255.255
 ip ospf 1 area 1
!
interface GigabitEthernet0/1
 description to C1
 ip address 10.0.128.6 255.255.255.252
 ip ospf 1 area 1
 ip ospf cost 1
!
router ospf 1
```

And here's the relevant part of the OSPF topology database. The prefix 192.168.0.2/32 that is advertised by X1 over EBGP is redistributed as type-5 LSA into OSPF by E1 (192.168.0.1)

{{<cc>}}Type-5 LSA in OSPF topology database{{</cc>}}
``` code
C1#show ip ospf database external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

    Type-5 AS External Link States

  LS age: 301
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.0.2 (External Network Number )
  Advertising Router: 192.168.0.1
  LS Seq Number: 80000001
  Checksum: 0xA154
  Length: 36
  Network Mask: /32
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 1
  Forward Address: 0.0.0.0
  External Route Tag: 65001
```

Enter the YAK (Yet Another Kludge) twilight zone: what if the ASBR advertises the external next hop (forwarding address) in the type-5 LSA, and both ASBRs advertise the external prefix (hopefully as a stub network)? Recursive next-hop lookup would solve the problem, and C1 would get two equal-cost routes toward the external destinations.

To enable this functionality, E1 and E2 have to advertise the external subnet as an internal OSPF route, so we'll add the external interface to the OSPF process on E1 and E2.

{{<cc>}}Enabling OSPF on the external interface on E1 and E2{{</cc>}}
``` code
interface GigabitEthernet0/2
 description to External_LAN
 ip ospf cost 1
```

{{<note warn>}}It looks like on some versions of Cisco IOS, you cannot make the external interface passive (= stub network) -- the routers would not set a forwarding address if the next-hop is on a passive interface; the external network must be a fully-functional OSPF interface. I was not able to find any relevant requirements in RFC 2328.{{</note>}}

After the configuration change, the Type-5 LSA in the OSPF topology database gets the *forwarding address* value, and C1 gets two equal-cost paths to the external destination.

{{<cc>}}Type-5 LSA with Forwarding Address field set to external next hop{{</cc>}}
``` code
C1>show ip ospf database external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

Type-5 AS External Link States

  LS age: 907
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.0.2 (External Network Number )
  Advertising Router: 192.168.0.1
  LS Seq Number: 80000001
  Checksum: 0x2CBD
  Length: 36
  Network Mask: /32
Metric Type: 2 (Larger than any link state path)
MTID: 0
Metric: 1
Forward Address: 10.0.0.2
External Route Tag: 65001
```

{{<cc>}}Two equal-cost routes to external destination{{</cc>}}
``` code
C1>show ip route 192.168.0.2
Routing entry for 192.168.0.2/32
  Known via "ospf 1", distance 110, metric 1
  Tag 65001, type extern 2, forward metric 2
  Last update from 10.0.128.6 on GigabitEthernet0/2, 00:15:21 ago
  Routing Descriptor Blocks:
    10.0.128.6, from 192.168.0.1, 00:15:21 ago, via GigabitEthernet0/2
      Route metric is 1, traffic share count is 1
      Route tag 65001
  * 10.0.128.1, from 192.168.0.1, 00:15:21 ago, via GigabitEthernet0/1
      Route metric is 1, traffic share count is 1
      Route tag 65001
```

Problem solved? **NO, OF COURSE NOT**. You just made it worse:

-   Even though it looks like everything works as expected, E1 is a single point of failure -- if it crashes, you lose route redistribution and connectivity to external destinations;
-   The already-too-complex link-state routing protocol got another hard-to-figure-out quirk. See the *passive interface* gotcha above, and check all the complications T5 FA caused in OSPF route selection process ([RFC 2328](https://tools.ietf.org/html/rfc2328));
- To make this kludge work, you have to run OSPF on the external interface (at least with recent Cisco IOS releases). Not exactly the most secure design I've seen in my life (and please don't even mention that you could use an ACL to filter incoming OSPF packets on the external interface before [reading this blog post](/2013/08/temper-your-macgyver-streak/)).

The proper design would be to run external routing protocol and route redistribution on both ASBRs (yeah, I know, the beauties of two-way redistribution), and tell everyone who complained about this *deficiency* of OSPF to get lost and fix his design.

Alas, that's not how [standards are made](https://xkcd.com/927/). No wonder academics are making fun of the complexities of distributed routing protocols, and we're continuously involved in [YAK shaving](http://sethgodin.typepad.com/seths_blog/2005/03/dont_shave_that.html) exercises.
