---
kb_section: OSPF_DV
minimal_sidebar: true
pre_scroll: true
title: The Solution
#url: /kb/Internet/EIGRP_stub/10-dual-homed-sites/
---
You might want to tackle the unexpected route flaps introduced by OSPF inter-area mechanisms with the tuning of various OSPF timers. This approach is clearly a kludge not a solution, as it does not address the underlying problem, but solely reduces the span of its impact. If you want to go down this route, these are the router configuration commands you can use:

| Configuration command syntax | Explanation |
|------------------------------|-------------|
| **timers throttle spf _delay interval max-interval_** |	Sets the SPF-related timers. The delay parameter specifies the time between LSA change detection and the SPF run. The interval and max-interval parameters specify the minimum and maximum intervals between the full SPF runs (the inter-SPF interval increases if the network remains unstable). |
| **timers throttle lsa all _delay interval_** | Specifies the initial delay between a change in the routing table and the LSA update. The interval parameter sets the minimum interval between updates to the same LSA. |
{.fmtTable}

There are two solutions (although both imperfect) to the unexpected OSPF route flaps:

* Inter-area route summarization removes the preconditions for the route flap, as the summary LSA inserted into area 0 is less specific than the disappearing IP prefix from a non-backbone OSPF area.
* You could also use the (non-standard) [OSPF ABR Type 3 LSA Filtering](http://www.cisco.com/en/US/products/ps6350/products_configuration_guide_chapter09186a00804556e1.html) feature of Cisco IOS to prevent an ABR from propagating backbone summary LSAs back into a non-backbone area.

For example, we could configure Type 3 LSA filter on A1 and A2 in our sample network to ensure that they don’t accept summary LSAs for prefixes known to be in area 1 from the backbone area. To configure LSA filtering, you have to:

1. Define an IP prefix list that is used to match the LSAs you want to filter.
2. Define an OSPF Type-3 filter with the **area *area-id* filter-list prefix *prefix-name* in|out** router configuration command.

The **area filter-list** configuration command is a bit complex to understand. To start with, the **ip prefix-list** used in the command has to **permit** the prefixes (summary LSAs) that should *not* be filtered and **deny** the prefixes that should be. The **in** and **out** keywords are also a bit counterintuitive:

* If you specify the **in** keyword, the IP prefix list filters the summary LSAs originated by this router into the specified area.
* If you specify the **out** keyword, the IP prefix list filters the summary LSAs generated into other areas based on the information received from this area.

In our scenario, we want to filter the summary LSAs propagated from area 0 into all non-backbone area. The easiest way to configure this filter is to use the **area 0 filter-list out** configuration command. The complete configuration is displayed in the next printout (assuming that the loopback interfaces in area 1 fall within the address range 10.0.0.8/29).

{{<cc>}}Summary LSA filter configured on A1 and A2{{</cc>}}
```
router ospf 1
 area 0 filter-list prefix Area_1_Loopback out
!
ip prefix-list Area_1_Loopback seq 5 deny 10.0.0.8/29 ge 32
ip prefix-list Area_1_Loopback seq 10 permit 0.0.0.0/0 ge 1
```

{{<note>}}You could also use **area 1 filter-list in** configuration command, but then the route flaps could still occur in other non-backbone areas attached to the same ABRs.{{</note>}}
