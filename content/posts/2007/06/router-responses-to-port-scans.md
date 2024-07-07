---
date: 2007-06-12 08:03:00+02:00
tags:
- security
title: Router Responses to Port Scans
url: /2007/06/router-responses-to-port-scans/
---
Recently I was trying to figure out what the various port states reported by [Nmap](http://insecure.org/nmap/index.html) really mean. This is what\'s actually going on:

-   If a packet is intercepted by a router\'s access-list, the router sends back an ICMP *administratively prohibited* packet. This is reported as *filtered* port by Nmap (and probably as *stealth* port by some other scanners).
-   If you do a TCP SYN scan of a router and the scanned port is not active, the router sends back TCP RST packet. This is reported as *closed* port.
-   If you perform a UDP scan of a router, the router sends back ICMP *port unreachable* message if the UDP application is not active. This is reported by Nmap as *filtered* port (even though in most cases it should be equivalent to *closed* TCP port).
-   In some cases, the router simply doesn\'t reply to UDP scans (for example, if you scan the *discard* service). This is reported as *Open¦Filtered* (as the scanner cannot reliably determine whether the probe was dropped due to a filter or simply not replied to).

**Note:** In any case, UDP scans are way more unreliable than TCP scans due to connectionless nature of UDP.
<!--more-->
Below you\'ll find the debugging outputs for the most common conditions:

#### Successful TCP scan

Debugged with **debug ip tcp packet**

```
tcp0: I LISTEN 172.16.10.34:49620 172.16.0.1:80 seq 2116160324
OPTS 4 SYN WIN 1024
tcp0: O SYNRCVD 172.16.10.34:49620 172.16.0.1:80 seq 3992162774
OPTS 4 ACK 2116160325 SYN WIN 4128
tcp0: I SYNRCVD 172.16.10.34:49620 172.16.0.1:80 seq 2116160325
RST WIN 0
```

#### TCP scan of a closed port

Debugged with **debug ip tcp packet**

```
tcp0: I LISTEN 172.16.10.34:50434 172.16.0.1:80 seq 1431055709
OPTS 4 SYN WIN 1024
TCP: sent RST to 172.16.10.34:50434 from 172.16.0.1:80
```

#### TCP scan blocked by an access-list

Debugged with **debug ip icmp**

```
ICMP: dst (172.16.0.1) administratively prohibited unreachable sent to 172.16.10.34
```

#### UDP scan of an unreachable port

Debugged with **debug ip udp** and **debug ip icmp**

```
UDP: rcvd src=172.16.10.34(37312), dst=172.16.0.1(8), length=8
ICMP: dst (172.16.0.1) port unreachable sent to 172.16.10.34
```
