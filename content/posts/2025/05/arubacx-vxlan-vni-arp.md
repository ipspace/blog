---
title: "Dear ArubaCX, VXLAN VNI Has 24 Bits"
date: 2025-05-29 07:55:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
_I thought I've [seen it all](/tag/netlab#quirks), but the networking vendors (and their lack of testing) never cease to amaze me. Today's special: ArubaCX software VXLAN implementation._

We decided it's a good idea to rewrite the VXLAN integration tests to use one target device and one FRR container to test inter-vendor VXLAN interoperability. After all, what could possibly go wrong with a [simple encapsulation format](https://www.rfc-editor.org/rfc/rfc7348.html) that could be described on a single page?

Everything worked fine (as expected), except for the ArubaCX VM (running release Virtual.10.15.1005, build ID AOS-CX:Virtual.10.15.1005:9d92f5caa6b6:202502181604), which failed every single test.
<!--more-->
The first integration test is a [simple 2-node VXLAN bridging scenario](https://blog.ipspace.net/2022/09/netlab-vxlan-bridging/) ([actual test topology](https://github.com/ipspace/netlab/blob/dev/tests/integration/vxlan/01-vxlan-bridging.yml), already including VNI fixes). The tested device is S1, and S2 is an FRR container. 

{{<figure src="/2022/09/vxlan-bridging.png" caption="Lab diagram">}}

This is the relevant configuration of the ArubaCX device:

{{<printout>}}
vlan 1000
    name red
vlan 1001
    name blue
interface vlan 1000
    description VLAN red (1000) -> [h1,h2,s2]
interface vlan 1001
    description VLAN blue (1001) -> [h3,h4,s2]
interface vxlan 1
    source ip 10.0.0.5
    no shutdown
    vni 101000
        vlan 1000
        vtep-peer 10.0.0.6
    vni 101001
        vlan 1001
        vtep-peer 10.0.0.6
{{</printout>}}

The only problem: while the configuration works with two ArubaCX boxes, it doesn't work with any other device. A quick packet capture on the link between S1 and S2 (while H1 is pinging H2) is all you need to identify the problem[^TWL]:

[^TWL]: Unfortunately, it can take hours (or even days) to figure out where to look 🤷‍♂️

{{<cc>}}H1 sending an ARP request for H2{{</cc>}}
```
$ netlab capture s2 eth1 udp
Starting packet capture on s2/eth1: sudo ip netns exec clab-X-s2 tcpdump -i eth1 --immediate-mode -l -vv udp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
...
15:11:31.700384 IP (tos 0x0, ttl 64, id 0, offset 0, flags [none], proto UDP (17), length 78)
    10.0.0.5.2157 > 10.0.0.6.4789: [no cksum] VXLAN, flags [I] (0x08), vni 35464
ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.2 tell 172.16.0.1, length 28
```

Did you notice the weird VNI (35646) in the packet capture? That's the lower 16 bits of the configured VNI (101000). No wonder S2 does not want to hear about that packet.

OK, so maybe someone copied *int* instead of *long* into a packet header. Things happen. However, ArubaCX also refuses to *receive* packets with the correct VNI:

{{<cc>}}H2 desperately trying to reach H1{{</cc>}}
```
$ netlab capture s2 eth1 udp
Starting packet capture on s2/eth1: sudo ip netns exec clab-X-s2 tcpdump -i eth1 --immediate-mode -l -vv udp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
...
15:09:20.666173 IP (tos 0x0, ttl 64, id 38708, offset 0, flags [none], proto UDP (17), length 78)
    10.0.0.6.43421 > 10.0.0.5.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 101000
ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.1 tell 172.16.0.2, length 28
15:09:21.683588 IP (tos 0x0, ttl 64, id 38899, offset 0, flags [none], proto UDP (17), length 78)
    10.0.0.6.43421 > 10.0.0.5.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 101000
ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.1 tell 172.16.0.2, length 28
15:09:22.707641 IP (tos 0x0, ttl 64, id 38988, offset 0, flags [none], proto UDP (17), length 78)
    10.0.0.6.43421 > 10.0.0.5.4789: [udp sum ok] VXLAN, flags [I] (0x08), vni 101000
ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.0.1 tell 172.16.0.2, length 28
```

Does it matter? I have no idea. It could be a quirk of Aruba's software packet forwarding implementation[^HCC], or it could be something more sinister, but someone definitely forgot to check Aruba's VXLAN implementation with VNIs larger than 65536.

[^HCC]: [Stefano Sasso claims](https://github.com/ipspace/netlab/pull/2283#pullrequestreview-2861859083) that the physical Aruba devices have no such limitations.

**Workarounds:**

* The integration tests use hard-coded VNIs (5000 and 5001). By default, VNIs start at 101000.
* _netlab_ release 2.0.1 generates an error if you try to use VNI values above 65535 on ArubaCX.

