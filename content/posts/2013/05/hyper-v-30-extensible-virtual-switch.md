---
date: 2013-05-24 07:18:00+02:00
tags:
- firewall
- switching
- virtualization
- video
title: Hyper-V 3.0 Extensible Virtual Switch
url: /2013/05/hyper-v-30-extensible-virtual-switch/
---
It took years before the rumored Cisco vSwitch materialized (in the form of Nexus 1000v), several more years before there was the first competitor ([IBM Distributed Virtual Switch](/2012/02/ibm-launched-nexus-1000v-competitor/)), and who knows how long before the third entrant ([recently announced HP vSwitch](/2013/05/interop-product-launch-craze/)) jumps out of PowerPoint slides and whitepapers into the real world.

Compare that to the Hyper-V environment, where we have at least two virtual switches ([Nexus 1000V](http://www.cisco.com/en/US/products/ps13056/index.html) and [NEC\'s PF1000](/2013/01/nec-launched-virtual-openflow-switch/)) mere months after Hyper-V\'s general availability.
<!--more-->
The difference: Microsoft did the right thing, created an extensible vSwitch architecture, and thoroughly documented all the APIs (there\'s enough documentation that you can go and implement your own switch extension if you\'re so inclined).

A [short video](https://my.ipspace.net/bin/get/VirtFW/D1%20-%20Hyper-V%20Extensible%20Switch.mp4?doccode=VirtFW) taken from [Virtual Firewalls](http://www.ipspace.net/Virtual_Firewalls) webinar describes the [extensible architecture of Hyper-V virtual switch](http://msdn.microsoft.com/en-us/library/windows/hardware/hh598163(v=vs.85).aspx).

{{<figure src="/2013/05/s320-Hyper-V+vSwitch.jpg" link="https://my.ipspace.net/bin/get/VirtFW/D1%20-%20Hyper-V%20Extensible%20Switch.mp4?doccode=VirtFW">}}

### Short Summary

-   A switch extension can be a [capturing, filtering, or forwarding extension](http://msdn.microsoft.com/en-us/library/windows/hardware/hh598169(v=vs.85).aspx);
-   [Capturing extensions](http://msdn.microsoft.com/en-us/library/windows/hardware/hh598135(v=vs.85).aspx) can capture packets and generate their own packets (example: report to an sFlow collector, implement ERSPAN functionality);
-   [Filtering extensions](http://msdn.microsoft.com/en-us/library/windows/hardware/hh598147(v=vs.85).aspx) can inspect, drop (traffic policing or filtering) or delay (traffic shaping) packets, as well as generate their own packets;
-   [Forwarding extensions](http://msdn.microsoft.com/en-us/library/windows/hardware/hh598148(v=vs.85).aspx) can do all of the above, plus replace the default forwarding rules (specify their own set of output ports). Each packet can be set to one or more output ports to implement flooding, multicast, or SPAN-like behavior.
-   [Each extension is called twice](http://msdn.microsoft.com/en-us/library/windows/hardware/hh582269(v=vs.85).aspx), first on the Ingress path (input VM or port to switch), then (when the set of destination physical or virtual ports is known) on the Egress path (switch to set of output ports).

It seems Microsoft really learned the hard lessons of the circuitous history of virtual networking, and it looks like they did the right thing ... assuming the highly extensible mechanism they implemented doesn't bog down the switching performance. Time to do some performance tests. Any volunteers?

{{<jump>}}
[Watch the video](https://my.ipspace.net/bin/get/VirtFW/D1%20-%20Hyper-V%20Extensible%20Switch.mp4?doccode=VirtFW)
{{</jump>}}
