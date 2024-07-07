---
date: 2023-05-25 06:43:00+00:00
netlab_tag: use
title: Inter-VRF DHCP Relaying with Redundant DHCP Servers
tags: [ DHCP ]
pre_scroll: True
series: [ dhcp-relay ]
---
Previous posts in this series covered numerous intricacies of DHCP relaying:

* [DHCP relaying principles](/2023/03/dhcp-relay-process/) described the basics
* In [Inter-VRFs relaying](/2023/03/netlab-vrf-dhcp-relay/) we figured out how a DHCP client reaches a DHCP server in another VRF without inter-VRF route leaking
* [Relaying in VXLAN segments](/2023/03/netlab-vxlan-dhcp-relay/) and [relaying from EVPN VRF](/2023/04/netlab-evpn-dhcp-relay/) applied those lessons to VXLAN/EVPN environment.
* [DHCP Relaying with Redundant DHCP Servers](/2023/04/dhcp-redundant-relay/) added relay- and server redundancy.

Now for the final bit of the puzzle: what if we want to do inter-VRF DHCP relaying with redundant DHCP servers?
<!--more-->
If you read the previous blog posts (carefully enough) you might have already noticed the gotcha:

* When relaying DHCP requests between VRFs, the DHCP relay acts as a DHCP server toward the client -- the DHCP server address in the DHCP OFFER or DHCP ACK replies is the IP address of the ingress interface of the DHCP relay.
* The DHCP server IP address in the DHCP REQUEST packet is used by the servers to figure out whether to complete the IP address allocation (and confirm it with DHCP ACK message) or abort the transaction and forget about it.
* That procedure obviously cannot work if the client doesn't know the actual IP address of the DHCP server. Now what?

It's time for another lab test...

### Lab Topology

We'll use the same lab topology we used in the [DHCP Relaying with Redundant DHCP Servers](/2023/04/dhcp-redundant-relay/) scenario but connect DHCP clients to a VRF (similar to the [Inter-VRFs relaying](/2023/03/netlab-vrf-dhcp-relay/) scenario).
<!--more-->
{{<figure src="/2023/05/evpn-dhcp-redundant-server.png" caption="Lab topology diagram">}}

{{<cc>}}Lab IPv4 addressing{{</cc>}}
```
  Interface                  IPv4 address  Description
================================================================================
srv1 (10.0.0.2/32)
  GigabitEthernet2            10.1.0.1/30  srv1 -> sw3

srv2 (10.0.0.3/32)
  GigabitEthernet2            10.1.0.5/30  srv2 -> sw3

sw1 (10.0.0.4/32)
  Ethernet1                   10.1.0.9/30  sw1 -> sw2
  Ethernet2                  10.1.0.13/30  sw1 -> sw3
  Vlan1000                  172.16.0.4/24  VLAN cv1 (1000) -> [cl_a,cl_b,sw2]

sw2 (10.0.0.5/32)
  Ethernet1                  10.1.0.10/30  sw2 -> sw1
  Ethernet2                  10.1.0.17/30  sw2 -> sw3
  Vlan1000                  172.16.0.5/24  VLAN cv1 (1000) -> [cl_a,sw1,cl_b]

sw3 (10.0.0.6/32)
  Ethernet1                   10.1.0.2/30  sw3 -> srv1
  Ethernet2                   10.1.0.6/30  sw3 -> srv2
  Ethernet3                  10.1.0.14/30  sw3 -> sw1
  Ethernet4                  10.1.0.18/30  sw3 -> sw2

cl_a (10.0.0.7/32)
  GigabitEthernet0/1        172.16.0.7/24  cl_a -> [sw1,cl_b,sw2]

cl_b (10.0.0.8/32)
  GigabitEthernet0/1        172.16.0.8/24  cl_b -> [cl_a,sw1,sw2]
```

