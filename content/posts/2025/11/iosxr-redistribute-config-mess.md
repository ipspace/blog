---
title: "IOS/XR Route Redistribution Configuration Mess"
date: 2025-11-24 07:43:00+0100
tags: [ OSPF, netlab ]
netlab_tag: quirks
ospf_tag: adj
---
One would hope that the developers of a network operating system wouldn't feel the irresistible urge to reinvent what should have been a common configuration feature for every routing protocol. Alas, the IOS/XR developers failed to get that memo.

I decided to [implement route redistribution](https://github.com/ipspace/netlab/pull/2824) (known as _route import_ in _netlab_) for OSPFv2/OSPFv3, IS-IS, and BGP on IOS/XR (Cisco 8000v running IOS/XR release 24.4.1) and found that each routing protocol uses a different syntax for the _source routing protocol_ part of the **redistribute** command.
<!--more-->
Here's how one can redistribute OSPF routes into BGP:

```
RP/0/RP0/CPU0:dut(config)#router bgp 123
RP/0/RP0/CPU0:dut(config-bgp)#addr ipv4 unicast
RP/0/RP0/CPU0:dut(config-bgp-af)#redistribute ospf 1 match internal external ?
  1              Redistribute external type 1 routes
  2              Redistribute external type 2 routes
  metric         Metric for redistributed routes
  multipath      Enable installation of multiple paths from RIB
  nssa-external  Redistribute OSPF NSSA external routes
  route-policy   Route policy reference
  <cr>
```

Having Cisco IOS battle scars, I decided to be on the safe side and use **match internal external nssa-external** to redistribute every possible route type from OSPF into BGP[^OS]. 

[^OS]: At least we don't have to tell IOS/XR to redistribute OSPF *subnets* into BGP like we have to do in Cisco IOS. I have no idea why that stupidity persists for 30+ years.

The same command syntax does not work when redistributing OSPF into IS-IS:

```
RP/0/RP0/CPU0:dut(config)#router isis Gandalf
RP/0/RP0/CPU0:dut(config-isis)#address-family ipv4 unicast
RP/0/RP0/CPU0:dut(config-isis-af)#redistribute ospf 1 match ?
  external       Redistribute OSPF external routes
  internal       Redistribute OSPF internal routes
  nssa-external  Redistribute OSPF NSSA external routes
RP/0/RP0/CPU0:dut(config-isis-af)#redistribute ospf 1 match internal ?
  level-1       Redistribute routes into level 1 only
  level-1-2     Redistribute routes into both levels
  level-2       Redistribute routes into level 2 only (the default)
  metric        Metric for redistributed routes
  metric-type   IS-IS metric type for redistributed routes
  route-policy  Route policy reference
  <cr>
```

You cannot specify more than one OSPF route type in the **redistribute** command, and if you try to enter two **redistribute ospf** commands, the second one overwrites the first one, even though they have different **match** requirements. Lovely. In the end, I gave up and used the simple **redistribute ospf _pid_** command. Some routes are bound to get from OSPF to IS-IS[^ORI].

[^ORI]: The integration tests pass, but I'm only checking for redistribution of internal OSPF routes. At least we know that works ;)

Redistributing IS-IS into OSPF or BGP is no better. Here's the IS-IS-to-BGP syntax:

```
RP/0/RP0/CPU0:dut(config)#router bgp 123
RP/0/RP0/CPU0:dut(config-bgp)#address-family ipv4 unicast
RP/0/RP0/CPU0:dut(config-bgp-af)#redistribute isis Gandalf level ?
  1             Redistribute ISIS level 1 routes
  1-inter-area  Redistribute ISIS level 1 inter-area routes
  2             Redistribute ISIS level 2 ISIS routes
RP/0/RP0/CPU0:dut(config-bgp-af)#redistribute isis Gandalf level 1 ?
  level         Redistribute routes from the specified ISIS levels
  metric        Metric for redistributed routes
  multipath     Enable installation of multiple paths from RIB
  route-policy  Route policy reference
  <cr>
```

You have to use **redistribute isis _instance_ level 1 level 2** to redistribute all IS-IS routes into BGP.
\
And here's how you redistribute IS-IS into OSPF:

```
RP/0/RP0/CPU0:dut(config)#router ospf 1
RP/0/RP0/CPU0:dut(config-ospf)#redistribute isis level ?
  level-1       IS-IS level-1 routes only
  level-1-2     IS-IS level-1 and level-2 routes
  level-2       IS-IS level-2 routes only
  lsa-type      LSA type for redistributed routes
  metric        Metric for redistributed routes
  metric-type   OSPF exterior metric type for redistributed routes
  nssa-only     Redistribute to NSSA areas only
  route-policy  Apply route-policy to redistribution
  tag           Set tag for routes redistributed into OSPF
  <cr>
```

The command to use to redistribute all IS-IS routes into OSPF is now **redistribute isis _instance_ level-1-2**.

One might not care about such minor inconsistencies (apart from yelling at the box when the fingers are faster than the conscious brain) when doing manual configuration, but they're soul-drainingly irritating[^SCG] (as is the IOS/XR boot time) when you try to create reusable configuration templates. However, I don't expect anything to change until we start voting with our wallets.

[^SCG]: Suggested by ChatGPT 😜
