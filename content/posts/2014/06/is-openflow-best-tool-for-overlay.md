---
cdate: 2022-07-19
comment: 'When you have a hammer, every problem seems like a nail -- Nicira (acquired
  by VMware to form the foundation layers of VMware NSX) and later Open Daylight tried
  to implement network virtualization with OpenFlow.


  As it turns out, they might have used a wrong tool, but old habits die hard: VMware
  NSX-T is still using Open vSwitch on Linux-based hypervisors.

  '
date: 2014-06-12 07:41:00+02:00
openflow_101_tag: ugly
series:
- openflow_101
series_weight: 150
tags:
- OpenFlow
- overlay networks
- virtualization
title: Is OpenFlow the Best Tool for Overlay Virtual Networks?
url: /2014/06/is-openflow-best-tool-for-overlay.html
---
Overlay virtual networks were the first commercial-grade OpenFlow use case -- [Nicira's Network Virtualization Platform](https://blog.ipspace.net/2011/10/what-is-nicira-really-up-to.html) (NVP -- rebranded as VMware NSX for Multiple Hypervisors after the acquisition, and finally rearchitected into VMware NSX-T) used OpenFlow to program the hypervisor virtual switches (Open vSwitches -- OVS).

OpenStack is using the same approach in its OVS Neutron plugin, and it seems Open Daylight aims to reinvent that same wheel, replacing OVS plugin running on the hypervisor host agent with central controller.

Does that mean one should always use OpenFlow to implement overlay virtual networks? Not really, OpenFlow is not exactly the best tool for the job.
<!--more-->
### Easy Start: Isolated Layer-2 Overlay Networks

Most OVS-based solutions (VMware NSX for Multiple Hypervisors, OpenStack ...) use OpenFlow to program forwarding entries in hypervisor virtual switches. In an isolated layer-2 overlay virtual network OpenFlow isn't such a bad fit -- after all, the hypervisor virtual switches need nothing more than mapping between VM MAC addresses and hypervisor transport IP addresses, and that information is readily available in the cloud orchestration system.

The OpenFlow controller can thus proactively download the forwarding information to the switches, and stay out of the forwarding path, ensuring reasonable scalability.

BTW, even this picture isn't all rosy -- Nicira had to [implement virtual tunnels to work around the OpenFlow point-to-point interface model](https://blog.ipspace.net/2013/08/are-overlay-networking-tunnels.html).

### The First Glitches: Layer-2 Gateways

[Adding layer-2 gateways to overlay virtual networks](https://blog.ipspace.net/2014/05/connecting-legacy-servers-to-overlay.html) reveals the first shortcomings of OpenFlow. Once the layer-2 environment stops being completely deterministic (layer-2 gateways introduce the need for dynamic MAC learning), the solution architects have only a few choices:

-   Perform dynamic MAC learning in the OpenFlow controller -- all frames with unknown source MAC addresses are punted to the controller, which builds the dynamic MAC address table and downloads the modified forwarding information to all switches participating in a layer-2 segment. This is the approach used by NEC's ProgrammableFlow solution.\
    **Drawback**: controller gets involved in the data plane, which limits the scalability of the solution.
-   Offload dynamic MAC learning to specialized service nodes, which serve as an intermediary between the predictive static world of virtual switching, and the dynamic world of VLANs. It seems NVP used this approach in one of the early releases, and it got reintroduced with VMware NSX-T Edge Nodes.\
    **Drawback**: The service nodes become an obvious chokepoint; an additional hop through a service node increases latency.
-   Give up, half-ditch OpenFlow, and implement either dynamic MAC learning in virtual switches in parallel with OpenFlow, or reporting of dynamic MAC addresses to the controller using a non-OpenFlow protocol (to avoid data path punting to the controller). VMware NSX-T uses this approach when it cannot offload the dynamic information into the Edge Nodes.

### The Killer: Distributed Layer-3 Forwarding

Every layer-2 overlay virtual networking solution must eventually support distributed layer-3 forwarding (the customers that matter usually want that for one reason or another). Regardless of how you implement the distributed forwarding, hypervisor switches need ARP entries (see [this blog post](https://blog.ipspace.net/2013/10/the-intricacies-of-optimal-layer-3.html) for more details), and have to reply to ARP queries from the virtual machines.

Even without the ARP proxy functionality, someone has to reply to the ARP queries for the default gateway IP address.

ARP is a nasty beast in an OpenFlow world -- it's a control-plane protocol and thus [not implementable in the pure OpenFlow switches](https://blog.ipspace.net/2013/06/implementing-control-plane-protocols.html). The implementers have (yet again) two choices:

-   [Punt](https://blog.ipspace.net/2013/03/controller-based-packet-forwarding-in.html) the ARP packets to the controller, which yet again places the OpenFlow controller in the forwarding path (and limits its scalability);
-   [Solve layer-3 forwarding with a different tool](https://blog.ipspace.net/2013/11/layer-2-and-layer-3-switching-in-vmware.html) (approach used by VMware NSX and distributed layer-3 forwarding in OpenStack).

### Do We Really Need OpenFlow?

With all the challenges listed above, does it make sense to use OpenFlow to control overlay virtual networks? Not really. OpenFlow is like a Swiss Army knife (or a [duck](https://blog.ipspace.net/2009/06/atm-is-like-duck.html)) -- it can solve many problems, but is not ideal for any one of them.

Instead of continuously adjusting the tool to make it fit for the job, let's step back a bit and ask another question: what information do we really need to implement layer-2 and layer-3 forwarding in an overlay virtual network? All we need are three simple lookup tables that can be installed via any API mechanism of your choice ([Hyper-V uses PowerShell](https://blog.ipspace.net/2012/12/hyper-v-network-virtualization-wnvnvgre.html)):

-   IP forwarding table;
-   ARP table;
-   VM MAC-to-underlay IP table.

Some implementations would have a separate *connected interfaces table*; other implementations would [merge that with the forwarding table](https://blog.ipspace.net/2007/05/what-is-cached-cef-adjacency.html). There are also implementations [merging ARP and IP forwarding tables](http://blog.ipspace.net/2014/02/this-is-not-host-route-youre-looking-for.html).

These three tables, combined with local layer-2 and layer-3 forwarding is all you need. Wouldn't it be better to keep things simple instead of introducing yet-another less-than-perfect abstraction layer?

### Want to Know More?

You'll find control-plane architectures and packet walks of numerous overlay virtual networking solutions in the [Overlay Virtual Networking](http://www.ipspace.net/Overlay_Virtual_Networking) webinar.
