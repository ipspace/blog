---
date: 2017-01-26 08:48:00+01:00
ospf_tag: fa
tags:
- design
- OSPF
title: 'OSPF Forwarding Address YAK: Take 2'
url: /2017/01/ospf-forwarding-address-yak-take-2.html
---
In my initial [OSPF Forwarding Address blog post](/2017/01/ospf-forwarding-address-yet-another.html), I described a common Forwarding Address (FA) use case (at least as preached on the Internet): two ASBRs connected to a single external subnet with route redistributing configured only on one of them.

That design is clearly broken from the reliability perspective, but are there other designs where OSPF FA might make sense?
<!--more-->
Here's another more convoluted design: two ASBRs are connected to the same external subnet implemented with Metro Ethernet. One ASBR has a 1 Gbps connection to the Metro Ethernet service; the other one has a 100 Mbps connection.

Fixing the errors of the previous broken design we're running BGP on both ASBRs and redistributing BGP routes into OSPF on both of them. We have full redundancy, but suboptimal forwarding: C1 has two equal-cost paths to the external destination, while in reality, one of them has 10 times less bandwidth than the other one.

{{<figure src="/2017/01/s550-OSPF_FA_BW_1.png">}}

Here are the relevant parts of the OSPF topology database and IP routing table on C1:

{{<cc>}}OSPF Type-5 LSAs on C1 {{</cc>}}
``` code
C1#show ip ospf data external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

    Type-5 AS External Link States

  LS age: 40
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

  LS age: 25
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.0.2 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000002
  Checksum: 0x8D64
  Length: 36
  Network Mask: /32
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 1
  Forward Address: 0.0.0.0
  External Route Tag: 65001
```

{{<cc>}}IP Routing Table on C1{{</cc>}}

``` code
C1#show ip route 192.168.0.2
Routing entry for 192.168.0.2/32
  Known via "ospf 1", distance 110, metric 1
  Tag 65001, type extern 2, forward metric 1
  Last update from 10.0.128.6 on GigabitEthernet0/2, 00:00:47 ago
  Routing Descriptor Blocks:
    10.0.128.6, from 192.168.0.4, 00:00:47 ago, via GigabitEthernet0/2
      Route metric is 1, traffic share count is 1
      Route tag 65001
  * 10.0.128.1, from 192.168.0.1, 00:01:01 ago, via GigabitEthernet0/1
      Route metric is 1, traffic share count is 1
      Route tag 65001
```

Time for [another MacGyver stunt](/2013/08/temper-your-macgyver-streak.html):

-   Enable OSPF on the (external) Metro Ethernet LAN that connects our OSPF network with a third-party router (yes, it's a Really Bad Idea from the security perspective);
-   Set OSPF costs (or bandwidth) correctly;
-   Hope that ASBRs start advertising Forwarding Address in Type-5 LSA and route selection of internal OSPF routes makes sure only the faster path is used.

{{<figure src="/2017/01/s550-OSPF_FA_BW_2.png">}}

It actually works:

{{<cc>}}IP Routing Table on C1 after enabling OSPF on external subnet{{</cc>}}
``` code
C1#show ip route 192.168.0.2
Routing entry for 192.168.0.2/32
  Known via "ospf 1", distance 110, metric 1
  Tag 65001, type extern 2, forward metric 2
  Last update from 10.0.128.1 on GigabitEthernet0/1, 00:01:13 ago
  Routing Descriptor Blocks:
  * 10.0.128.1, from 192.168.0.4, 00:01:13 ago, via GigabitEthernet0/1
      Route metric is 1, traffic share count is 1
      Route tag 65001
```

We can also observe another *interesting* (as in *how the **** did we ever get here*) behavior:

-   While both ASBRs advertised the Type-5 LSA before, after enabling OSPF on the external interface, only one of them advertises Type-5 LSA

{{<cc>}}Type-5 LSA is advertised only by E2{{</cc>}}
``` code
C1#show ip ospf data external

            OSPF Router with ID (192.168.0.3) (Process ID 1)

    Type-5 AS External Link States

  LS age: 272
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.0.2 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000003
  Checksum: 0x16CE
  Length: 36
  Network Mask: /32
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 1
  Forward Address: 10.0.0.2
  External Route Tag: 65001
```

-   In our network, the Type-5 LSA is advertised by the ASBR that is never used for packet forwarding toward the external destination (I am positive there's a section somewhere in [OSPF RFC](https://tools.ietf.org/html/rfc2328) talking about higher ASBR router ID).

Hooray, we just saved the memory occupied by one Type-5 LSA, and yet again increased the complexity of the protocol.

{{<note warn>}}Not only is this behavior fun to troubleshoot, try figuring out what happens when E2 crashes, resulting in loss of light on P2P links but no detectable change on the Metro Ethernet side. I have a wonderful explanation, but the [margins of this blog post are not wide enough for it](https://en.wikipedia.org/wiki/Fermat's_Last_Theorem), so it's [left as an exercise for the reader](http://catb.org/jargon/html/E/exercise--left-as-an.html).{{</note>}}

Guess what: we didn't need OSPF FA in the first place. The correct design would be to increase OSPF external metrics on E2 and use External Type 1 (E1) metrics so that the other OSPF routers would consider the total cost (internal + external) toward the external destinations. Alas, that's not how real-life problems are solved (at least not in the CCIE lab).
