---
date: 2013-10-15 07:31:00+02:00
openflow_101_tag: use
series:
- openflow_101
series_weight: 190
tags:
- SDN
- OpenFlow
title: Forwarding Models in OpenFlow Networks
url: /2013/10/forwarding-models-in-openflow-networks/
---
OpenFlow is a simple TCAM programming protocol, and can be used to implement any network forwarding paradigm as long as:

* OpenFlow specifications include matches and actions (including rewrites) of the packet header fields used in the forwarding paradigm. For example, you cannot program SRv6 tunnels with OpenFlow because it's not part of OpenFlow standard.
* The forwarding hardware you want to use supports the OpenFlow matches and actions you need in your forwarding paradigm.
* The forwarding paradigm does not use dynamic interfaces (example: MPLS-TE tunnels) or multipoint tunnel interfaces (example: VXLAN). OpenFlow was designed to be used on point-to-point physical interfaces and does not include interface management.

This blog post describes some of the more common OpenFlow use cases (assuming you want to use an [obsolete rarely-implemented protocol](/2022/05/openflow-still-kicking/)).
<!--more-->
### Point OpenFlow Deployments

Sometimes you can [solve your problem](/2011/11/openflow-enterprise-use-cases/) by using OpenFlow on individual (uncoupled) devices. Typical use cases:

-   **Edge security policy** -- authenticate users (or VMs) and deploy per-user ACLs before connecting a user to the network (example: [IPv6 first-hop security](/2012/10/ipv6-first-hop-security-ideal-openflow/));
-   **Programmable SPAN ports** -- use OpenFlow entries on a single switch to mirror selected traffic to SPAN port;
-   **DoS traffic blackholing** -- use OpenFlow to block DoS traffic as close to the source as possible, using N-tuples for more selective traffic targeting than the more traditional RTBH approach.
-   **Traffic redirection** -- use OpenFlow to redirect interesting subset of traffic to network services appliance (example: IDS).

Using OpenFlow on one or more isolated devices is simple (no interaction with adjacent devices) and linearly scalable -- you can add more devices and controllers as needed because there's no [tight coupling anywhere in the system](/2013/09/openflow-fabric-controllers-are-light/).

### Fabric OpenFlow Deployments

Most OpenFlow products tried to solve the OpenFlow fabric use case. In these scenarios the OpenFlow controller manages all the switches in the forwarding path and has to install forwarding entries on every one of them.

Not surprisingly, developers of these products took different approaches based on their understanding of networking challenges and limitations of OpenFlow devices.

**Bypass the fabric.** Some solutions (example: [VMware NSX](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)) [bypass the complexities of fabric forwarding by establishing end-to-end something-over-IP tunnels](/2013/08/nicira-nvp-control-plane/), effectively reducing the fabric to a single hop.

**Path-based forwarding**. Install end-to-end path forwarding entries into the fabric and assign user traffic to paths at the edge nodes (aka [Edge and Core OpenFlow](/2013/01/edge-and-core-openflow-and-why-mpls-is/)). Bonus points if you're smart enough to pre-compute and install backup paths.

{{<note>}}If this looks like a description of MPLS LSPs, FECs and FRR, you're spot on. There are only so many ways you can solve a problem in a scalable way.{{</note>}}

The dirty details of path-based forwarding vary based on the hardware capabilities of the switches you use and your programming preferences. Using MPLS or PBB would be the cleanest option -- those packet formats are well understood by network troubleshooting tools, so an unlucky engineer trying to fix a problem in an OpenFlow-based fabric would have a fighting chance.

Unfortunately I haven't seen a data center switch that would implement OpenFlow support for PBB or MPLS. OpenFlow controller developers were trying to bypass those problems with creative uses of packet headers ([VLAN or MAC rewrite](/2012/02/virtual-circuits-in-openflow-10-world/) comes to mind), making a troubleshooters job much more interesting.

**Hop-by-hop forwarding**. Install flow-matching N-tuples in every switch along the path. Results in an architecture that works great in PowerPoint and lab tests, but breaks down in anything remotely similar to a production network due to [scalability problems](http://highscalability.com/blog/2012/6/4/openflowsdn-is-not-a-silver-bullet-for-network-scalability.html), primarily [FIB update challenges](/2012/01/fib-update-challenges-in-openflow/).

If an OpenFlow controller using hop-by-hop forwarding paradigm implements proactive flow installation (install N-tuples based on configuration and topology), it just might work in small deployments. If it uses [reactive flow installation](http://networkstatic.net/openflow-proactive-vs-reactive-flows/) ([punts new flows to the controller](/2013/03/controller-based-packet-forwarding-in/), and installs [microflow entries on every hop for each new flow](/2012/08/openstackquantum-sdn-based-virtual/)), it deserves a nomination for Darwin Award.

### Why does it matter?

Would you buy a core router that only supports RIPv1? Would you use a solution that uses static routes, PBR, and NAT instead of routing protocols? Would you use NetFlow-based forwarding with flows being instantiated by a central router (remember Multi-Layer Switching on Cat5000)? Probably not -- we've learned the hard way which protocols and architectures work and which ones don't.

You might still stumble upon vendors selling you OpenFlow-based solutions (and pixie dust). It's important to understand how these solutions work behind the scenes when evaluating them. Everything will work great in your 2-node proof-of-concept lab, but you might encounter severe scalability limitations in real-life deployment.

### Revision History

2022-07-15
: Edited and cleaned up obsolete references
