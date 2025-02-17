---
title: "Weird Junos IS-IS Metrics"
date: 2025-01-14 08:13:00+0100
tags: [ IS-IS, netlab ]
netlab_tag: quirks
---
_As part of the [netlab](https://netlab.tools/) development process, I run almost [200 integration tests](https://tests.netlab.tools/) on more than [20 platforms](https://netlab.tools/platforms/) (over a dozen operating systems), and the amount of weirdness I discover is unbelievable._

**Today's special**: Junos is failing the [IS-IS metrics](https://github.com/ipspace/netlab/blob/dev/tests/integration/isis/11-cost.yml) test.

The test is trivial:

* The device under test is connected to two IS-IS routers (X1 and X2)
* It has a low metric configured on the link with X1 and a high metric configured on the link with X2

The validation process is equally trivial:
<!--more-->
* Check for IS-IS adjacencies (just to be on the safe side)
* Check for prefixes in the IS-IS database (just to verify they're there)[^VTT]
* Check the cost of the IS-IS prefixes.

[^VTT]: The validation plugin returns `found it` or `not found` status. If we're looking for an IP prefix with a specified cost, the `not found` status might mean `no prefix` or `wrong cost`, so we must first check for the prefix.

That last bit was failing on Junos.

Here's the relevant IS-IS Junos config[^HS]:

[^HS]: I'm positive the Junos old-timers are slapping their heads right now.

{{<cc>}}Junos IS-IS configuration{{</cc>}}
```
protocols {
    isis {
        interface ge-0/0/0.0 {
            level 1 metric 17;
            level 2 metric 17;
            point-to-point;
        }
        interface ge-0/0/1.0 {
            level 1 metric 80000;
            level 2 metric 80000;
            point-to-point;
        }
        interface lo0.0;
    }
}
```

Here's how the test is failing:

{{<cc>}}The IS-IS metric validation is failing{{</cc>}}
```
[c_x1_l1]   Check level-1 cost X2 => X1 [ node(s): x1 ]
[FAIL]      Node x1: Invalid cost for prefix 10.0.0.3/32: expected 150010 found 70073

[c_x1_l2]   Check level-2 cost X2 => X1 [ node(s): x1 ]
[FAIL]      Node x1: Invalid cost for prefix 10.0.0.3/32: expected 150010 found 70063
```

The routing table on X1 does contain an unexpectedly low metric (considering the metric on the incoming link is 70000)[^M63].

[^M63]: The remainder of the cost (63) is probably another dead giveaway for the oldtimers.

{{<cc>}}IS-IS routes on X1{{</cc>}}
```
I>* 10.0.0.1/32 [115/70000] via 10.1.0.1, eth1, weight 1, 00:01:51
I>* 10.0.0.3/32 [115/70073] via 10.1.0.1, eth1, weight 1, 00:01:51
I   10.1.0.0/30 [115/70017] via 10.1.0.1, eth1 inactive, weight 1, 00:01:51
I>* 10.1.0.4/30 [115/70063] via 10.1.0.1, eth1, weight 1, 00:01:51
```

Next step: look at the IS-IS LSP originated by the Junos device:

{{<cc>}}LSP originated by the Junos device{{</cc>}}
```
IS-IS Level-1 link-state database:
LSP ID                  PduLen  SeqNumber   Chksum  Holdtime  ATT/P/OL
dut.00-00                 239   0x00000004  0xc224     905    0/0/0
  Protocols Supported: IPv4, IPv6
  Area Address: 49.0001
  IS Reachability: 0000.0000.0002.00 (Metric: 17)
  IS Reachability: 0000.0000.0003.00 (Metric: 63)
  Hostname: dut
  TE Router ID: 10.0.0.1
  Router Capability: 10.0.0.1 , D:0, S:0
  Extended Reachability: 0000.0000.0002.00 (Metric: 17)
    Link Local  ID: 342
    Link Remote ID: 0
    Local Interface IP Address(es): 10.1.0.1
    Remote Interface IP Address(es): 10.1.0.2
  Extended Reachability: 0000.0000.0003.00 (Metric: 63)
    Link Local  ID: 343
    Link Remote ID: 0
    Local Interface IP Address(es): 10.1.0.5
    Remote Interface IP Address(es): 10.1.0.6
  IP Reachability: 10.1.0.0/30 (Metric: 17)
  IP Reachability: 10.0.0.1/32 (Metric: 0)
  IP Reachability: 10.1.0.4/30 (Metric: 63)
  IPv4 Interface Address: 10.0.0.1
  Extended IP Reachability: 10.1.0.0/30 (Metric: 17)
  Extended IP Reachability: 10.0.0.1/32 (Metric: 0)
  Extended IP Reachability: 10.1.0.4/30 (Metric: 63)
```

Like most other vendors, Junos uses *transitional* IS-IS metrics[^NW] by default in 2025 even though the *wide* metrics were standardized in an RFC in 2004 ([more details](https://isis.bgplabs.net/basic/4-metric/)).

[^NW]: *Narrow* and *wide* metrics are advertised for every prefix or router-to-router connection

Unlike any other vendor I've seen so far, Junos *does not complain* when you enter metrics larger than 63 on a device still using *narrow* metrics but silently changes the narrow (`IP Reachability`) and the wide (`Extended IP Reachability`) metric to 63. Good job guys![^AIT]

[^AIT]: Bizarre behavior clearly violating the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment) might also explain why they're so keen to use AI to troubleshoot networks 😜

Anyway, you have to configure **wide-metrics-only** on **level-1** and **level-2**, and suddenly, everything works as expected.

{{<cc>}}Final Junos configuration{{</cc>}}
```
isis {
    interface ge-0/0/0.0 {
        level 1 metric 17;
        level 2 metric 17;
        point-to-point;
    }
    interface ge-0/0/1.0 {
        level 1 metric 80000;
        level 2 metric 80000;
        point-to-point;
    }
    interface lo0.0;
    level 1 wide-metrics-only;
    level 2 wide-metrics-only;
}
```
