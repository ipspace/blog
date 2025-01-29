---
title: "The Curious Case of the BGP Connect State"
date: 2025-01-30 07:55:00+0100
tags: [ BGP ]
---
I got this question from Paul:

> Have you ever seen a BGP peer in the "Connect" state? In 20 years, I have never been able to see or reproduce this state, nor any mention in a debug/log. I am starting to believe that all the documentation is BS, and this does not exist.

The BGP Finite State Machine (FSM) (at least the one [defined in RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271#section-8) and [amended in RFC 9687](https://datatracker.ietf.org/doc/html/rfc9687#name-changes-to-the-fsm)) is "a bit" hard to grasp but the basics haven't changed from the [ancient days of RFC 1771](https://datatracker.ietf.org/doc/html/rfc1771#autoid-31):
<!--more-->
* When a router decides to connect to a BGP neighbor, it sends a TCP SYN and transitions from the Idle to the Connect state.
* Once the TCP session is established[^TCPEST], the router sends the BGP OPEN message and moves to the OpenSent state
* If the TCP session cannot be established, the router transitions to the Active state, where it waits for an incoming TCP session (transitioning to OpenSent) or for the ConnectRetry timer (transitioning to Connect)

[^TCPEST]: The router receives SYN/ACK confirmation for an outgoing TCP session or an ACK confirmation for an incoming TCP session.

{{<note info>}}
You will never see the Connect state on Cisco IOS. Cisco implemented BGP in the days of the (original) RFC 1105 when the [state machine](https://datatracker.ietf.org/doc/html/rfc1105#autoid-10) did not have Connect and Active states. The Connect state was [added in RFC 1163](https://datatracker.ietf.org/doc/html/rfc1163#autoid-20), but Cisco never changed the printouts.

To see the states of the recent BGP FSMs, use FRR or Arista EOS (the easiest ones to get started in a virtual lab).
{{</note>}}

Based on the above, how could we keep a BGP speaker in the Connect state long enough to observe it? Not configuring a BGP neighbor on one side of the BGP session doesn't help -- most routers getting an incoming TCP SYN packet would [immediately respond with an RST](https://blog.ipspace.net/2023/10/reject-unknown-bgp-session/) (with a [notable depressing exception](https://blog.ipspace.net/2023/11/open-bgp-daemons/)). Configuring an EBGP neighbor with an invalid IP address also doesn't bring us much -- the ARP/ND processing would fail pretty quickly, bringing down the TCP session.

To get stuck in the Connect state for an observable amount of time, we need the TCP SYN packet to disappear without a trace. Here are some ideas on how to get that done:

* Configure GTSM on one end of the EBGP session ([does not work on some platforms](https://blog.ipspace.net/2023/11/bgp-ttl-security-shortcomings/))
* Configure an IBGP neighbor (or a multi-hop EBGP neighbor) with a bogus IP address.
* Break the end-to-end path between IBGP neighbors (for example, mess up an MPLS LSP)
* Drop BGP packets with an ACL that does not generate ICMP unreachables.

Next, sit back and enjoy watching the BGP Connect state ;)
