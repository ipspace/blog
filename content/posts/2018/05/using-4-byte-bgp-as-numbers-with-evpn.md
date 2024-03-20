---
date: 2018-05-07 07:47:00+02:00
evpn_tag: details
pre_scroll: true
tags:
- EVPN
title: Using 4-Byte BGP AS Numbers With EVPN on Junos
url: /2018/05/using-4-byte-bgp-as-numbers-with-evpn.html
---
After documenting the [basic challenges of using EBGP and 4-byte AS numbers with EVPN automatic route targets](http://www.ipspace.net/Data_Center_BGP/EVPN_Route_Target_Considerations), I asked my friends working for various vendors how their implementation solves these challenges. This is what [Krzysztof Szarkowicz](https://www.oreilly.com/pub/au/6140) sent me on specifics of Junos implementation:
<!--more-->
Four byte ASN can be used with EVPN (from Junos 13.x), including within an EVPN RT community, where the AS number takes four bytes, leaving two bytes for the VPN ID. Here is an example of EVPN advertisement with four-byte ASN from Junos EVPN PE:

``` code
root@R1# run show route advertising-protocol bgp 192.168.0.4 table RI-EVPN-1.evpn.0 detail    
W15: Sun 2018-04-15T16:32:18 CEST (UTC+0200)
 
RI-EVPN-1.evpn.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)
* 1:192.168.0.1:201::0201222222000000::0/192 AD/EVI (1 entry, 1 announced)
 BGP group IBGP-TO-RR type Internal
     Route Distinguisher: 192.168.0.1:201
     Route Label: 37
     Nexthop: Self
     Localpref: 100
     AS path: [4200000000] I ← Local AS is 4200000000
     Communities: target:4200000000L:1111 ← RT with 4-byte ASN
```

However, 4B ASN doesn't currently (18.1) works with automatic RT. When Automatic RT is used together with 4B ASN, 16 least significant bits from 4B ASN are used to populate automatic RT, e.g.:

``` code
* 2:192.168.0.1:201::201::00:11:11:11:11:11/304 MAC/IP (1 entry, 1 announced)
 BGP group IBGP-TO-RR type Internal
     Route Distinguisher: 192.168.0.1:201
     Route Label: 81
     ESI: 00:11:22:33:44:55:66:00:00:00
     Nexthop: Self
     Localpref: 100
     AS path: [4200000000] I ← Local AS is 4200000000
     Communities: target:59904:201 mac-mobility:0x1:sticky (sequence 0). ← 59904 is used in automatic RT
```

Where:

``` code
4200000000:    0xFA56EA00
     59904:        0xEA00
```

#### More Details on Automatic Route Targets in EBGP Environment

Automatic RT on MX platforms works since Junos 18.1. The ASN part is taken from global AS configuration ('set routing-options autonomous-system \<ASN\>').

In case of four-byte ASN, only 16 least significant bits are taken from global AS to generate automatic RT. In Junos, EBGP IP fabric configuration with automatic RT is quite simple, since we can define different local AS for iBGP (EVPN Overlay, RT autogeneration) and eBGP (Underlay).

Also, there is one more aspect, which are important from RT perspective. EVPN Type 4 routes have auto generated RTs encoded as ES-Import RT communities (RFC 7432, Section 7.6). Here's an example:

``` code
* 4:192.168.0.1:0::112233445566000000:192.168.0.1/296 ES (1 entry, 1 announced) ← encoded ESI: Type 0
 BGP group IBGP-TO-RR type Internal
     Route Distinguisher: 192.168.0.1:0
     Nexthop: Self
     Localpref: 100
     AS path: [4200000000] I
     Communities: es-import-target: 11-22-33-44-55-66 ← ES-Import RT
```

These ES-Import RTs are generated from ESI, e.g.:

``` code
set interfaces ge-0/0/4 unit 201 esi 00:11:22:33:44:55:66:00:00:00
```

ESI has 10 bytes; ES-Import RT has space for 6 bytes payload (useful info). Therefore, first 6 most significant bytes from ESI payload are taken to generate ES-Import RT. In ESI, first byte is ESI Type (e.g. Type 0: manually configured), Therefore in the above example 11:22:33:44:55:66 are taken from configured ESI and used to populate advertised ES-Import RT. ES-Import RT enables all the PEs connected to the same multihomed site to import the Ethernet Segment (Type 4) routes.

Now, if I have following ESIs configured on some interfaces:

``` code
00:00:00:00:11:22:33:44:55:66, connected to PE1/PE2
00:00:00:00:11:22:33:44:55:77, connected to PE2/PE3
00:00:00:00:11:22:33:44:55:88, connected to PE3/PE1 
```

ES-Import RT will be:

``` code
00:00:00:00:11:22:33:44:55:66, —> 00:00:00:11:22:33 
00:00:00:00:11:22:33:44:55:77, —> 00:00:00:11:22:33
00:00:00:00:11:22:33:44:55:88, —> 00:00:00:11:22:33
```

That is, it is the same for all above ESIs. So, all PEs will import these Type 4 routes, but later, based on the actual ESI advertised in this Type 4 routes, and actual ESI configured on some local interface, if there is no match, the route will not be used.

So, while from EVPN machinery perspective, it is OK, it is not most optimal. Most optimal (i.e. for control plane optimization), is to differentiate ESIs in the first 6 useful bytes (rather than use last 3 bytes), so that generated ES-Import RT prevents these routes from even being imported on PEs that don't need them.

#### Master EVPN and Data Center Fabrics

-   Want to know more about EVPN technology? Watch the [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.
-   Want to know how to use EVPN in data center fabric designs? Watch the [Mixed Layer-2+3 Fabrics](https://my.ipspace.net/bin/list?id=Clos#L2_L3_FABRIC) section of [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.
-   Want to learn the basics of data center fabrics and figure out what individual vendors are doing? Check out the [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar.
-   Looking for a guided and mentored tour with plenty of peer- and instructor support? You probably need [Designing and Building Data Center Fabrics online course](http://www.ipspace.net/Designing_and_Building_Data_Center_Fabrics).
