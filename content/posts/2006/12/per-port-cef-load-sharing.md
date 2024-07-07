---
date: 2007-01-14 15:38:00+01:00
tags:
- CEF
- load balancing
title: Per-Port CEF Load Balancing
url: /2006/12/per-port-cef-load-sharing/
---
In designs with very low number of IP hosts, no per-destination load-sharing algorithm will work adequately. Consider, for example, an extranet design where a large number of IP hosts are NAT-ed to a single IP address which then accesses a single remote server.

{{<figure src="/2006/12/LoadSharing_2.jpg">}}

In this design, all the traffic flows between a single pair of IP addresses, making per-destination load-sharing unusable.
<!--more-->
Cisco has addressed this problem in IOS release 12.4(11)T with *per-port CEF load sharing*, which extends the [CEF hashing function](/2006/10/cef-load-sharing-details/) to include source and/or destination TCP or UDP port.

The global configuration command that enables per-port CEF load-sharing is **ip cef load-sharing algorithm \[ include-ports \[source\] \[dest\] \] *seed***. To test it, use the **show ip cef exact-route** command, which now supports source and destination port numbers. For example:

``` {.code}
a1(config)#ip cef load-sharing algorithm include-ports source dest 22

a1#show ip cef exact-route 10.0.0.10 src-port 35 192.168.0.2 dest-port 80
10.0.0.10       -> 192.168.0.2    : Serial0/0/0.100 (next hop 172.16.1.2)
a1#show ip cef exact-route 10.0.0.10 src-port 36 192.168.0.2 dest-port 80
10.0.0.10       -> 192.168.0.2    : Serial0/0/0.200 (next hop 172.16.1.6)
a1#show ip cef exact-route 10.0.0.10 src-port 37 192.168.0.2 dest-port 80
10.0.0.10       -> 192.168.0.2    : Serial0/0/0.100 (next hop 172.16.1.2)
```
