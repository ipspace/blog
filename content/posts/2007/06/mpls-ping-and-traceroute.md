---
date: 2007-06-21 17:25:00+02:00
tags:
- MPLS
- network management
title: MPLS Ping and Traceroute
url: /2007/06/mpls-ping-and-traceroute/
---
One of the hardest troubleshooting problems within an MPLS VPN network has always been finding a broken LSP. While you could (in theory) use the IP **ping** or **traceroute** (assuming all hops support ICMP extensions for MPLS), the results are not always reliable... and interpreting them is not so easy. For example, after I\'ve disabled LDP on an interface with the **no mpls ip** configuration command, the routers in the LSP path still reported outgoing MPLS labels in ICMP replies for a few seconds (until the LDP holddown timer expired on both ends of the link).

As a side note, would you deduce from the printout that the break in the LSP path happened on the router with the IP address 192.168.201.1?
<!--more-->
``` {.code}
ro#trace ip 1.0.0.1
Tracing the route to 1.0.0.1

  1 192.168.201.1 [MPLS: Label 22 Exp 0] 204 msec 200 msec 212 msec
  2 192.168.201.6 [MPLS: Label 16 Exp 0] 112 msec 112 msec 116 msec
  3 192.168.0.6 56 msec *  60 msec
ro#trace ip 1.0.0.1
Tracing the route to 1.0.0.1

  1 192.168.201.1 [MPLS: Label 22 Exp 0] 56 msec 60 msec 56 msec
  2 192.168.201.6 56 msec 56 msec 56 msec
  3 192.168.0.6 56 msec *  56 msec
```

The MPLS ping and traceroute commands, introduced in IOS release 12.0(27)S and integrated in mainstream IOS release 12.4(6)T (at least five years too late in my humble opinion) address this problem: they both use IP packets that are [not capable of being IP-switched](http://www.cisco.com/en/US/products/sw/iosswrel/ps1829/products_feature_guide09186a00801eb054.html#wp1086556) and thus report the exact failure spot.

In our scenario, MPLS ping and traceroute correctly identified the problem (unlabeled output interface) and the MPLS traceroute also provides the correct IP address of the offending router.

``` {.code}
ro#ping mpls ip 1.0.0.1 255.255.255.255
Sending 5, 100-byte MPLS Echos to 1.0.0.1/32,
     timeout is 2 seconds, send interval is 0 msec:

Codes: '!' - success, 'Q' - request not sent, '.' - timeout,
  'L' - labeled output interface, 'B' - unlabeled output interface,
  'D' - DS Map mismatch, 'F' - no FEC mapping, 'f' - FEC mismatch,
  'M' - malformed request, 'm' - unsupported tlvs, 'N' - no label entry,
  'P' - no rx intf label prot, 'p' - premature termination of LSP,
  'R' - transit router, 'I' - unknown upstream index,
  'X' - unknown return code, 'x' - return code 0

Type escape sequence to abort.
BBBBB
Success rate is 0 percent (0/5)
ro#trace mpls ip 1.0.0.1 255.255.255.255
Tracing MPLS Label Switched Path to 1.0.0.1/32, timeout is 2 seconds

Codes: '!' - success, 'Q' - request not sent, '.' - timeout,
  'L' - labeled output interface, 'B' - unlabeled output interface,
  'D' - DS Map mismatch, 'F' - no FEC mapping, 'f' - FEC mismatch,
  'M' - malformed request, 'm' - unsupported tlvs, 'N' - no label entry,
  'P' - no rx intf label prot, 'p' - premature termination of LSP,
  'R' - transit router, 'I' - unknown upstream index,
  'X' - unknown return code, 'x' - return code 0

Type escape sequence to abort.
  0 192.168.201.2 MRU 1500 [Labels: 22 Exp: 0]
B 1 192.168.201.1 MRU 1504 [No Label] 64 ms
```

After the problem has been fixed, both commands report successful tests:

``` {.code}
ro#trace mpls ip 1.0.0.1 255.255.255.255
Tracing MPLS Label Switched Path to 1.0.0.1/32, timeout is 2 seconds

Codes: '!' - success, 'Q' - request not sent, '.' - timeout,
  'L' - labeled output interface, 'B' - unlabeled output interface,
  'D' - DS Map mismatch, 'F' - no FEC mapping, 'f' - FEC mismatch,
  'M' - malformed request, 'm' - unsupported tlvs, 'N' - no label entry,
  'P' - no rx intf label prot, 'p' - premature termination of LSP,
  'R' - transit router, 'I' - unknown upstream index,
  'X' - unknown return code, 'x' - return code 0

Type escape sequence to abort.
  0 192.168.201.2 MRU 1500 [Labels: 22 Exp: 0]
I 1 192.168.201.1 MRU 1500 [Labels: 16 Exp: 0] 68 ms
I 2 192.168.201.6 MRU 1504 [Labels: implicit-null Exp: 0] 140 ms
! 3 192.168.0.6 112 ms
ro#ping mpls ip 1.0.0.1 255.255.255.255
Sending 5, 100-byte MPLS Echos to 1.0.0.1/32,
     timeout is 2 seconds, send interval is 0 msec:

Codes: '!' - success, 'Q' - request not sent, '.' - timeout,
  'L' - labeled output interface, 'B' - unlabeled output interface,
  'D' - DS Map mismatch, 'F' - no FEC mapping, 'f' - FEC mismatch,
  'M' - malformed request, 'm' - unsupported tlvs, 'N' - no label entry,
  'P' - no rx intf label prot, 'p' - premature termination of LSP,
  'R' - transit router, 'I' - unknown upstream index,
  'X' - unknown return code, 'x' - return code 0

Type escape sequence to abort.
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 100/103/104 ms
```
