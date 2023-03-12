---
date: 2021-02-03 07:15:00+00:00
distributed-systems_tag: sdn
series:
- distributed-systems
series_weight: 1300
tags:
- SDN
- fabric
title: Impact of Centralized Control Plane Partitioning
---
A long-time reader sent me a series of questions about the impact of WAN partitioning in case of an SDN-based network spanning multiple locations after watching the [Architectures](https://my.ipspace.net/bin/list?id=DCFabric#ARCHITECTURES) part of [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics) webinar. He therefore focused on the specific case of *centralized control plane* (read: an equivalent of a stackable switch) with *distributed controller cluster* (read: switch stack spread across multiple locations).

{{<figure src="/2021/02/multi-dc-controllers.png" caption="SDN controllers spread across multiple data centers">}}
<!--more-->
He started with...

> You said that the Centralized control has one IP address per subnet and if the two DC's lose connectivity, it will result in one DC completely unreachable. Is it because the Controller only exists in one DC?

That's how most stackable switch solutions work, see for example [HP IRF](https://blog.ipspace.net/2011/09/long-distance-irf-fabric-works-best-in.html) (mentioned here because they were one of the few vendors "brave" enough to advertise Cross-DC Switch Stack stupidity).
	
The location of the controller cluster and its operations (active/active or active/standby) are architectural decisions, and different architectures went different ways. For example, VMware NSX-V has controllers spread across multiple locations, while VMware NSX-T requires all controllers to be in one location.

The behavior under network partitioning (this is what DCI link failure really is) also depends on controller architecture (does it implement control plane or only management plane) and quality of its implementation. Shutting down the minority part of the partitioned network is the most brutal approach to solving this problem. There are better solutions -- here are some of the typical behaviors observed in the wild:

* Complete shutdown of minority part of the network (most stackable switches);
* Complete shutdown of control plane with data plane operating as long as there are no topology changes or control-plane requests that cannot be handled locally. NSX-T [uses this approach](https://blog.ipspace.net/2019/08/brief-history-of-vmware-nsx.html), and Big Switch made it a bit better by [offloading LACP and ARP to the edge switches](https://blog.ipspace.net/2015/02/big-cloud-fabric-scaling-openflow-fabric.html).
* Minority part of the network reverting to non-controller mode. This is NSX-V approach -- minority site uses fabric-wide flood-and-learn.
* Minority part of the network becoming read-only. This is Cisco ACI approach, and works well only when the controllers remain a management-plane component. The moment you introduce control plane to the controller you're almost forced to go back to one of the previous approaches.
* Minority part of the network losing write access to shared objects. This is how Cisco ACI Multi-Site controller and NSX-T federation work. They both deploy a full-blown controller cluster on each site, and use an umbrella system to synchronize configurable objects across sites. Each location remains fully operational and manageable, and you can even create local objects when undergoing network partition. I expect Microsoft Azure orchestration system to work in a similar way.
* No impact when each location becomes an independent management-plane entity. This is how AWS regions are implemented.

## Summary

When choosing a multi-site controller solution always ask yourself "*what happens when the inter-site link fails?*" and "_am I OK with that behavior?_" 

You won't find the answer to the first question in vendor whitepapers for obvious reasons. You'll have to dig deep into the product documentation; or you could find the answer for the most common data center controller products in *[VMware NSX, Cisco ACI or Standard-Based EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN)* webinar.

## More to Explore

A [quick search for *controller failure* on my blog](https://www.google.com/search?q=controller+failure+site%3Ablog.ipspace.net) resulted in these blog posts:

* [Impact of Controller Failures in Software-Defined Networks](https://blog.ipspace.net/2019/06/impact-of-controller-failures-in.html)
* [Controller Cluster Is a Single Failure Domain](https://blog.ipspace.net/2014/09/controller-cluster-is-single-failure.html)
* [How Hard Is It to Think about Failures?](https://blog.ipspace.net/2016/03/how-hard-is-it-to-think-about-failures.html)
* [On SDN Controllers, Interconnectedness and Failure Domains](https://blog.ipspace.net/2015/04/on-sdn-controllers-interconnectedness.html)
* [OpenFlow Fabric Controllers Are Light-years Away from Wireless Ones](https://blog.ipspace.net/2013/09/openflow-fabric-controllers-are-light.html)

You will also find the impacts of controller failures discussed in these webinars:

* [SDN Architectures and Deployment Considerations](https://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations)
* [VMware NSX, Cisco ACI or Standard-Based EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN)
* [Multi-Site NSX Deployments](https://my.ipspace.net/bin/list?id=NSX#CROSS) and [NSX-T Federation](https://my.ipspace.net/bin/list?id=NSX#FEDERATION) parts of [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)
* [Architectures](https://my.ipspace.net/bin/list?id=DCFabric#ARCHITECTURES) part of [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics)
