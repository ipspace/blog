---
date: 2010-06-28 06:30:00.005000+02:00
dmvpn_tag: quirk
tags:
- DMVPN
- security
- IP routing
title: uRPF Violation Logging Is Not Working on 12.4T
url: /2010/06/urpf-violation-logging-not-working-on/
---
One of the scenarios I'm discussing in the [*DMVPN webinar*](http://www.ipspace.net/DMVPN) is redundant DMVPN network with two ISPs. It's not a particularly complex setup, unless the ISPs decide to deploy anti-spoofing filters (more precisely: unicast RPF checks) in which case it becomes crucially important which outbound interface you use for your DMVPN tunnel.

Anyhow, I was trying to make the whole thing work in a lab and it was repeatedly failing, so I decided to log uRPF violations. According to the documentation, it's a piece of cake:
<!--more-->
-   Define an ACL that denies and logs packets
-   Use the ACL in **ip verify unicast source** interface configuration command.

Sounds simple. I've used these configuration commands:

``` code
interface Serial2/3
 description Link to R2
 ip address 10.0.8.13 255.255.255.252
 ip verify unicast source reachable-via rx 199
 encapsulation ppp
 no peer neighbor-route
!
access-list 199 deny   ip any any log
```

It worked like a charm in 15.0(1)M, my *Internet* router generated lots of syslog messages similar to these:

``` code
%SEC-6-IPACCESSLOGP: list 199 denied udp 10.0.8.10(0) -> 10.0.8.2(0)
%SEC-6-IPACCESSLOGP: list 199 denied udp 10.0.8.10(0) -> 10.0.7.17(0)
```

12.4T? Accepts the ACL parameter and remains mum. Great inter-release consistency 🤷‍♂️
