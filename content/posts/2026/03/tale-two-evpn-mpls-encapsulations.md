---
title: "The Tale of Two EVPN/MPLS Encapsulations"
subtitle: The SIP of Networking Strikes Again
date: 2026-03-04 08:09:00+0100
tags: [ EVPN, MPLS ]
evpn_tag: details
---
I decided it was high time to create [EVPN/MPLS](https://github.com/ipspace/netlab/tree/dev/tests/integration/evpn) netlab [integration tests](/2024/05/netlab-integration-tests/) and wanted to use the same approach I used for the EVPN/VXLAN ones:

* One of the PE-devices is the device we want to test
* The other PE-device is a device that is known to work (ideally, an FRRouting container).
* Bonus points if the other PE-device can generate operational data in JSON format. Using a device for which we already have a validation plugin is close to perfection.
* Add a P-router in the middle because MPLS.
* Attach some hosts to the two PE-devices (we're testing two MAC-VRFs in the [final version of the test](https://github.com/ipspace/netlab/blob/dev/tests/integration/evpn/51-mpls-bridging.yml))
* After validating everything that can reasonably be validated (OSPF session, IBGP session, EVPN AF on IBGP session), do the end-to-end pings and hope for the best.

This is the graph netlab created from the lab topology:
<!--more-->
{{<figure src="/2026/03/evpn-mpls-topo.png">}}

The wonderful idea quickly came apart when I realized FRRouting does not support EVPN with MPLS encapsulation. No biggie; Arista EOS does. Let's use Arista EOS as the well-known PE-device.

We already had an EVPN-over-MPLS implementation for Arista EOS, and once I wrote the simple *bridging over EVPN/MPLS* test, the Arista EOS implementation passed it with flying colors (no surprise there, since the two PE routers were running the same software).

Next step: EVPN-over-MPLS implementation for Cisco IOS/XE. The control plane immediately worked. All the expected EVPN routes were in the BGP table, but the ARPs failed.

I had experienced similar problems in the past, so I knew what to do: start packet capturing. Here's the ARP request sent from H1 to H2:

```
17:26:58.138629 aa:c1:ab:ff:be:2f (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: 
  Ethernet (len 6), IPv4 (len 4), Request who-has 172.31.1.2 tell 172.31.1.1, length 28
```

And this is what H2 received:

```
17:26:58.139554 be:2f:08:06:00:01 (oui Unknown) > ff:ff:aa:c1:ab:ff (oui Unknown), ethertype IPv4 (0x0800), length 38: IP0 (invalid)
```

Doesn't look like an ARP request, does it? It took me a while to figure out I should be capturing the MPLS traffic carrying the Ethernet frames, but once I did that, everything made (some weird) sense. Here's the ARP request from H1 to H2 (encapsulated by Cisco IOS/XE):

```
17:29:39.637254 MPLS (label 16, exp 0, ttl 255)
	(label 1040999, exp 0, [S], ttl 255)
	0x0000:  ffff ffff ffff aac1 abff be2f 0806 0001  .........../....
	0x0010:  0800 0604 0001 aac1 abff be2f ac1f 0101  .........../....
	0x0020:  0000 0000 0000 ac1f 0102                 ..........
```

And here's the ARP request from H2 to H1 (encapsulated by Arista EOS):

```
17:30:26.071591 MPLS (label 16, exp 0, [S], ttl 255)
	0x0000:  0000 0000 ffff ffff ffff aac1 ab58 2fa5  .............X/.
	0x0010:  0806 0001 0800 0604 0001 aac1 ab58 2fa5  .............X/.
	0x0020:  ac1f 0102 0000 0000 0000 ac1f 0101 0000  ................
	0x0030:  0000 0000 0000 0000 0000 0000 0000 0000  ................
```

Can you spot the difference? Let me help you: the initial four bytes of all zeros in the MPLS payload sent by Arista EOS.

After losing way too much time trying to figure out what's going on, the MPLS LFIB printout on Arista EOS proved to be the illuminating bit I needed:

```
s2#show mpls route
MPLS forwarding table (Label [metric] Vias) - 4 routes
MPLS next-hop resolution allow default route: False
Metric Codes:
          A - Active metric
Via Type Codes:
          M - MPLS via, LP - LDP pseudowire via,
          I - IP lookup via, V - VLAN via,
          VA - EVPN VLAN aware via, ES - EVPN ethernet segment via,
          VF - EVPN VLAN flood via, AF - EVPN VLAN aware flood via,
          NG - Nexthop group via, BP - BGP pseudowire via,
          VP - VPWS pseudowire via, MSP - Static pseudowire via,
          EL - EVPN E-Tree Leaf Label via

 116384  A[1]
                via M, 10.1.0.5, pop
                    EgressACL: apply
                    directly connected, Ethernet1
                    aa:c1:ab:0d:c2:5e, vlan 1006
 116385  A[1]
                via M, 10.1.0.5, swap 17
                    EgressACL: apply
                    directly connected, Ethernet1
                    aa:c1:ab:0d:c2:5e, vlan 1006
 1040999  [0]
                via VF, vlan1000, control word present
 1047390  [0]
                via V, vlan1000, control word present
```

Arista EOS expects to use the pseudowire control word on flooding LSPs.

Time for a deep dive into [RFC 7432](https://datatracker.ietf.org/doc/html/rfc7432) (BGP MPLS-Based Ethernet VPN). Here's what it has to say about the *control words* in [Section 18 (Frame Ordering)](https://datatracker.ietf.org/doc/html/rfc7432#section-18):

{{<long-quote>}}
In order to avoid any such misordering, the following rules are applied:

* If a network uses deep packet inspection for its ECMP, then the "Preferred PW MPLS Control Word" [RFC4385] SHOULD be used with the value 0 (e.g., a 4-octet field with a value of zero) when sending EVPN-encapsulated packets over an MP2P LSP.
* If a network uses entropy labels [RFC6790], then the control word SHOULD NOT be used when sending EVPN-encapsulated packets over an MP2P LSP.
* When sending EVPN-encapsulated packets over a P2MP LSP or P2P LSP, then the control word SHOULD NOT be used.
{{</long-quote>}}

As the PE device advertises the same MPLS label for ingress replication to all peers in the same MAC-VRF, one could argue that the flooding LSPs are MP2P LSPs and SHOULD use the control word. Either someone on the Cisco IOS/XE team didn't get the memo, or considers the flooding LSPs to be P2P LSPs, or they decided that SHOULD is not a MUST.

I honestly don't care who's right; if only there had been a nerd knob on either platform that would allow me to adapt it to the other perspective on how the RFC should be read. Alas, I had no luck finding it.

Every time I bring up some "EVPN is SIP of networking" scenario, I hear from the vendors claiming how much EVPN interoperability testing they're doing. While that might be comforting to hear, it didn't help me much; I'm obviously too stupid to make EVPN/MPLS MAC-VRFs work between Arista EOS and Cisco IOS/XE. Please leave a comment if I missed something.
