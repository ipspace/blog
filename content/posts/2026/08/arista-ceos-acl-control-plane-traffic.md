---
title: "Arista cEOS Does Not Apply ACLs to Control-Plane Traffic"
date: 2026-08-24 07:20:00+0200
tags: [ security, netlab ]
netlab_tag: quirks
---
When someone starts singing the *Use Digital Twins to Test Your Network* hymn (or, more recently, tells you how AI agents can do that to validate their ideas), ask them about [these minor details](/2025/06/digital-twins-powerpoint-reality/). If they persist, point them (not that it would help) to this [long list of gotchas](/tag/netlab/#quirks).

That list just got longer: Arista cEOS container does not apply inbound ACLs to control-plane traffic (Arista vEOS VM does).
<!--more-->
When testing the [BGP FSM implementations](/2026/08/exploring-bgp-connect-state/), I tried using ACLs to get one-way connectivity on Arista cEOS containers. It didn't work; EBGP sessions were established regardless of what I put in the ACL. I shelved that weird behavior at that time; when I decided to investigate it weeks later, I started with the simplest possible scenario:

* Two hosts (H1, H2) are connected to an Arista cEOS container (SW)
* The cEOS container has an ACL that blocks ICMP and permits everything else
* The ACL is applied in the inbound direction to all switch ports

{{<figure src="/2026/08/eos_acl.png" caption="Lab scenario">}}

Here's the relevant Arista cEOS configuration:

```
interface Ethernet1
   description sw -> h1 [stub]
   platform tfa phy control-frame disabled
   no switchport
   ip address 172.16.0.1/24
   ip access-group noicmp_ipv4 in
!
interface Ethernet2
   description sw -> h2 [stub]
   platform tfa phy control-frame disabled
   no switchport
   ip address 172.16.1.1/24
   ip access-group noicmp_ipv4 in
!
ip access-list noicmp_ipv4
   100 deny icmp any any
   110 permit ip any any
```

Guess what: H1 can't ping H2 (as expected), but it can ping the IP addresses of SW:

```
h1:/# ping h2
PING h2 (172.16.1.3): 56 data bytes
^C
--- h2 ping statistics ---
5 packets transmitted, 0 packets received, 100% packet loss
h1:/# ping sw
PING sw (10.0.0.1): 56 data bytes
64 bytes from 10.0.0.1: seq=0 ttl=64 time=0.059 ms
64 bytes from 10.0.0.1: seq=1 ttl=64 time=0.097 ms
^C
--- sw ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.059/0.078/0.097 ms
h1:/# ping Ethernet1.sw
PING Ethernet1.sw (172.16.0.1): 56 data bytes
64 bytes from 172.16.0.1: seq=0 ttl=64 time=0.059 ms
64 bytes from 172.16.0.1: seq=1 ttl=64 time=0.074 ms
^C
--- Ethernet1.sw ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.059/0.066/0.074 ms
h1:/# ping Ethernet2.sw
PING Ethernet2.sw (172.16.1.1): 56 data bytes
64 bytes from 172.16.1.1: seq=0 ttl=64 time=0.067 ms
64 bytes from 172.16.1.1: seq=1 ttl=64 time=0.060 ms
^C
--- Ethernet2.sw ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.060/0.063/0.067 ms
```

**QED:** Arista cEOS release 4.35.2F does not apply ACLs to traffic sent to its own IP addresses[^HWTT].

[^HWTT]: But then, who would ever want to test that in a digital twin, right? 🤪

Interestingly, Arista vEOS (the virtual machine) works as expected: the inbound ACL blocks all ICMP, and it's inserted early enough in the packet forwarding process that you cannot see the incoming ICMP packets with **tcpdump** running on the switch.

### Reproducing the Results

Here's the [_netlab_ topology](https://netlab.tools/) I used in the test (you'll need the [release 26.08](https://netlab.tools/release/26.08/) with [ACL support](https://netlab.tools/module/routing/#generic-routing-acl) to try it out). Change the `provider` to `libvirt` to test the Arista vEOS VM.

```
provider: clab

module: [ routing ]

nodes:
  sw:
    device: eos
    routing.acl.noicmp:
    - action: deny
      protocol: icmp
    - protocol: ip
  h1.device: linux
  h2.device: linux

links:
- h1:
  sw.routing.acl.in: noicmp
- h2:
  sw.routing.acl.in: noicmp
```