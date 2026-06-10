---
title: "Anycast-Only Gateways in EVPN Asymmetric IRB"
series_title: "ARP with Anycast-Only Gateways in EVPN Asymmetric IRB"
subtitle: "TL&DR: Making this work in a multi-vendor environment is bound to be great fun."
date: 2026-06-24 08:19:00+0200
tags: [ evpn ]
evpn_tag: details
---
In the [previous blog post](/2026/06/arp-issues-evpn-anycast-unicast/), I described how ARP works in an EVPN asymmetric IRB environment where the PE devices share an anycast MAC/IP address *in addition to* a unicast MAC/IP address. Today, let's see how well things work if the PE devices have *only* the anycast MAC/IP address:

{{<figure src="/2026/06/evpn-fwd-asymmetric-anycast-only.png" caption="Packet forwarding in an EVPN asymmetric IRB design using only anycast gateways">}}
<!--more-->
{{<note warn>}}
The idea of using the same MAC/IP address on multiple devices connected to the same (extended) VLAN should make you very nervous, but that's *state of the art* we have to deal with.

Even if the PE devices are very careful not to step on each other's toes (for example, they usually do not advertise the shared MAC/IP address as an EVPN route), don't expect any control-plane protocols apart from ARP/ND (and maybe other ICMP messages) to work. 
{{</note>}}

Ignoring minor details, let's focus on the elephant in the room: how can L1 resolve the MAC address of HR1 when HB1 tries to reach HR1? The easy way out is "Oh, well, L2 will surely advertise the MAC/IP route for HR1, and L1 can use that to build its ARP cache" (see [ARP with EVPN Asymmetric IRB](/2026/05/arp-issues-evpn-asymmetric-irb/) and [ARP with Anycast Gateways in EVPN Asymmetric IRB](/2026/06/arp-issues-evpn-anycast-unicast/) for details). But what if HR1 is a silent host? Some vendors might shrug and say "too bad," others (like Arista EOS) got creative.

I captured the **tcpdump** of the packets exchanged between L1 and L2 when HB1 first tries to ping HR1 (which has been silent). As we already know, these are the packets exchanged in *blue* and *red* VLANs:

* HB1 sends an ARP request for the default gateway. L1 intercepts that request and answers with the anycast MAC/IP address. We cannot see that packet in the **tcpdump**.
* At the same time, L1 advertises the MAC/IP route for HB1:

```
16:51:35.367560 IP (tos 0xc0, ttl 255, id 12360, offset 0, flags [DF], proto TCP (6), length 195)
    10.0.0.2.36495 > 10.0.0.3.bgp: Flags [P.], cksum 0xce86 (correct), seq 426:569, ack 426, win 500, options [nop,nop,TS val 1463143690 ecr 2676372988], length 143: BGP
	Update Message (2), length: 143
	  Origin (1), length: 1, Flags [T]: IGP
	    0x0000:  00
	  AS Path (2), length: 0, Flags [T]: empty
	  Local Preference (5), length: 4, Flags [T]: 100
	    0x0000:  0000 0064
	  Multi-Protocol Reach NLRI (14), length: 83, Flags [OE]:
	    AFI: VPLS (25), SAFI: EVPN (70)
	    no AFI 25 / SAFI 70 decoder
	    0x0000:  0019 4604 0a00 0002 0002 2100 010a 0000
	    0x0010:  0203 e800 0000 0000 0000 0000 0000 0000
	    0x0020:  0030 aac1 ab44 8040 0001 8a88 0225 0001
	    0x0030:  0a00 0002 03e8 0000 0000 0000 0000 0000
	    0x0040:  0000 0000 30aa c1ab 4480 4020 ac10 000a
	    0x0050:  018a 88
	  Extended Community (16), length: 16, Flags [OT]:
	    target (0x0002), Flags [none]: 65000:1000 (= 0.0.3.232)
	    encapsulation (0x030c), Flags [none]: Tunnel type: VXLAN
	    0x0000:  0002 fde8 0000 03e8 030c 0000 0000 0008
```

