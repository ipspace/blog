---
title: "State of LDPv6 and 6PE"
date: 2023-01-12 07:11:00
tags: [ IPv6, MPLS, segment routing ]
---
One of my readers successfully deployed LDPv6 in their production network:

> We are using LDPv6 since we started using MPLS with IPv6 because I was used to OSPF/OSPFv3 in dual-stack deployments, and it simply worked.

Not everyone seems to be sharing his enthusiasm:

> Now some consultants tell me that they know no-one else that is using LDPv6. According to them "everyone" is using 6PE and the future of LDPv6 is not certain.
<!--more-->
I would believe that the future of LDPv6 is uncertain because the vendors are furiously pushing segment routing, be it as a control-plane addition to MPLS data plane or as a completely new IPv6-based data plane.

However, let's start with the basics. If plan to use IPv4+IPv6 throughout your network, and already use LDP, then LDPv6 is the natural way to go. However:

* While you can run LDPv6 on Junos, IOS XR, and Nokia/ALU[^MP], there's still no LDPv6 on Arista EOS or Cisco IOS XE ([more details](https://2021.internetsummit.africa/images/ais20-slides/14-sept/9-ais20-ldpv6-realworld.pdf))
* [LDP/IGP interactions are tricky](https://blog.ipspace.net/2011/11/ldp-igp-synchronization-in-mpls.html), and introducing LDPv6 will more than double your headaches -- now you'll have to deal with OSPF/LDP and OSPFv3/LDPv6 interactions.

6PE is an obvious alternative, and since L3VPN and EVPN often cannot use IPv6 next hops, it might still make sense to stay with an IPv4-only core transport network if you plan to offer more than simple IPv4/IPv6 transport. 6PE is also supported on a wider variety of platforms than LDPv6.

In greenfield networks, SR-MPLSv6[^SRA] would be a [viable alternative to LDPv6](https://blog.ipspace.net/2021/05/segment-routing-mpls-bgp-free-core.html), assuming it's supported by the platforms you're interested in[^SRS]. It would also simplify your protocol stack, particularly if you use IS-IS as the routing protocol.

Finally, if you need an excuse to [burn way too much money replacing still-working gear with the latest gizmos](https://blog.ipspace.net/2022/09/greenfield-sr-mpls-srv6.html) while ensuring job security for the next decade or so, you could decide to go for an IPv6-only network implementing all services with SRv6. I wish you plenty of luck, and would love to hear how well it worked out for you. 

[^MP]: At least we did make some progress since I [last wrote about LDPv6](https://blog.ipspace.net/2009/11/who-needs-ipv6.html) in 2009.

[^SRA]: Or however we should write that combo of acronyms

[^SRS]: According to _netlab_ SR-MPLS implementations, Arista EOS, Junos, Nokia SR Linux and Nokia SR OS support IPv6 SID while Cisco IOS XE does not.
