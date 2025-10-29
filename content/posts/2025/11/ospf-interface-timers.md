---
title: "The Curious Case of Default OSPF Interface Timers"
date: 2025-11-04 07:14:00+0100
tags: [ OSPF, netlab ]
netlab_tag: quirks
ospf_tag: adj
---
We run two types of integration tests before shipping a *netlab* release: *device* integration tests that check whether we correctly implemented *netlab* features on all supported devices, and *platform* integration tests that check whether rarely-used core functionality works as expected.

I want to have some validation included in the platform integration tests to ensure the lab devices are started, and that the links and the management network work as expected. The simplest way to get that done is to start OSPF with short hello intervals (to get adjacency up in no time), for example:
<!--more-->
{{<cc>}}Minimal netlab topology that sets OSPF hello interval to one second{{</cc>}}
```
module: [ ospf ]
ospf.timers.hello: 1

nodes: [ a, b ]
links: [ a-b ]
```

That works beautifully with two FRRouting devices or with two Arista EOS devices, but fails miserably when one runs the FRRouting OSPF daemon and the other is an Arista EOS device.

Here are the relevant bits of OSPF configuration:

{{<cc>}}OSPF interface configuration on node A (FRRouting){{</cc>}}
```
interface eth1
 description a -> b
 ip address 10.1.0.1/30
 ip ospf area 0.0.0.0
 ip ospf hello-interval 1
 ip ospf network point-to-point
```

{{<cc>}}OSPF interface configuration on node B (Arista cEOS){{</cc>}}
```
interface Ethernet1
   description b -> a
   ip address 10.1.0.2/30
   ip ospf hello-interval 1
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
```

The configuration commands are almost a perfect match. What could possibly go wrong? Fortunately, both FRRouting and Arista EOS have nice OSPF adjacency logging mechanisms. The moment I turned on terminal logging, my terminal window was flooded with messages similar to this one:

{{<cc>}}FRRouting complaining about interface interval mismatch{{</cc>}}
```
2025-10-29 16:25:18.436 [WARN] ospfd: [XQA13-4ED8B][EC 134217741] Packet 10.0.0.2 [Hello:RECV]: RouterDeadInterval mismatch on eth1:10.1.0.1 (expected 4, but received 40).
```

Arista EOS had something similar to say:

{{<cc>}}Arista EOS complaining about interface interval mismatch{{</cc>}}
```
Oct 29 16:27:02 b Ospf: Instance 1: OSPF: invalid HELLO packet from 10.1.0.1: Invalid Router Dead interval (rcvd/configured: 4/40) (11)
```

You might recognize the value Arista EOS claims is the correct *dead* interval. It's the default OSPF *dead* interval.

**Long story short:** When you configure just the OSPF **hello-interval** on FRRouting, it adjusts the **dead-interval** to be four times the value of the **hello-interval**. Arista EOS does no such adjustment.

Which implementation is correct? RFC 2328, with all its prescriptive slant, offers only a suggestion in Appendix C.3: 

> [RouterDeadInterval] should be some multiple of the HelloInterval (say 4)

FRRouting developers decided to use the suggestion. Arista EOS developers decided the network operator should configure the timers as they see fit.

However, proving (yet again) RFC 1925 rule 6a, _netlab_ release 25.11 [includes a fix](https://github.com/ipspace/netlab/pull/2772): if you specify only **ospf.timers.hello** or **ospf.timers.dead** parameter, the OSPF configuration module calculates the missing value using the magic conversion factor of, say, four.
