---
kb_section: OSPF_DV
minimal_sidebar: true
pre_scroll: true
title: What’s going on?
#url: /kb/Internet/EIGRP_stub/10-dual-homed-sites/
---
To understand why OSPF behaves like it does in a multi-area environment, you must realize that it’s a link-state protocol only within a single area. For example, the path toward the 10.0.0.11/32 prefix (loopback interface on S1) is announced into area 0 as a summary (type-3) Link State Advertisement (LSA), as shown in Figure 2.

{{<figure src="/kb/Internet/OSPF_DV/InterAreaGeneration.gif" caption="Generation of inter-area summary LSA">}}

The contents of the LSA are displayed in the next printout. The LSA contains only the prefix and the cost toward the prefix (typical distance-vector information), but not even the area in which the prefix originates.

{{<cc>}}Summary LSA for IP prefix 10.0.0.11/32 in area 0{{</cc>}}
```
A1#show ip ospf database summary 10.0.0.11

            OSPF Router with ID (10.0.0.1) (Process ID 1)
                Summary Net Link States (Area 0)

  Options: (No TOS-capability, DC, Upward)
  LS Type: Summary Links(Network)
  Link State ID: 10.0.0.11 (summary Network Number)
  Advertising Router: 10.0.0.1
  Network Mask: /32
        TOS: 0  Metric: 65

  Options: (No TOS-capability, DC, Upward)
  LS Type: Summary Links(Network)
  Link State ID: 10.0.0.11 (summary Network Number)
  Advertising Router: 10.0.0.2
  Network Mask: /32
        TOS: 0  Metric: 65
```

{{<note info>}}
**Configuration tip**

The results of the above **show** command were filtered with the output filter **include ^$|Options|Type|Link|Router|Mask|Metric**.
{{</note>}}

When the S1 loses the 10.0.0.11/32 subnet, the ABRs (A1 and A2) run the SPF algorithm in area 1 and discover that the path toward the 10.0.0.11/32 is lost. However, they both have an alternate path through area 0 and the other ABR. The path through area 0 is thus selected as the best path and re-advertized into area 1, as illustrated in Figure 3.

{{<figure src="/kb/Internet/OSPF_DV/InterAreaLoop.gif" caption="A temporary microloop introduced by the ABRs">}}

The following listing contains the corresponding debugging printouts on A1. Please note that the printouts have been heavily filtered for brevity reasons.

{{<cc>}}Initial SPF run on A1{{</cc>}}
```
25:08.699: OSPF: Detect change in LSA type 1, LSID 10.0.0.11, from 10.0.0.11 area 1
25:13.707: OSPF: running SPF for area 1, SPF-type Full
25:13.751: OSPF: Generate sum from intra-area route 10.0.0.11, mask 255.255.255.255, type 3, age 3600, metric 16777215, seq 0x80000002 to area 0
25:13.763: OSPF: running spf for summaries area 0
25:13.767: OSPF: Start processing Summary LSA 10.0.0.11, mask 255.255.255.255, adv 10.0.0.2, age 66, seq 0x80000001 (Area 0) type 3
25:13.771:    Add better path to LSA ID 10.0.0.11, gateway 0.0.0.0, dist 75
25:13.771:    Add path: next-hop 10.0.1.2, interface FastEthernet0/0
25:13.775: Add Summary Route to 10.0.0.11/255.255.255.255. Metric: 75, Next Hop: 10.0.1.2
25:13.779: OSPF: Entered inter-area route sync - area 0
25:13.783: OSPF: Generate sum from inter-area route 10.0.0.11, mask 255.255.255.255, type 3, age 0, metric 75, seq 0x80000001 to area 1
```

However, as the summary LSA for the IP prefix 10.0.0.11/32 in area 0 depends on the router LSA in area 1, both ABRs eventually remove the summary LSA from area 0, triggering another SPF run in area 0 (next diagram and printout). When the SPF algorithm is run the second time in area 0, both ABRs discover they no longer have an inter-area route toward the 10.0.0.11/32 prefix. Thus, the summary LSA is removed from area 1, finally resulting in a correct network topology.

{{<figure src="/kb/Internet/OSPF_DV/LoopCompletion.gif" caption="Network topology is corrected after the summary LSAs are removed">}}

{{<cc>}}Partial SPF run after the inter-area summary is removed from area 0{{</cc>}}
```
25:13.827: OSPF: Detect change in LSA type 3, LSID 10.0.0.11, from 10.0.0.2 area 0
25:13.851: OSPF: Start partial processing Summary LSA 10.0.0.11, mask 255.255.255.255, adv 10.0.0.2, age 3600, seq 0x80000002 (Area 0) type 3
25:13.855: OSPF: inter-route to 10.0.0.11/32 became unreachable, check externals
25:13.867: OSPF: Start partial processing Summary LSA 10.0.0.11, mask 255.255.255.255, adv 10.0.0.1, age 0, seq 0x80000001 (Area 1) type 3
25:13.867: OSPF: Non-backbone/self-originated LSA
25:13.871: OSPF: Start partial processing Summary LSA 10.0.0.11, mask 255.255.255.255, adv 10.0.0.2, age 2, seq 0x80000001 (Area 1) type 3
25:13.875: OSPF: Non-backbone/self-originated LSA
25:18.859: OSPF: Generate sum from inter-area route 10.0.0.11, mask 255.255.255.255, type 3, age 3600, metric 16777215, seq 0x80000002 to area 1
```

However, the whole process resulted in two topology changes in area 1, requiring an extra SPF run on all routers in area 1 to complete the network convergence. As the default throttle timers set the inter-SPF interval at a higher value than the initial SPF delay, the network convergence is prolonged for a significant amount of time.

The debugging printouts on S2 illustrate another interesting behavior of Cisco’s OSPF implementation: even though A1 and A2 realized pretty early on that they were dealing with a loop (the second SPF run was a partial SPF run in area 0 and was thus not subject to inter-SPF interval), they could not originate a changed LSA (to remove the bogus summary route) into area 1 immediately due to [LSA throttling functionality](http://www.cisco.com/en/US/products/ps6350/products_configuration_guide_chapter09186a00804556ba.html) of Cisco IOS; the default LSA throttling parameters allow an LSA to be originated only once every five seconds. The five-second gap between the original LSA and the changed LSA is very evident in the abbreviated debugging printouts:

{{<cc>}}Delayed convergence in area 1 due to LSA throttling{{</cc>}}
```
27:06.271: OSPF: Detect change in LSA type 1, LSID 10.0.0.11, from 10.0.0.11 area 1
27:11.307: OSPF: running SPF for area 1, SPF-type Full
27:11.379: OSPF: Schedule partial SPF - type 3 id 10.0.0.11 adv rtr 10.0.0.2
27:11.387: OSPF: Schedule partial SPF - type 3 id 10.0.0.11 adv rtr 10.0.0.1
27:16.495: OSPF: Detect change in LSA type 3, LSID 10.0.0.11, from 10.0.0.1 area 1
27:16.499: OSPF: Schedule partial SPF - type 3 id 10.0.0.11 adv rtr 10.0.0.1
27:16.571: OSPF: Detect change in LSA type 3, LSID 10.0.0.11, from 10.0.0.2 area 1
27:16.571: OSPF: Schedule partial SPF - type 3 id 10.0.0.11 adv rtr 10.0.0.2
```