* L1 sends an ARP reply to HB1.
* HB1 sends the packet for HR1 to the anycast MAC address.
* L1 receives the packet and has to resolve the MAC address of HR1. It sends an ARP request over VXLAN using the anycast MAC/IP as the source MAC/IP address:

```
16:51:35.376644 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto UDP (17), length 96)
    10.0.0.2.13568 > 10.0.0.3.4789: [no cksum] VXLAN, flags [I] (0x08), vni 101001
ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 172.16.1.11 tell 172.16.1.1, length 46
```

* HR1 replies to the ARP request with an ARP reply sent to the anycast MAC address. We know that L2 intercepts the ARP reply, so L1 will never get its answer. That's where communication can get stuck in some EVPN implementations, but Arista EOS has an ace up its sleeve. **L2 accepts the unsolicited ARP reply and creates a MAC/IP route for HR1**

```
16:51:35.380635 IP (tos 0xc0, ttl 254, id 47576, offset 0, flags [DF], proto TCP (6), length 195)
    10.0.0.3.bgp > 10.0.0.2.36495: Flags [P.], cksum 0x554f (correct), seq 426:569, ack 569, win 506, options [nop,nop,TS val 2676374023 ecr 1463143690], length 143: BGP
	Update Message (2), length: 143
	  Origin (1), length: 1, Flags [T]: IGP
	    0x0000:  00
	  AS Path (2), length: 0, Flags [T]: empty
	  Local Preference (5), length: 4, Flags [T]: 100
	    0x0000:  0000 0064
	  Multi-Protocol Reach NLRI (14), length: 83, Flags [OE]:
	    AFI: VPLS (25), SAFI: EVPN (70)
	    no AFI 25 / SAFI 70 decoder
	    0x0000:  0019 4604 0a00 0003 0002 2500 010a 0000
	    0x0010:  0303 e900 0000 0000 0000 0000 0000 0000
	    0x0020:  0030 aac1 ab5f 980e 20ac 1001 0b01 8a89
	    0x0030:  0221 0001 0a00 0003 03e9 0000 0000 0000
	    0x0040:  0000 0000 0000 0000 30aa c1ab 5f98 0e00
	    0x0050:  018a 89
	  Extended Community (16), length: 16, Flags [OT]:
	    target (0x0002), Flags [none]: 65000:1001 (= 0.0.3.233)
	    encapsulation (0x030c), Flags [none]: Tunnel type: VXLAN
	    0x0000:  0002 fde8 0000 03e9 030c 0000 0000 0008
```

{{<note warn>}}
Do I have to tell you what an excellent attack vector that is if you're trying to snatch the IP address of a neighbor, for example, a SQL server that doesn't use session encryption? Alas, that's the price we're paying for the convenience of bleeding-edge technology.
{{</note>}}

* After receiving the MAC/IP EVPN route for HR1, L1 can update its ARP cache and forward the IP packet it received from HB1 to HR1 over VXLAN:

```
16:51:35.383665 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto UDP (17), length 134)
    10.0.0.2.58699 > 10.0.0.3.4789: [no cksum] VXLAN, flags [I] (0x08), vni 101001
IP (tos 0x0, ttl 63, id 10687, offset 0, flags [DF], proto ICMP (1), length 84)
    172.16.0.10 > 172.16.1.11: ICMP echo request, id 7, seq 0, length 64
```

Problem solved (at least on Arista EOS). What about other vendors? I gave you the blueprint, go and try it out ;)

### Trying It Out {#try}

The [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/asymmetric-irb/topology.yml) I used in this blog post is in the [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/EVPN/asymmetric-anycast). If you want to try it out:

* [Set up your lab environment](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab) (you can use free GitHub Codespaces)
* Change directory to `EVPN/asymmetric-anycast`
* Execute `netlab up`
* If you're using Arista EOS, execute `netlab config --limit pe anycast_only` to remove the unicast IP addresses on L1 and L2, and configure the anycast gateways. You'll have to configure other devices manually.
