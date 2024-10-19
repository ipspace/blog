---
date: 2012-07-31 07:09:00+02:00
tags:
- Internet
- BGP
- MPLS VPN
title: Is It Safe to Run Internet in a VRF?
url: /2012/07/is-it-safe-to-run-internet-in-vrf/
---
During the [February Packet Party](http://packetpushers.net/show-91-packet-party-feb-2012/), someone asked the evergreen question: "*Is it safe to run Internet services in a VRF?*" and my off-the-cuff answer was (as always) "*Doing that will definitely consume more memory than having the Internet routes in the global routing table.*" After a few moments, [Derick Winkworth](http://packetpushers.net/author/dwinkworth/) looked into one of his routers and confirmed the difference is huge \... but then [he has a very special setup](http://packetpushers.net/virtualizing-network-services-part-1-the-beginning/), so I decided to do a somewhat controlled test.
<!--more-->
### Results Summary

Running Internet services in a single VRF versus the global IP routing table increases the overall memory consumption by around 8% while providing a clean separation between the internal ISP network (in the global IP routing table) and the public Internet (in the Internet VRF).

Configuring Internet services with multiple VRFs having different route distinguishers (for example, using *Overlapping VPN* or *Common Services* designs) dramatically increases the memory consumption due to the [MPLS/VPN VPNv4 BGP route replication](/2012/07/bgp-route-replication-in-mplsvpn-pe/) and multiple copies of full Internet routing table in per-VRF FIBs. Every additional VRF increases the memory consumption by \~80%.

### Test Setup

The difference between having a global BGP and IP routing table and a VRF-based BGP table (and VPNv4 prefixes) should be much more noticeable with a large BGP table size, so I decided to announce a few hundred thousand BGP prefixes to a router running Cisco IOS release 15.1(3)S2.

I used the trick [Jeremy Gaddis described a while ago](http://evilrouters.net/2009/08/21/getting-bgp-routes-into-dynamips-with-video/), cursed [*bgp_simple*](http://code.google.com/p/bgpsimple/wiki/README) because it would send a different number of BGP prefixes every time I ran it, and finally decided to settle for approximate results.

I executed **show memory free** before the BGP session with *bgp_simple* was established, **show ip bgp summary** to see how many BGP prefixes the router received from *bgp_simple*, and **show memory alloc total** to see how much free memory was left and which processes were the largest memory consumers.

### Internet in the Global Routing Table

I used the following simple configuration to establish the baseline case. The router had a global EBGP session with a Linux machine running *bgp_simple.*

```
interface FastEthernet0/0
 ip address 10.17.0.1 255.255.255.0
!
router bgp 65000
 bgp log-neighbor-changes
 neighbor 10.17.0.2 remote-as 65100
```

Prior to the test, the router had almost 360M of free memory:

{{<cc>}}Free memory on PE-A prior to the *Internet in global routing table* test{{</cc>}}
```
PE-A#sh mem free
               Head   Total(b)    Used(b)    Free(b)  Lowest(b) Largest(b)
Processor  64FB4E00  402960204   41332768  361627436  361627436  352628556
      I/O   E000000   33554432    3134628   30419804   30419804   30417180
Transient  7D000000   16777216       5156   16772060   16772032   16772028
```

*bgp_simple* sent the router 186,683 BGP prefixes (from a file containing 200,000 unique BGP prefixes). They consumed a bit more than 45M:

{{<cc>}}BGP memory consumption during the *Internet in global routing table* test{{</cc>}}
```
PE-A#sh ip bgp sum
BGP router identifier 172.16.0.1, local AS number 65000
BGP table version is 1, main routing table version 1
186883 network entries using 27658684 bytes of memory
186883 path entries using 11960512 bytes of memory
34942/0 BGP path/bestpath attribute entries using 4472576 bytes of memory
31632 BGP AS-PATH entries using 1555798 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 45647570 total bytes of memory
BGP activity 186883/0 prefixes, 186883/0 paths, scan interval 60 secs

Neighbor    V     AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.17.0.2   4  65100  186889       4        1    0    0 00:00:57   186883
```

{{<note>}}
BGP uses several memory structures to store the BGP table:

-   *Network entries* table (IP prefixes)
-   *Path entries* table (BGP paths)
-   *Path attribute entries* (Attributes associated with BGP paths)
-   *AS-Path entries* (unique AS-paths)
{{</note>}}

The memory consumption per BGP prefix obviously depends on the path attributes associated with the prefix (example: BGP communities), AS-path lengths, and number of unique AS-paths (our table had over 186,000 prefixes and a bit over 31,000 unique AS paths). In our case, the average memory consumption was a bit more than 244 bytes per BGP prefix.

Interestingly, the **show memory alloc total** command revealed BGP was not the largest memory consumer; IP routing table and FIB table have consumed more memory than the BGP table.

{{<cc>}}Largest memory consumers during the *Internet in global routing table* test{{</cc>}}
```
PE-A#sh mem alloc total 
               Head   Total(b)    Used(b)    Free(b)  Lowest(b) Largest(b)
Processor  64FB4E00  402958764  193812292  209146472  209100168  201632172
      I/O   E000000   33554432    3126436   30427996   30419888   30417180
Transient  7D000000   16777216     136332   16640884   16640884   16640852

Allocator PC Summary for: Processor

    PC          Total   Count  Name
0x60D6E524   37931664    1154  IP primary NDB 
0x6026C57C   29317836     447  IPv4 Unicast ne
0x61B4A978   25585788     760  CEF: fib
0x60D6E030   15274128    1519  IP PRIMARY RDB 
0x6026C4C0   13511128     206  BGP IPv4 Unicas
0x606C2970   11215204      45  Init
0x61BF5E20    9966704     302  TAL: MTRIE n08
0x630CE374    5955036    2038  IP routing tabl
0x630CE344    5937504    2032  IP routing tabl
0x60214F14    5247040      80  BGP attr chunk
0x60213E58    2266348      90  BGP (2) attr
0x62C61A4C    2089156     253  Process Stack
0x626E4AC0    1937628       2  RMON packet pool
0x628454AC    1463756     857  *Packet Header*
0x62845504    1258296     152  *Packet Data*
```

Average per-route memory consumption, calculated as the difference between free memory before and after the test divided by the number of prefixes: \~820 bytes per prefix.

### Internet in a VRF

For the second test, I configured the EBGP session with *bgp_simple* in a VRF:

{{<cc>}}Internet in a VRF{{</cc>}}
```
ip vrf Internet
 rd 65000:1
 route-target export 65000:1
 route-target import 65000:1
!
interface FastEthernet0/0
 ip vrf forwarding Internet
 ip address 10.17.0.1 255.255.255.0
!
router bgp 65000
 bgp log-neighbor-changes
 !
 address-family ipv4 vrf Internet
  neighbor 10.17.0.2 remote-as 65100
  neighbor 10.17.0.2 activate
 exit-address-family
```

Here are the relevant printouts (this time *bgp_simple* managed to send 196,074 prefixes from the same file containing 200,000 prefixes):

{{<cc>}}Free memory prior to the *Internet in a VRF* test{{</cc>}}
```
PE-A#sh mem free
               Head   Total(b)    Used(b)    Free(b)  Lowest(b) Largest(b)
Processor  64FB4E00  402960204   41474912  361485292  361465196  352628556
      I/O   E000000   33554432    3137124   30417308   30417308   30414684
Transient  7D000000   16777216       5156   16772060   16772032   16772028
```

{{<cc>}}BGP memory consumption in the *Internet in a VRF* test{{</cc>}}
```
PE-A#sh ip bgp vpnv4 vrf Internet sum
BGP router identifier 172.16.0.1, local AS number 65000
BGP table version is 196075, main routing table version 196075
196074 network entries using 32940432 bytes of memory
196074 path entries using 12548736 bytes of memory
71878/35939 BGP path/bestpath attribute entries using 9775408 bytes of memory
32494 BGP AS-PATH entries using 1599258 bytes of memory
1 BGP extended community entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 56863858 total bytes of memory
BGP activity 196074/0 prefixes, 196074/0 paths, scan interval 60 secs

Neighbor    V     AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.17.0.2   4  65100  196084       8   196075    0    0 00:02:14   196074
```

{{<cc>}}Largest memory consumers in the *Internet in a VRF* test{{</cc>}}
```
PE-A#sh mem alloc totals 
               Head   Total(b)    Used(b)    Free(b)  Lowest(b) Largest(b)
Processor  64FB4E00  402958604  215429140  187529464  187485516  184854796
      I/O   E000000   33554432    3128932   30425500   30417392   30414684
Transient  7D000000   16777216     136332   16640884   16640884   16640852

Allocator PC Summary for: Processor

    PC          Total   Count  Name
0x60D6E524   39820880    1212  IP primary NDB 
0x6026C57C   34696052     529  VPNv4 Unicast n
0x61B4A978   26805108     796  CEF: fib
0x60D6E030   16032940    1595  IP PRIMARY RDB 
0x6026C4C0   14167008     216  BGP VPNv4 path-
0x60214F14   11281136     172  BGP attr chunk
0x606C2970   11215204      45  Init
0x61BF5E20   10428632     316  TAL: MTRIE n08
0x630CE374    6323208    2164  IP routing tabl
0x630CE344    5972592    2044  IP routing tabl
0x60213E58    2338592      94  BGP (1) attr
0x602A77B4    2198940      67  BGP TX attr top
0x62C61A4C    2083104     252  Process Stack
0x626E4AC0    1937628       2  RMON packet pool
0x628454AC    1468880     860  *Packet Header*
0x62845504    1258296     152  *Packet Data*
0x6021486C    1068624     349  BGP attrlist-ch
0x602158A8    1063712     348  BGP attrlist-ch
```

Average memory consumption:

-   \~290 bytes per BGP table entry (increase of 45 bytes per prefix or 18%)
-   \~890 bytes total per IP prefix (increase of \~70 bytes per prefix or 8%)

### Internet in a VRF with MPLS/VPN Route Replication

Finally, I configured another VRF on the same PE-router and used the *overlapping VPN* design (different route distinguishers and common route target) to leak Internet routes into a customer VRF:

{{<cc>}}Additional configuration on the PE-router{{</cc>}}
``` code
PE-A#sh run vrf Customer
Building configuration...

Current configuration : 95 bytes
ip vrf Customer
 rd 65000:2
 route-target export 65000:1
 route-target import 65000:1
```

As expected, both BGP table size and total memory consumption increased significantly due to duplicate entries in the BGP table and duplicate FIBs (each VRF has its own FIB).

{{<cc>}}BGP memory consumption with route leaking between Internet and Customer VRF{{</cc>}}
``` code
PE-A#sh ip bgp vpnv4 all sum
BGP router identifier 172.16.0.1, local AS number 65000
BGP table version is 392149, main routing table version 392149
392148 network entries using 65880864 bytes of memory
392148 path entries using 25097472 bytes of memory
71878/35939 BGP path/bestpath attribute entries using 9775408 bytes of memory
32494 BGP AS-PATH entries using 1599258 bytes of memory
1 BGP extended community entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 102353026 total bytes of memory
BGP activity 392148/0 prefixes, 392148/0 paths, scan interval 60 secs

Neighbor    V     AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.17.0.2   4  65100  196100      26   392149    0    0 00:07:40   196074
```

{{<cc>}}Total memory consumption with route leaking between Internet and Customer VRF{{</cc>}}
``` code
PE-A#sh mem alloc total
                Head  Total(b)    Used(b)    Free(b)  Lowest(b) Largest(b)
Processor  64FB4E00  402957004  374350796   28606208   28597336   17081036
      I/O   E000000   33554432    3128932   30425500   30417392   30414684
Transient  7D000000   16777216     136332   16640884   16640884   16640852

Allocator PC Summary for: Processor

    PC          Total   Count  Name
0x60D6E524   79605176    2424  IP primary NDB 
0x6026C57C   69392104    1058  VPNv4 Unicast n
0x61B4A978   53562408    1586  CEF: fib
0x60D6E030   32053992    3188  IP PRIMARY RDB 
0x6026C4C0   28334016     432  BGP VPNv4 path-
0x61BF5E20   20923268     634  TAL: MTRIE n08
0x630CE344   12243204    4190  IP routing tabl
0x630CE374   12219836    4182  IP routing tabl
0x60214F14   11281136     172  BGP attr chunk
0x606C2970   11215204      45  Init
0x602A77B4    4365060     133  BGP TX attr top
0x60213E58    2338592      94  BGP (1) attr
0x62C61A4C    2083104     252  Process Stack
0x626E4AC0    1937628       2  RMON packet pool
0x630CE1F0    1700604     582  IP routing tabl
0x628454AC    1468880     860  *Packet Header*
0x62845504    1258296     152  *Packet Data*
0x6021486C    1068624     349  BGP attrlist-ch
0x602158A8    1063712     348  BGP attrlist-ch
```

Average memory consumption with two VRFs carrying Internet routes:

-   \~520 bytes per BGP table entry (increase of \~230 bytes or \~80%)
-   Total \~1700 bytes per IP prefix (increase of \~810 bytes per prefix or over 90%)


{{<next-in-series page="/posts/2013/02/internet-in-vrf-and-lfib-explosion.md" />}}