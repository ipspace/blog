---
title: "ARP Challenges in EVPN/VXLAN Symmetric IRB"
date: 2025-04-03 08:30:00+0200
tags: [ EVPN, netlab ]
netlab_tag: quirks
evpn_tag: details
---
_Whenever I claimed that EVPN is The SIP of Networking, vendor engineers quickly told me that "EVPN interoperability is a solved problem" and that they run regular multi-vendor interoperability labs to iron out the quirks. As it turns out, things aren't as rosy in real life; it's still helpful to have an EVPN equivalent of the DTMF tone generators handy._

I encountered a particularly nasty quirk when running the _netlab_ EVPN symmetric IRB integration test with an anycast gateway between Juniper vSwitch/Nokia SR Linux and FRR container  (note: it could be that we messed up the configurations; [the usual smallprint](/quirks) applies).

{{<figure src="/2025/04/evpn-symmetric-irb.png" caption="Lab topology">}}

The network topology was as simple as I could make it:
<!--more-->
* Two switches are running VXLAN with EVPN control plane.
* The **red** VLAN is stretched across both switches.
* The **blue** and the **green** VLAN are attached to a single switch (to trigger the various IRB packet flows)
* The **red** VLAN has an anycast gateway configured on both switches, with all hosts using it for static routes.
* All three VLANs are in the same VRF.
* The actual lab topology includes a probe device -- out-of-they-way participant in the EVPN control plane I used to generate debugging printouts.

After the two switches establish OSPF and IBGP adjacencies and exchange EVPN routes, the hosts should be able to ping each other, right? It doesn't always work that way. This is what I experienced when running FRR on S2 and SR Linux (or vJunos-switch) on S1:

* H1 can ping H2 and H4.
* H2 cannot ping H3 *until it pings the default gateway*

Sounds crazy? Here are the printouts generated in an SR Linux/FRR lab[^MFV]. Everything works when S2 runs SR Linux or Arista EOS.

[^MFV]: Because I no longer have the patience to wait for the vjunos-switch container to boot.

{{<cc>}}Pings from H1{{</cc>}}
```
$ netlab connect h1
Connecting to container clab-symmetric_ir-h1, starting bash
h1:/# ping -c 2 h2
PING h2 (172.16.0.5): 56 data bytes
64 bytes from 172.16.0.5: seq=0 ttl=64 time=0.636 ms
64 bytes from 172.16.0.5: seq=1 ttl=64 time=0.539 ms

--- h2 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.539/0.587/0.636 ms
h1:/# ping -c 2 h4
PING h4 (172.16.2.7): 56 data bytes
64 bytes from 172.16.2.7: seq=0 ttl=63 time=0.732 ms
64 bytes from 172.16.2.7: seq=1 ttl=63 time=0.411 ms

--- h4 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.411/0.571/0.732 ms
```

{{<cc>}}Pings from H2{{</cc>}}
```
$ netlab connect h2
Connecting to container clab-symmetric_ir-h2, starting bash
h2:/# ping -c 2 h1
PING h1 (172.16.0.4): 56 data bytes
64 bytes from 172.16.0.4: seq=0 ttl=64 time=0.402 ms
64 bytes from 172.16.0.4: seq=1 ttl=64 time=0.412 ms

--- h1 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.402/0.407/0.412 ms
h2:/# ping -c 2 h3
PING h3 (172.16.1.6): 56 data bytes
^C
--- h3 ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
h2:/# ping -c 2 172.16.0.254
PING 172.16.0.254 (172.16.0.254): 56 data bytes
64 bytes from 172.16.0.254: seq=0 ttl=64 time=0.081 ms
64 bytes from 172.16.0.254: seq=1 ttl=64 time=0.037 ms

--- 172.16.0.254 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.037/0.059/0.081 ms
h2:/# ping -c 2 h3
PING h3 (172.16.1.6): 56 data bytes
64 bytes from 172.16.1.6: seq=0 ttl=63 time=0.294 ms
64 bytes from 172.16.1.6: seq=1 ttl=63 time=0.297 ms

--- h3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.294/0.295/0.297 ms
```

### What's Going On?

I started with a packet capture on H3. It received ICMP requests and replied to them:

