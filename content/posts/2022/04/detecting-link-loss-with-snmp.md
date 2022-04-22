---
title: "Detecting Byzantine Link Failures with SNMP"
date: 2022-04-26 07:03:00
tags: [ SNMP ]
---
One of my readers has to deal with a crappy Network Termination Equipment (NTE)[^MODEM] that does not drop local link carrier[^LIGHT] when the remote link fails. Here's the original ASCII art describing the topology:

```
PE---------------NTE--FW---NMS 
  <--------IP-------->
```

He'd like to use interface SNMP counters on the firewall to detect the PE-NTE link failure. He's using static default route toward PE on FW, and tried to detect the link failure with **ifOutDiscards** counter.
<!--more-->

[^MODEM]: Often lovingly and incorrectly called a *modem*.

[^LIGHT]: Sometimes called *light* by the uninitiated when dealing with a fiber cable.

Not surprisingly, that doesn't work. **ifOutDiscard** counter counts the number of packets that got to the outgoing interface but could not be transmitted (the most common scenario being output queue overflow). Straight from MIB-2 description of **ifOutDiscard** counter:

> The number of outbound packets which were chosen to be discarded even though no errors had been detected to prevent their being transmitted. One possible reason for discarding such a packet could be to free up buffer space.

However, a few hours after the link failure, the ARP entry for PE will time out on FW. You can monitor that with **ipNetToMediaTable**, and I'm positive some IP-related error counters (in the **ip** part of MIB-2) will start increasing at that time... but maybe it's a bit too long to wait for a few hours.

What if we were running a routing protocol (for example, BGP) between PE and FW? The routing protocol adjacency between PE and FW would fail after the PE-NTE link failure, and the default route sent from PE to FW would be gone. Would that cause **ifOutDiscard** counter to increase?

Nope. When an IP router has no route toward a destination, it cannot enqueue a packet into an output interface queue, and thus can never cause the **ifOutDiscard** counter to increase, but there are tons of other ways to monitor the loss of the default route:

* An IP router can generate a SNMP trap whenever a routing protocol adjacency goes down;
* You can monitor the state of the routing table on a device with **ipRouteTable** part of MIB-2
* Whenever an IP packet is dropped because an IP router does not have a route to its destination, the **ipOutNoRoutes** counter should be increased[^HW].

Any one of the above approaches would work, but only after the routing adjacency is gone. Welcome to the wonderful world of [routing protocol convergence](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING) where BFD is one of your best friends. 

You don't even have to run a routing protocol to detect path failure between PE and FW. BFD can often be used to check the next hop of a static route; there's also Ethernet Connectivity Fault Management (CFM) and boring old **ping** (aka IP SLA). You can usually monitor all of them with SNMP.

Finally, let's assume we can't run a dynamic routing protocol with PE, cannot use BFD or CFM, and don't want to rely on **ping**. Is there another way to detect PE-NTE link failure in a few seconds with SNMP? Of course -- monitor the packets received by the FW on its external interface (for example, using **ifInOctets**). After all, if the PE-NTE link is gone, we shouldn't be receiving any packets at all. A similar approach might be used to detect unidirectional link failure -- if you see a *sudden drop* in inbound or outbound traffic, it's time to investigate what's going on.

Assuming that _no inbound traffic means link loss_ could result in a false positive -- there might be no traffic on a link during the night. You could mitigate that with a workload that continuously generates traffic (periodically checking whether a remote server is reachable is often a good idea). You could also use a smarter threshold along the lines of _generate an alert if the inbound traffic volume is less than x% of the traffic usually seen at this time of the day on this day of the week_... but that's boring. Wouldn't it be more fun to trigger a billion random link failures[^USER] and use them to train a neural network?

[^HW]: I have no idea how reliable that counter is on platforms using hardware switching.

[^USER]: Warning: your users might get annoyed and trigger a resume-generating event.