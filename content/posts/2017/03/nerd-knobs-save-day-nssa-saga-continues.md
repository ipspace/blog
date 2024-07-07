---
date: 2017-03-02 13:43:00+01:00
ospf_tag: areas
tags:
- OSPF
title: 'Nerd Knobs Save the Day: NSSA Saga Continues'
url: /2017/03/nerd-knobs-save-day-nssa-saga-continues/
pre_scroll: True
---
Remember the [OSPF NSSA Forwarding Address](/2017/02/the-unintended-consequences-of-nssa/) kludge and [its consequences](/2017/02/why-ospf-needs-forwarding-address-with/)? Let's figure out whether the nerd knobs available in Cisco IOS can save the day.

**TL&DR**: Don't use OSPF areas if you can avoid them. Don't use NSSA areas.
<!--more-->
### The OSPF Forwarding Address and NSSA Saga

This blog post is the last in a series of six blog posts, and the only reason I published it was a huge *Thank You* I got from one of my friends when we met at Cisco Live Berlin. He said, "*I forwarded your blog posts to a customer who planned on building a network using OSPF NSSA areas. They probably changed his mind.*"

So let's conclude the saga with a [MacGyver fix](/2013/08/temper-your-macgyver-streak/) -- a series of nerd knobs that have to be adjusted to make the network work. If this won't persuade you to stay away from NSSA areas, nothing will.

### Other Blog Posts in This Saga

You might want to read these blog posts before continuing:

-   [OSPF Forwarding Address -- Yet Another Kludge](/2017/01/ospf-forwarding-address-yet-another/)
-   [OSPF Forwarding Address -- Take 2](/2017/01/ospf-forwarding-address-yak-take-2/)
-   [Why OSPF Needs Forwarding Address with NSSA Areas](/2017/02/why-ospf-needs-forwarding-address-with/)
-   [The Unintended Consequences of NSSA Kludges](/2017/02/the-unintended-consequences-of-nssa/)
-   [More Thoughts on OSPF Forwarding Address](/2017/02/more-thoughts-on-ospf-forwarding-address/)

### Breaking the Network

As before, we'll start with what seems to be a perfectly designed network (trust me, [there's a snake in this paradise](/2017/02/why-ospf-needs-forwarding-address-with/)):

{{<figure src="/2017/03/s500-OSPF_NSSA_1.png">}}

As expected, C1 has two equal-cost paths to 192.168.1.0/24 and can reach 192.168.1.1:

{{<cc>}}Expected network behavior{{</cc>}}
``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/33] via 10.0.0.13, 00:00:21, GigabitEthernet0/2
                     [110/33] via 10.0.0.9, 00:00:21, GigabitEthernet0/1
C1#ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 2/4/7 ms
```

After we shut down the loopback interface on E1 (to emulate a broken design with no loopback interface on ASBR), C1 loses one of the paths to E1 but can still reach it. For a detailed explanation of this behavior, read the previous blog posts mentioned above.

{{<cc>}}C1 loses one path toward E1{{</cc>}}
``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/32] via 10.0.0.13, 00:00:07, GigabitEthernet0/2
C1#ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 2/4/7 ms
```

Finally, when the interface between A2 and E1 breaks down in a mysterious way (line protocol is up, but something on the link drops OSPF traffic), C1 has the route to 192.168.1.0/24 but can no longer reach 192.168.1.1

{{<cc>}}Traffic blackhole after the A2-E1 link failure{{</cc>}}
``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/32] via 10.0.0.13, 00:00:11, GigabitEthernet0/2
C1#ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
U.U.U
Success rate is 0 percent (0/5)
```

### Nerd Knobs Save the Day

Cisco IOS OSPF implementation has way too many nerd knobs, some of them violating OSPF standards to make your network work. We'll use two of them here.

The **area nssa translate type7 suppress-fa** knob disables the Forwarding Address propagation from type-7 to type-5 LSA. The backbone type-5 LSA is originated without the forwarding address (making it look like the external subnet is attached directly to ABR) and *with no OSPF cost adjustment*. From the SPF perspective, the cost to traverse the NSSA area is zero.

After configuring this feature on A1 and A2, the type-5 LSA observed on C1 has the same OSPF cost as before (E1 cost 30) but no forwarding address.

{{<cc>}}Type-5 LSA on C1{{</cc>}}
``` code
C1#show ip ospf data external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

Type-5 AS External Link States

  LS age: 20
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.1
  LS Seq Number: 80000002
  Checksum: 0xF749
  Length: 36
  Network Mask: /24
Metric Type: 1 (Comparable directly to link state metric)
MTID: 0
Metric: 30
Forward Address: 0.0.0.0
External Route Tag: 0
```

A change in forwarding address fixes the network. C1 can see a path to 192.168.1.0/24 going through A1 (10.0.0.9) -- remember that the A2-E1 link is still broken. It can also reach 192.168.1.1 (a major improvement).

{{<cc>}}Connectivity to 192.168.1.0/24 works{{</cc>}}
``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/31] via 10.0.0.9, 00:00:39, GigabitEthernet0/1
C1#ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 2/4/5 ms
```