You can [view the complete topology file](https://github.com/ipspace/netlab-examples/blob/master/DHCP/evpn-redundant-server/topology.yml) and [device configurations](https://github.com/ipspace/netlab-examples/tree/master/DHCP/evpn-redundant-server/config) in the *[netlab-examples](https://github.com/ipspace/netlab-examples)* repository.

### Finding DHCP Servers

The first few steps of this scenario are almost equivalent to the non-redundant inter-VRF DHCP relaying scenario ([complete server- and client logs](https://github.com/ipspace/netlab-examples/tree/master/DHCP/evpn-redundant-server/logs) are on GitHub)

* Client broadcasts a DHCP DISCOVER packet:

```
00:18:56: Temp IP addr: 0.0.0.0  for peer on Interface: GigabitEthernet0/1
00:18:56: Temp  sub net mask: 0.0.0.0
00:18:56:    DHCP Lease server: 0.0.0.0, state: 3 Selecting
00:18:56:    DHCP transaction id: 1BFE
00:18:56:    Lease: 0 secs,  Renewal: 0 secs,  Rebind: 0 secs
00:18:56:    Next timer fires after: 00:00:04
00:18:56:    Retry count: 1   Client-ID: cisco-5254.0015.f24f-Gi0/1
00:18:56:    Client-ID hex dump: 636973636F2D353235342E303031352E
00:18:56:                        663234662D4769302F31
00:18:56:    Hostname: cl_a
00:18:56: DHCP: SDiscover placed class-id option: 636973636F706E70
00:18:56: DHCP: SDiscover: sending 303 byte length DHCP packet
```

* Two copies of the DHCP DISCOVER packet are forwarded to each DHCP server (please note different `giaddr` addresses set to loopback interfaces of sw-1 and sw-2):

{{<cc>}}DHCP DISCOVER step on srv-1{{</cc>}}
```
00:18:57: DHCPD: Sending notification of DISCOVER:
00:18:57:   DHCPD: htype 1 chaddr 5254.0015.f24f
00:18:57:   DHCPD: circuit id 566c616e31303030
00:18:57:   DHCPD: giaddr = 10.0.0.4
00:18:57:   DHCPD: interface = GigabitEthernet2
00:18:57:   DHCPD: class id 636973636f706e70
00:18:57: DHCPD: DHCPDISCOVER received from client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 through relay 10.0.0.4.
00:18:57: DHCPD: Option 125 not present in the msg.
00:18:57: DHCPD: using received relay info.
...
00:18:57: DHCPD: Sending notification of DISCOVER:
00:18:57:   DHCPD: htype 1 chaddr 5254.0015.f24f
00:18:57:   DHCPD: circuit id 566c616e31303030
00:18:57:   DHCPD: giaddr = 10.0.0.5
00:18:57:   DHCPD: interface = GigabitEthernet2
00:18:57:   DHCPD: class id 636973636f706e70
00:18:57: DHCPD: DHCPDISCOVER received from client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 through relay 10.0.0.5.
00:18:57: DHCPD: Option 125 not present in the msg.
00:18:57: DHCPD: using received relay info.
```

* Both servers should reply with two DHCP offer message, one for each relayed packet, as you can see on the printout from *srv-1*. Please note how the *server-id-override* option is used to set the DHCP server IP address to the VLAN IP address of the DHCP relay:

```
00:18:57: DHCPD: Sending DHCPOFFER to client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 (172.16.0.6)
00:18:57: DHCPD: using server-id-override 172.16.0.4
00:18:57: DHCPD: Option 125 not present in the msg.
00:18:57: DHCPD: egress Interfce GigabitEthernet2
00:18:57: DHCPD: unicasting BOOTREPLY for client 5254.0015.f24f to relay 10.0.0.4.
...
00:18:57: DHCPD: Sending DHCPOFFER to client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 (172.16.0.6).
00:18:57: DHCPD: using server-id-override 172.16.0.5
00:18:57: DHCPD: Option 125 not present in the msg.
00:18:57: DHCPD: egress Interfce GigabitEthernet2
00:18:57: DHCPD: unicasting BOOTREPLY for client 5254.0015.f24f to relay 10.0.0.5.
```

### Selecting a DHCP Server

The DHCP client receives multiple DHCP OFFER replies. The first offer is accepted, and the client proceeds with a DHCP REQUEST message (still sent as a broadcast packet):

```
00:18:57: DHCP: Received a BOOTREP pkt
00:18:57: DHCP: Scan: Message type: DHCP Offer
00:18:57: DHCP: Scan: Client ID: cisco-5254.0015.f24f-Gi0/1
00:18:57: DHCP: Scan: Server ID Option: 172.16.0.4 = AC100004
00:18:57: DHCP: Scan: Lease Time: 86400
00:18:57: DHCP: Scan: Renewal time: 43200
00:18:57: DHCP: Scan: Rebind time: 75600
00:18:57: DHCP: Scan: Subnet Address Option: 255.255.255.0
00:18:57: DHCP: Scan: Router Option: 172.16.0.1
00:18:57: DHCP: rcvd pkt source: 172.16.0.4,  destination:  255.255.255.255
00:18:57:    UDP  sport: 43,  dport: 44,  length: 317
00:18:57:    DHCP op: 2, htype: 1, hlen: 6, hops: 1
00:18:57:    DHCP server identifier: 172.16.0.4
00:18:57:         xid: 1BFE, secs: 0, flags: 8000
00:18:57:         client: 0.0.0.0, your: 172.16.0.6
00:18:57:         srvr:   0.0.0.0, gw: 172.16.0.4
00:18:57:         options block length: 69

00:18:57: DHCP Offer Message   Offered Address: 172.16.0.6
00:18:57: DHCP: Lease Seconds: 86400    Renewal secs:  43200    Rebind secs:   75600
00:18:57: DHCP: Server ID Option: 172.16.0.4
00:18:57: DHCP: offer received from 172.16.0.4
00:18:57: DHCP: SRequest attempt # 1 for entry:
00:18:57: Temp IP addr: 172.16.0.6  for peer on Interface: GigabitEthernet0/1
00:18:57: Temp  sub net mask: 255.255.255.0
00:18:57:    DHCP Lease server: 172.16.0.4, state: 4 Requesting
00:18:57:    DHCP transaction id: 1BFE
00:18:57:    Lease: 86400 secs,  Renewal: 0 secs,  Rebind: 0 secs
00:18:57:    Next timer fires after: 00:00:03
00:18:57:    Retry count: 1   Client-ID: cisco-5254.0015.f24f-Gi0/1
00:18:57:    Client-ID hex dump: 636973636F2D353235342E303031352E
00:18:57:                        663234662D4769302F31
00:18:57:    Hostname: cl_a
00:18:57: DHCP: SRequest- Server ID option: 172.16.0.4
00:18:57: DHCP: SRequest- Requested IP addr option: 172.16.0.6
00:18:57: DHCP: SRequest placed class-id option: 636973636F706E70
00:18:57: DHCP: SRequest: 315 bytes
00:18:57: DHCP: SRequest: 315 bytes
00:18:57:             B'cast on GigabitEthernet0/1 interface from 0.0.0.0
```

The second DHCP OFFER message is a relayed packet from the same DHCP server but coming from the second DHCP relay, so it looks like it's coming from another server. The client decides to ignore it because it already requested address allocation from what seems to be another server:

```
00:18:57: DHCP: Received a BOOTREP pkt
...
00:18:57: DHCP Offer Message   Offered Address: 172.16.0.6
00:18:57: DHCP: Lease Seconds: 86400    Renewal secs:  43200    Rebind secs:   75600
00:18:57: DHCP: Server ID Option: 172.16.0.5
00:18:57: DHCP: offer received from 172.16.0.5
00:18:57: DHCP: offer received in bad state: Requesting  punt
```

Finally, the client receives offer(s) from the second DHCP server. These offers are also ignored:

```
00:19:01: DHCP: Received a BOOTREP pkt
00:19:01: DHCP: Scan: Message type: DHCP Offer
...
00:19:01: DHCP Offer Message   Offered Address: 172.16.0.132
00:19:01: DHCP: Lease Seconds: 86400    Renewal secs:  43200    Rebind secs:   75600
00:19:01: DHCP: Server ID Option: 172.16.0.4
00:19:01: DHCP: offer received from 172.16.0.4
00:19:01: DHCP: offer received in bad state: Bound  punt
00:19:01: Allocated IP address = 172.16.0.6  255.255.255.0
```

### Request an Address Allocation

The DHCP REQUEST message from the DHCP client is sent as a broadcast, which means that it will be relayed to *both DHCP servers*, making one of them confused. Here's what srv-2 has to say about it:

```
00:19:02: DHCPD: DHCPREQUEST received from client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31.
00:19:02: DHCPD: DHCPREQUEST received on interface GigabitEthernet2.
00:19:02: DHCPD: no subnet configured for 10.1.0.5.
00:19:02: DHCPD: FSM state change INVALID
00:19:02: DHCPD: Workspace state changed from INIT to INVALID
00:19:02: DHCPD : Client request received seeing the client for first time
00:19:02: DHCPD: client is confused about its IP address (requested 172.16.0.6, assigned 172.16.0.132).
00:19:02: DHCPD: Option 125 not present in the msg.
00:19:02: DHCPD: Sending notification of ASSIGNMENT FAILURE:
00:19:02:   DHCPD: htype 1 chaddr 5254.0015.f24f
00:19:02:   DHCPD: remote id 020a00000a01000500000000
00:19:02:   DHCPD: giaddr = 10.0.0.5
00:19:02:   DHCPD: interface = GigabitEthernet2
00:19:02:   DHCPD: class id 636973636f706e70
```

However, just before sending out the error message, srv-2 decides that might not be a good idea because we might be dealing with an inter-VRF relaying scenario:

```
00:19:02: DHCPD: Not sending DHCPNAK to client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 due toServer-id-override.
```

Meanwhile, the DHCP client receives a DHCP ACK message from one of the relaying switches and decides to use that switch as its DHCP server in the future[^DIM].

[^DIM]: A bit like how [duck imprinting](https://en.wikipedia.org/wiki/Imprinting_(psychology)) works ;)

```
00:18:57: DHCP: Received a BOOTREP pkt
00:18:57: DHCP: Scan: Message type: DHCP Ack
00:18:57: DHCP: Scan: Client ID: cisco-5254.0015.f24f-Gi0/1
00:18:57: DHCP: Scan: Server ID Option: 172.16.0.4 = AC100004
00:18:57: DHCP: Scan: Lease Time: 86400
00:18:57: DHCP: Scan: Renewal time: 43200
00:18:57: DHCP: Scan: Rebind time: 75600
00:18:57: DHCP: Scan: Subnet Address Option: 255.255.255.0
00:18:57: DHCP: Scan: Router Option: 172.16.0.1
00:18:57: DHCP: rcvd pkt source: 172.16.0.4,  destination:  255.255.255.255
00:18:57:    UDP  sport: 43,  dport: 44,  length: 317
00:18:57:    DHCP op: 2, htype: 1, hlen: 6, hops: 1
00:18:57:    DHCP server identifier: 172.16.0.4
00:18:57:         xid: 1BFE, secs: 0, flags: 8000
00:18:57:         client: 0.0.0.0, your: 172.16.0.6
00:18:57:         srvr:   0.0.0.0, gw: 172.16.0.4
00:18:57:         options block length: 69

00:18:57: DHCP Ack Message
00:18:57: DHCP: Lease Seconds: 86400    Renewal secs:  43200    Rebind secs:   75600
00:18:57: DHCP: Server ID Option: 172.16.0.4
00:19:00: DHCP: Releasing ipl options:
00:19:00: DHCP: Applying DHCP options:
00:19:00:   Setting default_gateway to 172.16.0.1
00:19:00:   Adding default route 172.16.0.1
00:19:01: DHCP: Sending notification of ASSIGNMENT:
00:19:01:   Address 172.16.0.6 mask 255.255.255.0
00:19:01: DHCP Client Pooling: ***Allocated IP address: 172.16.0.6
```

It also receives a second copy of the DHCP ACK message from the same server (but coming through another DHCP relaying switch), and ignores it because it already got an IPv4 address from "another" server:

```
00:19:01: DHCP: Received a BOOTREP pkt
00:19:01: DHCP: Scan: Message type: DHCP Ack
...
00:19:01: DHCP: Server ID Option: 172.16.0.5
00:19:01: DHCP: rcv ack in Bound state: punt
```

### Renewing the Lease

The DHCP client keeps using one of the relaying switches as its DHCP server throughout the lifetime of the lease. For example, when renewing the lease it sends the DHCP REQUEST message to the VLAN IP address of the relaying switch:

```
00:20:56: Temp IP addr: 172.16.0.6  for peer on Interface: GigabitEthernet0/1
00:20:56: Temp  sub net mask: 255.255.255.0
00:20:56:    DHCP Lease server: 172.16.0.4, state: 7 Renewing
00:20:56:    DHCP transaction id: 1BFE
00:20:56:    Lease: 86400 secs,  Renewal: 43200 secs,  Rebind: 75600 secs
00:20:56: Temp default-gateway addr: 172.16.0.1
00:20:56:    Next timer fires after: 04:30:01
00:20:56:    Retry count: 1   Client-ID: cisco-5254.0015.f24f-Gi0/1
00:20:56:    Client-ID hex dump: 636973636F2D353235342E303031352E
00:20:56:                        663234662D4769302F31
00:20:56:    Hostname: cl_a
```

{{<note warn>}}Attempts to renew the lease fail if the DHCP client cannot reach the relaying switch, for example due to switch- or interface failure. However, the DHCP client switches back to broadcast packets before the lease expires, and might be able to reach the DHCP server through another relaying switch.{{</note>}}

There's no information in the DHCP REQUEST packet that would help the relaying switch to figure out what needs to be done, so it forwards the request to all DHCP servers. One of them renews the lease, the other one is (yet again) confused, but decides not to reply:

```
00:21:17: DHCPD: DHCPREQUEST received from client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31.
00:21:17: DHCPD: DHCPREQUEST received on interface GigabitEthernet2.
00:21:17: DHCPD: no subnet configured for 10.1.0.5.
00:21:17: DHCPD: FSM state change INVALID
00:21:17: DHCPD: Workspace state changed from INIT to INVALID
00:21:17: DHCPD: Client either rebooted or rebinding we are seeing the client for first time
00:21:17: DHCPD: client is confused about its IP address (requested 172.16.0.6, assigned 172.16.0.132).
...
00:21:17: DHCPD: Sending notification of ASSIGNMENT_FAILURE:
00:21:17:  DHCPD: due to: CLIENT CONFUSED ABOUT ADDRESS
00:21:17:   DHCPD: htype 1 chaddr 5254.0015.f24f
00:21:17:   DHCPD: remote id 020a00000a01000500000000
00:21:17:   DHCPD: giaddr = 10.0.0.4
00:21:17:   DHCPD: interface = GigabitEthernet2
00:21:17:   DHCPD: class id 636973636f706e70
00:21:17: DHCPD: Not sending DHCPNAK to client 0063.6973.636f.2d35.3235.342e.3030.3135.2e66.3234.662d.4769.302f.31 due toServer-id-override.
```

### Summary

* Inter-VRF DHCP relaying with redundant DHCP servers works, but results in violations of DHCP protocol at several steps of the address assignment and lease renewal process.
* DHCP servers and clients written in strict accordance with [Postel's Law](https://en.wikipedia.org/wiki/Robustness_principle) should have no problems dealing with the resulting mess (Cisco IOS clients and Cisco IOS XE servers definitely work).
* DHCP servers and clients that were not tested in this scenario might misbehave. For example, a DHCP server receiving a DHCP REQUEST for an unexpected IP address might mark that address as already used, reducing the size of its address pool.

**Long story short**: build a lab and run thorough tests before deploying a particular combination of DHCP clients, DHCP relays, and DHCP servers in inter-VRF scenarios with redundant DHCP servers.