{{<cc>}}tcpdump of traffic received and sent by H3{{</cc>}}
```
10:14:09.900986 02:00:ca:fe:00:ff (oui Unknown) > aa:c1:ab:49:d2:55 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 63, id 50416, offset 0, flags [DF], proto ICMP (1), length 84)
    172.16.0.5 > 172.16.1.6: ICMP echo request, id 22, seq 0, length 64

10:14:09.901003 aa:c1:ab:49:d2:55 (oui Unknown) > 02:00:ca:fe:00:ff (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 5210, offset 0, flags [none], proto ICMP (1), length 84)
    172.16.1.6 > 172.16.0.5: ICMP echo reply, id 22, seq 0, length 64
```

Next step: the VXLAN link between S1 and S2. That's where my troubleshooting took a decidedly weird turn:

* ICMP packets are forwarded from S2 to S1 (we knew that already)
* S1 keeps sending ARP requests for H2. It seems it tries to forward the ICMP reply to H2 but lacks its ARP entry.

{{<cc>}}tcpdump of VXLAN traffic between S1 and S2 while H2 tries to ping H3{{</cc>}}
```
09:57:05.735642 aa:c1:ab:d3:ac:3f (oui Unknown) > 1a:cc:05:ff:00:01 (oui Unknown), ethertype IPv4 (0x0800), length 148: (tos 0x0, ttl 64, id 47804, offset 0, flags [none], proto UDP (17), length 134)
    10.0.0.2.39678 > 10.0.0.1.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 5042
12:57:5d:78:fe:32 (oui Unknown) > 1a:cc:05:ff:00:00 (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 63, id 55279, offset 0, flags [DF], proto ICMP (1), length 84)
    172.16.0.5 > 172.16.1.6: ICMP echo request, id 17, seq 0, length 64

09:57:05.823975 1a:cc:05:ff:00:01 (oui Unknown) > aa:c1:ab:d3:ac:3f (oui Unknown), ethertype IPv4 (0x0800), length 92: (tos 0x0, ttl 255, id 25, offset 0, flags [DF], proto UDP (17), length 78)
    10.0.0.1.49772 > 10.0.0.2.4789: [no cksum] VXLAN, flags [I] (0x08), vni 101000
02:00:ca:fe:00:ff (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.5 tell 172.16.0.254, length 28
```

Time to check whether H2 responds to the ARP request. It does 🤔

{{<cc>}}tcpdump of traffic sent and received by H2{{</cc>}}
```
10:02:37.714878 aa:c1:ab:3f:84:eb (oui Unknown) > 02:00:ca:fe:00:ff (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 64, id 32884, offset 0, flags [DF], proto ICMP (1), length 84)
    172.16.0.5 > 172.16.1.6: ICMP echo request, id 21, seq 0, length 64

10:02:37.820849 02:00:ca:fe:00:ff (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.5 tell 172.16.0.254, length 28

10:02:37.820855 aa:c1:ab:3f:84:eb (oui Unknown) > 02:00:ca:fe:00:ff (oui Unknown), ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Reply 172.16.0.5 is-at aa:c1:ab:3f:84:eb (oui Unknown), length 28
```

However, the ARP reply is sent to `02:00:ca:fe:00:ff`, which happens to be the anycast MAC address configured on S1 and S2:

{{<cc>}}netlab data used to configure the **red** VLAN interface on S1{{</cc>}}
```
$ netlab inspect --node s1 interfaces[4]
bridge_group: 1
gateway:
  anycast:
    mac: 0200.cafe.00ff
    unicast: true
  id: -2
  ipv4: 172.16.0.254/24
  protocol: anycast
ifindex: 40000
ifname: irb0.1000
ipv4: 172.16.0.1/24
name: VLAN red (1000) -> [h1,h2,s2]
neighbors:
- ifname: eth1
  ipv4: 172.16.0.4/24
  node: h1
- ifname: eth1
  ipv4: 172.16.0.5/24
  node: h2
- ifname: vlan1000
  ipv4: 172.16.0.2/24
  node: s2
type: svi
virtual_interface: true
vlan:
  mode: irb
  name: red
vrf: customer
```

**BINGO!** We have the first root cause of our mystery: SR Linux is sending the ARP requests *from the anycast gateway MAC address*. However, a bigger mystery remains: why does pinging the gateway MAC address solve the problem?

### The Many Faces of EVPN Type-2 Routes

We know the following packets are sent when H2 tries to ping H3:

* H2 must send an ARP request for the default gateway (172.16.0.254) to get its MAC address
* H2 sends an ICMP request to H3 using the anycast gateway MAC address
* S2 intercepts the H2→H3 packet (that's how anycast gateway works) and routes it onto the *transit VNI* (5042) of customer VRF (evident from the above tcpdump)
* S1 receives the H2→H3 packet and delivers it to H3
* H3 replies to the ICMP request
* S1 receives the ICMP reply and sends an ARP request to H2 *from the anycast gateway MAC address*
* H2 replies to the ARP request, *but the reply never makes it past S2*

What could possibly change when H2 pings the anycast gateway? Here's the sequence of events that ping triggers:

* H2 already has the MAC address of the anycast gateway in its ARP cache
* H2 sends an ICMP request to the anycast gateway IP address using the anycast gateway MAC address.
* The packet is (as before) intercepted by S2.
* S2 replies to the ICMP request but might not have the MAC address of H2 in its ARP cache (it never had to send a packet to H2).
* **S2 sends an ARP request to H2 and receives an ARP reply**
* S2 can deliver the ICMP reply to H2

However, the packets never got past S2, right? As we don't believe in switch entanglement and spooky action at a distance, the only other explanation is *the propagation of some relevant information from S2 to S1*, and we know the relevant information is propagated in EVPN routing updates.

Time to log into the probe device to see what happens when H2 pings anycast gateway on S2. Not surprisingly, S2 does send an update once H2 starts pinging the anycast gateway:

{{<cc>}}EVPN update received by the probe router after the H2→anycast ping{{</cc>}}
```
2025-03-28 10:22:38.224 [DEBG] bgpd: [YCKEM-GB33T]
  10.0.0.2(s2) rcvd 
    RD 10.0.0.2:1000 [2]:[0]:[48]:[aa:c1:ab:3f:84:eb]:[32]:[172.16.0.5] 
      label 101000/5042 l2vpn evpn
```

Time to go back to square one. We'll reload the lab (starting with clean ARP tables and a minimum number of EVPN routes) and inspect the route details for the EVPN type-2 routes with RD 10.0.0.2:1000.

Here are the results:

* When the lab starts, S2 finds the MAC address of H2 and creates the corresponding EVPN type-2 route.

{{<cc>}}MAC address of Ethernet interface on H2{{</cc>}}
```
h2:/# ip link show eth1
975: eth1@if974: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether aa:c1:ab:4e:b2:95 brd ff:ff:ff:ff:ff:ff
```

{{<cc>}}EVPN route for the MAC address of H2{{</cc>}}
```
probe# show bgp evpn route rd 10.0.0.2:1000 mac aa:c1:ab:4e:b2:95
BGP routing table entry for 10.0.0.2:1000:[2]:[0]:[48]:[aa:c1:ab:4e:b2:95]
Paths: (1 available, best #1)
  Not advertised to any peer
  Route [2]:[0]:[48]:[aa:c1:ab:4e:b2:95] VNI 101000
  Local
    10.0.0.2(s2) (metric 10) from s2(10.0.0.2) (10.0.0.2)
      Origin IGP, localpref 100, valid, internal, bestpath-from-AS Local, best (First path received)
      Extended Community: RT:65000:1000 ET:8
      Last update: Fri Mar 28 10:35:38 2025
```

* S2 had no prior IP communication with H2 and does not have H2 in its ARP cache. Consequently, it cannot include the IP address of H2 in the EVPN type-2 route.
* After H2 tries to ping H3, S2 gets the ARP entry for H2 *pointing to the virtual anycast gateway interface*. It does not advertise that information in EVPN.

```
s2(bash)# arp
eth2.probe (10.1.0.9) at aa:c1:ab:c6:ed:54 [ether]  on eth2
h2 (172.16.0.5) at aa:c1:ab:4e:b2:95 [ether]  on varp-40000
ethernet-1-1.s1 (10.1.0.1) at 1a:c7:05:ff:00:01 [ether]  on eth1
```

* After H2 pings the anycast gateway (*varp-40000* interface) on S2, S2 has to reply but uses the regular VLAN interface to send the ICMP reply. S2 now has two ARP entries for H2:

```
s2(bash)# arp
eth2.probe (10.1.0.9) at aa:c1:ab:c6:ed:54 [ether]  on eth2
h2 (172.16.0.5) at aa:c1:ab:4e:b2:95 [ether]  on vlan1000
h2 (172.16.0.5) at aa:c1:ab:4e:b2:95 [ether]  on varp-40000
ethernet-1-1.s1 (10.1.0.1) at 1a:c7:05:ff:00:01 [ether]  on eth1
```

* The ARP entry from the VLAN1000 interface is converted into EVPN type-2 route and advertised to S1 and probe device. The updated route has an IP address attached to it and a VNI label saying _you can use that for the transit VNI in customer VRF_

{{<cc>}}Updated EVPN route for the IP/MAC address of H2{{</cc>}}
```
BGP routing table entry for 10.0.0.2:1000:[2]:[0]:[48]:[aa:c1:ab:4e:b2:95]:[32]:[172.16.0.5]
Paths: (1 available, best #1)
  Not advertised to any peer
  Route [2]:[0]:[48]:[aa:c1:ab:4e:b2:95]:[32]:[172.16.0.5] VNI 101000/5042
  Local
    10.0.0.2(s2) (metric 10) from s2(10.0.0.2) (10.0.0.2)
      Origin IGP, localpref 100, valid, internal, bestpath-from-AS Local, best (First path received)
      Extended Community: RT:65000:1 RT:65000:1000 ET:8 Rmac:46:04:2d:bc:3b:18
      Last update: Fri Mar 28 10:42:46 2025
```

* S1 (SR Linux) can create an ARP entry using the updated EVPN route. It no longer needs to send ARP requests and can deliver the ICMP reply from H3 to H2.

### But Why Does It Work With Arista EOS?

Arista EOS and most other EVPN implementations:

* Cache the ARP requests sent by H2 when it tries to find the anycast gateway MAC address (the ARP request is sent as a broadcast and thus reaches all switches participating in the VXLAN segment)

{{<cc>}}H2 ARP request propagated to S1 in a VXLAN packet{{</cc>}}
```
10:51:58.580026 aa:c1:ab:37:3b:e7 (oui Unknown) > 52:dc:ca:fe:01:01 (oui Unknown), ethertype IPv4 (0x0800), length 92: (tos 0x0, ttl 64, id 20912, offset 0, flags [none], proto UDP (17), length 78)
    10.0.0.2.57652 > 10.0.0.1.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 101000
aa:c1:ab:2e:b3:3f (oui Unknown) > Broadcast, ethertype ARP (0x0806), length 42: Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.254 tell 172.16.0.5, length 28
```

{{<cc>}}S1 does not send an ARP request before delivering the ICMP reply{{</cc>}}
```
10:51:58.580115 aa:c1:ab:37:3b:e7 (oui Unknown) > 52:dc:ca:fe:01:01 (oui Unknown), ethertype IPv4 (0x0800), length 148: (tos 0x0, ttl 64, id 20913, offset 0, flags [none], proto UDP (17), length 134)
    10.0.0.2.39678 > 10.0.0.1.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 5042
6a:34:a1:4d:55:ab (oui Unknown) > 00:1c:73:b4:8c:1a (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 63, id 9249, offset 0, flags [DF], proto ICMP (1), length 84)
    172.16.0.5 > 172.16.1.6: ICMP echo request, id 12, seq 0, length 64

10:51:58.582212 52:dc:ca:fe:01:01 (oui Unknown) > aa:c1:ab:37:3b:e7 (oui Unknown), ethertype IPv4 (0x0800), length 148: (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto UDP (17), length 134)
    10.0.0.1.20067 > 10.0.0.2.4789: [no cksum] VXLAN, flags [I] (0x08), vni 101000
00:1c:73:b4:8c:1a (oui Unknown) > aa:c1:ab:2e:b3:3f (oui Unknown), ethertype IPv4 (0x0800), length 98: (tos 0x0, ttl 63, id 43784, offset 0, flags [none], proto ICMP (1), length 84)
    172.16.1.6 > 172.16.0.5: ICMP echo reply, id 12, seq 0, length 64
```

* Advertise the IP address of H2 the moment they see its first ARP request.

{{<cc>}}EVPN type-2 route advertised by Arista EOS after H2 starts pinging H3{{</cc>}}
```
BGP routing table entry for 10.0.0.2:1000:[2]:[0]:[48]:[aa:c1:ab:d8:2f:bf]:[32]:[172.16.0.5]
Paths: (1 available, best #1)
  Not advertised to any peer
  Route [2]:[0]:[48]:[aa:c1:ab:d8:2f:bf]:[32]:[172.16.0.5] VNI 101000/5042
  Local
    10.0.0.2 (metric 20) from 10.0.0.2 (10.0.0.2)
      Origin IGP, localpref 100, valid, internal, bestpath-from-AS Local, best (First path received)
      Extended Community: RT:65000:1 RT:65000:1000 ET:8 Rmac:00:1c:73:a0:3b:b1
      Last update: Fri Mar 28 11:04:34 2025
```