However, once we fix the A2-E1 link C1 still sees only a single path to C1, this time through 10.0.0.13 (A2).

{{<cc>}}C1 sees a single path to 192.168.1.0/24{{</cc>}}
``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/31] via 10.0.0.13, 00:02:15, GigabitEthernet0/2
```

The reason for that unexpected behavior is quite simple: due to NSSA rules, a single ABR translates the type-7 LSA into type-5 LSA, and as we no longer have the forwarding address in type-5 LSA, routers in other OSPF areas don't know there are two equal-cost paths to E1.

When inspecting the type-5 LSAs in the backbone area, you can see that the type-5 LSA for 192.168.1.0/24 is no longer originated by 192.168.0.1 (A1) but by 192.168.0.4 (A2).

{{<cc>}}Type-5 LSA on C1{{</cc>}}
``` code
C1#show ip ospf data external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

Type-5 AS External Link States

  LS age: 170
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000001
  Checksum: 0xE757
  Length: 36
  Network Mask: /24
Metric Type: 1 (Comparable directly to link state metric)
MTID: 0
Metric: 30
Forward Address: 0.0.0.0
External Route Tag: 0
```

To fix that side effect we need yet another nerd knob: *always* translate type-7 LSAs into type-5 LSAs: **area 1 nssa translate type7 suppress-fa always**.

After the configuration change both A1 *and* A2 advertise type-5 LSA corresponding to the original type-7 LSA:

{{<cc>}}C1 has two type-5 LSAs in its OSPF database{{</cc>}}
``` code
C1#show ip ospf data external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

Type-5 AS External Link States

  LS age: 37
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.1
  LS Seq Number: 80000001
  Checksum: 0xF948
  Length: 36
  Network Mask: /24
Metric Type: 1 (Comparable directly to link state metric)
MTID: 0
Metric: 30
Forward Address: 0.0.0.0
External Route Tag: 0

  LS age: 221
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000001
  Checksum: 0xE757
  Length: 36
  Network Mask: /24
Metric Type: 1 (Comparable directly to link state metric)
MTID: 0
Metric: 30
Forward Address: 0.0.0.0
External Route Tag: 0
```

Not surprisingly, C1 has two equal-cost paths to 192.168.1.0.

``` code
C1#show ip route | sect 192.168.1.0
O E1  192.168.1.0/24 [110/31] via 10.0.0.13, 00:03:32, GigabitEthernet0/2
                     [110/31] via 10.0.0.9, 00:00:28, GigabitEthernet0/1
```

### Lesson Learned

You might fix networks using OSPF NSSA areas with nerd knobs that violate OSPF standards. They might come in handy if you have to fix an existing network, but just because they are there, you **SHOULD NOT** use them when designing a network. Try to stay away from OSPF areas, and don't use NSSA areas -- even though OSPF looks like a Swiss Army Knife, there are better tools to get the job done.

### Initial router configurations

Here are the relevant parts of router configurations in case you  want to rebuild the scenario in a test lab:

``` code
hostname C1
!
interface Loopback0
 ip address 192.168.0.3 255.255.255.255
 ip ospf 1 area 0
!
interface GigabitEthernet0/1
 description to A1
 ip address 10.0.0.10 255.255.255.252
 ip ospf 1 area 0
!
interface GigabitEthernet0/2
 description to A2
 ip address 10.0.0.14 255.255.255.252
 ip ospf 1 area 0
!
router ospf 1
```

``` code
hostname A1
!
interface Loopback0
 ip address 192.168.0.1 255.255.255.255
!
interface GigabitEthernet0/1
 description to C1
 ip address 10.0.0.9 255.255.255.252
 ip ospf 1 area 0
!
interface GigabitEthernet0/2
 description to E1
 ip address 10.0.0.5 255.255.255.252
 ip ospf 1 area 1
!
router ospf 1
 area 1 nssa
```

``` code
hostname A2
!
interface Loopback0
 ip address 192.168.0.4 255.255.255.255
!
interface GigabitEthernet0/1
 description to C1
 ip address 10.0.0.13 255.255.255.252
 ip ospf 1 area 0
!
interface GigabitEthernet0/2
 description to E1
 ip address 10.0.0.17 255.255.255.252
 ip ospf 1 area 1
!
router ospf 1
 area 1 nssa
```

``` code
hostname E1
!
interface Loopback0
 description Loopback
 ip address 192.168.0.2 255.255.255.255
 ip ospf 1 area 1
!
interface Loopback1
 ip address 192.168.1.1 255.255.255.0
!
interface GigabitEthernet0/1
 description to A1
 ip address 10.0.0.6 255.255.255.252
 ip ospf 1 area 1
!
interface GigabitEthernet0/2
 description to A2
 ip address 10.0.0.18 255.255.255.252
### ip access-group blockospf in ### use to block OSPF between A2 and E1
 ip ospf 1 area 1
!
router ospf 1
 area 1 nssa
 redistribute connected metric 30 metric-type 1 subnets
!
ip access-list extended blockospf
 deny   ospf any any
 permit ip any any
```
