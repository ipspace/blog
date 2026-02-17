---
title: "Cisco IOS/XR OSPFv2 Not-So-Passive Interfaces"
date: 2026-02-19 07:46:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
What's wrong with me? Why do I have to uncover another weirdness  every single time I run _netlab_ integration tests on a new platform? Today, it's Cisco IOS/XR (release 25.2.1) and its understanding of what "passive" means. According to the [corresponding documentation](https://www.cisco.com/c/en/us/td/docs/routers/asr9000/software/25xx/routing/configuration/guide/b-routing-cg-asr9000-25xx/implementing-ospf.html#concept_0B9B449619D748A8B3F3C61DC756BB83), the **passive** interface configuration command is exactly what I understood it to be:

> Use the passive command in appropriate mode to suppress the sending of OSPF protocol operation on an interface.

However, when I ran the *OSPFv2 passive interface* [integration test](https://github.com/ipspace/netlab/blob/5aae878dff0da1ffb256a33532e0748d9ba7df56/tests/integration/ospf/ospfv2/04-passive.yml) with an IOS/XR container, it kept failing with *neighbor is in Init state* (the first and only time I ever encountered such an error after testing over two dozen platforms).
<!--more-->
This is the IOS/XR configuration applied to the offending interface[^NP2P]. It should work, right?

[^NP2P]: Don't fixate on the "network point-to-point" bit. I observed the same behavior without it, but left it in the printout because that's how the interface was configured when I performed the packet capture.

```
router ospf 1
 area 0.0.0.0
  interface GigabitEthernet0/0/0/1
   passive enable
   network point-to-point
   cost 15
```

It took me a bit to realize I should use **tcpdump** to figure out what's *really* going on. This was my [cunning plan](https://blackadderquotes.com/i-have-a-cunning-plan/):

* Start the lab without configuring the devices (`netlab up --no-config`)
* Start **tcpdump** capturing OSPFv2 packets on the FRRouting interface connected to the passive interface of the IOS/XR container (`netlab capture x2 eth1 ip proto 89`)
* Open the popcorn and start the device configuration process (`netlab initial`)

I didn't have to wait long. OSPFv2 was configured on FRRouting first (because it's [done with a Linux script](/2026/02/netlab-frr-configuration/)) and on IOS/XR approximately 10 seconds later. FRRouting started sending its OSPFv2 hellos every 10 seconds (the default *hello interval*), and then IOS/XR jumps in, sends *two OSPFv2 hellos 10 msec apart* **on a passive interface**, and *never sends another OSPFv2 packet on that interface*:

{{<cc>}}OSPFv2 packets captured on the link connected to the IOS/XR passive interface.{{</cc>}} 
```
18:14:14.249230 IP (tos 0xc0, ttl 1, id 24183, offset 0, flags [none], proto OSPF (89), length 64)
    10.42.1.2 > 224.0.0.5: OSPFv2, Hello, length 44
	Router-ID 10.0.0.3, Backbone Area, Authentication Type: none (0)
	Options [External]
	  Hello Timer 10s, Dead Timer 40s, Mask 255.255.255.0, Priority 1
18:14:24.249215 IP (tos 0xc0, ttl 1, id 24190, offset 0, flags [none], proto OSPF (89), length 64)
    10.42.1.2 > 224.0.0.5: OSPFv2, Hello, length 44
	Router-ID 10.0.0.3, Backbone Area, Authentication Type: none (0)
	Options [External]
	  Hello Timer 10s, Dead Timer 40s, Mask 255.255.255.0, Priority 1
18:14:26.367384 IP (tos 0xc0, ttl 1, id 1, offset 0, flags [none], proto OSPF (89), length 96)
    10.42.1.1 > 224.0.0.5: OSPFv2, Hello, length 76 [len 44]
	Router-ID 10.0.0.1, Backbone Area, Authentication Type: none (0)
	Options [External, LLS]
	  Hello Timer 10s, Dead Timer 40s, Mask 255.255.255.0, Priority 1
	  LLS: checksum: 0x7fc4, length: 8
	    Extended Options (1), length: 4
	      Options: 0x00000001 [LSDB resync]
	    Unknown TLV (18), length: 4
	    Unknown TLV (32768), length: 8
18:14:26.370263 IP (tos 0xc0, ttl 1, id 4, offset 0, flags [none], proto OSPF (89), length 96)
    10.42.1.1 > 224.0.0.5: OSPFv2, Hello, length 76 [len 44]
	Router-ID 10.0.0.1, Backbone Area, Authentication Type: none (0)
	Options [External, LLS]
	  Hello Timer 10s, Dead Timer 40s, Mask 255.255.255.0, Priority 1
	  LLS: checksum: 0x7fc4, length: 8
	    Extended Options (1), length: 4
	      Options: 0x00000001 [LSDB resync]
	    Unknown TLV (18), length: 4
	    Unknown TLV (32768), length: 8
18:14:34.249229 IP (tos 0xc0, ttl 1, id 24195, offset 0, flags [none], proto OSPF (89), length 68)
    10.42.1.2 > 224.0.0.5: OSPFv2, Hello, length 48
	Router-ID 10.0.0.3, Backbone Area, Authentication Type: none (0)
	Options [External]
	  Hello Timer 10s, Dead Timer 40s, Mask 255.255.255.0, Priority 1
	  Neighbor List:
	    10.0.0.1
```

The weirdest bit: I would understand low-end network operating systems configured line by line to burp between OSPFv2 being configured on an interface and the **passive** command being accepted (but they never do). However, IOS/XR uses a *candidate* configuration with **commit** to make configuration changes *transactional*. Obviously they're not transactional enough 🤷‍♂️🤦‍♂️

Finally, the QDS[^QDS] I used to [patch the integration test](https://github.com/ipspace/netlab/commit/60582a5e7dfb75e52fab6566f0b04b2b12eabcda): do **clear ip ospf neighbor** on the FRR container connected to the tested device to make it forget its initial indigestion.

[^QDS]: Quick and Dirty Solution