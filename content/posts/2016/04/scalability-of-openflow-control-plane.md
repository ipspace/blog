---
date: 2016-04-25 08:21:00+02:00
distributed-systems_tag: openflow
series:
- distributed-systems
tags:
- SDN
- scalability
- OpenFlow
title: Scalability of OpenFlow Control Plane Network
url: /2016/04/scalability-of-openflow-control-plane/
---
I got an interesting question from one of my readers:

> If every device talking to a centralized control plane uses an out-of-band channel to talk to the OpenFlow controller, isn't this a scaling concern?

A year or so ago I would have said **NO** (arguing that the \$0.02 CPU found in most networking devices is too slow to overload a controller or reasonably-fast [control-plane network](/2013/12/control-plane-in-openflow-networks/)).
<!--more-->
In the meantime, the last generations of data center switches got decent CPUs (even multi-core ones) and way more bandwidth between forwarding ASICs and CPUs, so the control-plane network overload might be a real consideration. Still, we're probably far away from the point where 1GE-per-device control-plane network would become a bottleneck.

Well-designed solutions that use [proactive flow setups](/2013/03/controller-based-packet-forwarding-in/)exchange small amounts of information between an OpenFlow switch and a controller. On the other hand, if your controller sets up flows in response to unknown traffic punted to the controller (reactive mode), you'll face so many [scalability challenges](http://content.ipspace.net/get/2.1%20-%20Centralized%20Control%20Plane.mp4) that you won't even notice the potential bandwidth limitations of the control-plane network.

This does not mean that you can ignore the problem though. Some [control-plane traffic](/2013/10/what-exactly-is-control-plane/) has to be [sent to the controller](/2013/06/implementing-control-plane-protocols/) and represents a nice attack vector that can be used to bring down the switch or even the controller without proper control-plane policing.

{{<note warn>}}Most vendors offering OpenFlow-enabled switches haven't even considered control-plane policing of [punted OpenFlow traffic](/2013/03/controller-based-packet-forwarding-in/). Cisco is the only exception I found so far; if I've missed something, please write a comment.{{</note>}}

Finally, you might be concerned with the controller scalability. Building scale-out controller architecture where each controller instance controls a subset of the network is a well-understood problem that is relatively easy to solve if you're OK with eventual consistency across the controller cluster, but then your controller-based network won't behave any different from classical networks, so why bother.

A shipping example of this architecture is VMware NSX, and I'm not aware of any other OpenFlow-based controller that would have the same functionality -- if you know more, please send me an email.

For more technical details, watch my [OpenFlow Deep Dive](http://www.ipspace.net/OpenFlow_Deep_Dive) webinar.
