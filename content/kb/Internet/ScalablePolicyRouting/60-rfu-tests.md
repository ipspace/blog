title: Ready-for-Use Tests

To test the correct operation of the policy routing in your network, you should perform at least the following tests:

*	Traceroute from sample clients at various remote sites toward all classes of servers (in our scenario, a server in the Legacy LAN and a server in the Web LAN).
*	Traceroute from the servers back to the clients.

WARN: The record route option available in the IOS **traceroute** command does not help you, as it records forward route (which you test with the traceroute command anyway), not the return route.

The tests should be performed under all possible link conditions (both links active, failure of the primary link, failure of the backup link).

The first set of the tests, executed between a client on site A and the legacy (TN3270) and web (MAIL) servers are displayed in the following printout:

```
Client.Site-A#traceroute TN3270

Type escape sequence to abort.
Tracing the route to TN3270 (10.0.20.20)

  1 Site-A (192.168.1.1) 4 msec 4 msec 4 msec
  2 Serial-1-0-100.CoreFR (10.0.8.1) 8 msec 8 msec 8 msec
  3 Fast-0-0.Legacy (10.0.10.3) 16 msec 12 msec 12 msec
  4 TN3270 (10.0.20.20) 20 msec *  36 msec
Client.Site-A#traceroute MAIL

Type escape sequence to abort.
Tracing the route to MAIL (10.0.21.25)

  1 Site-A (192.168.1.1) 8 msec 8 msec 4 msec
  2 Tunnel-0.CoreInet (10.0.11.1) 12 msec 8 msec 12 msec
  3 Fast-0-0.Web (10.0.10.4) 8 msec 8 msec 16 msec
  4 MAIL (10.0.21.25) 36 msec *  28 msec
```
CAPTION: Traceroute executed from a client on site A toward various servers

Similar tests executed from the two servers toward the client on site A are shown below:

```
TN3270#traceroute Client.Site-A

Type escape sequence to abort.
Tracing the route to Client.Site-A (192.168.1.100)

  1 Fast-0-1.Legacy (10.0.20.1) 8 msec 4 msec 4 msec
  2 Fast-0-0.CoreFR (10.0.10.2) 12 msec 12 msec 8 msec
  3 FR-1-0-100.Site-A (10.0.8.2) 8 msec 8 msec 12 msec
  4 Client.Site-A (192.168.1.100) 20 msec *  40 msec

Mail#traceroute Client.Site-A

Type escape sequence to abort.
Tracing the route to Client.Site-A (192.168.1.100)

  1 Fast-0-1.Web (10.0.21.1) 8 msec 4 msec 4 msec
  2 Fast-0-0.CoreInet (10.0.10.1) 12 msec 8 msec 8 msec
  3 Tunnel-0.Site-A (10.0.11.2) 16 msec 16 msec 16 msec
  4 Client.Site-A (192.168.1.100) 24 msec *  40 msec
```
CAPTION: Traceroute executed toward a client on site A

## Summary

Most network designers and implementers try to avoid policy routing, as its common implementation requires a complex mix of access-lists and route-maps that have to be deployed on a hop-by-hop basis. In reality, distance vector routing protocols can be used to implement common policy routing requirements in enterprise networks where a set of applications should prefer a different subset of links than other applications.

Routing protocol based policy routing should be implemented (if at all possible) with BGP, as it gives you the richest set of tools to use to influence the route selection policy. EIGRP is a viable alternative (you can manipulate the delay portion of the metric for each individual IP prefix), with RIP being the solution of last resort. You cannot implement the same mechanisms with any link state routing protocol, as you cannot increase the link cost for individual IP prefixes.
