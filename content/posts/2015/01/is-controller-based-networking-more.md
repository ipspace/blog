---
cli_tag: real
date: 2015-01-28 07:27:00+01:00
distributed-systems_tag: sdn
ha-cluster_tag: sdn
high-availability_tag: ignore
series:
- ha-cluster
- cli
- distributed-systems
series_weight: 1800
tags:
- SDN
- data center
- fabric
- OpenFlow
- high availability
title: Is Controller-Based Networking More Reliable than Traditional Networking?
url: /2015/01/is-controller-based-networking-more/
---
Listening to some SDN pundits one gets an impression that SDN brings peace to Earth, solves all networking problems and makes networking engineers obsolete.

Cynical jokes aside, and ignoring inevitable bugs, is controller-based networking really more reliable than what we do today?
<!--more-->
An SDN solution that abstracts the dirty details of whatever networking functionality (example: [Tail-F NCS](/2013/05/tail-f-network-control-system-first/)) is definitely an improvement over today's CLI-driven box-by-box mentality. If you can disable manual bypasses (it's always easier to tweak a device configuration than to modify the service definition), you'll get a consistent behavior across all devices managed by the SDN controller.

Will that make a network more reliable? It might, but do keep in mind that most network problems arise from operator errors. Making a configuration error on an SDN controller just increases the blast radius (listen to the [Software Gone Wild podcast with Jeremy Schulman](/2014/09/schprokits-with-jeremy-schulman-on/) for more details) -- instead of misconfiguring a single device, the SDN controller helps you [misconfigure the whole network](https://twitter.com/devops_borat/status/41587168870797312). Role-based access controls and other checks are thus even more important in the SDN world than they are in the traditional world of networking.

Finally, there's the (in)famous [*separation of control and data plane*](/2014/01/control-and-data-plane-separation-three/). To illustrate what might be lurking in that part of the SDN world, consider these questions: did you ever have to upgrade a stack of stackable switches, or suffered a bad case of brain-dead supervisor module that [looked OK to the backup supervisor module](/2014/04/should-we-use-redundant-supervisors/) (which thus refused to take over)?

Fabrics implemented with [controller-based centralized control plane](/2013/09/openflow-fabric-controllers-are-light/) (example: OpenFlow controller like Open Daylight) are functionally identical to stackable switches (or Cisco's VSS, Juniper's Virtual Chassis or HP's IRF). Why should they work better than other centralized control plane implementations?

### From Theory to Practice

Want to know more about data center fabric architectures? Check out [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar.

Interested in SDN? Find what you need to get started on [ipSpace.net SDN Resources page](http://www.ipspace.net/SDN) and [explore SDN webinars](http://www.ipspace.net/Roadmap/SDN_and_OpenFlow_webinars).
