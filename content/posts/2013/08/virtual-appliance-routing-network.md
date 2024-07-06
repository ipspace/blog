---
anycast_tag: use
date: 2013-08-29 10:14:00+02:00
lastmod: 2023-02-01 13:35:00
series:
- anycast
tags:
- firewall
- data center
- IP routing
- virtualization
title: Virtual Appliance Routing – Network Engineer’s Survival Guide
url: /2013/08/virtual-appliance-routing-network.html
---
Routing protocols running on virtual appliances [significantly increase the flexibility of virtual-to-physical network integration](/2013/06/dynamic-routing-with-virtual-appliances.html) -- you can easily [move the whole application stack across subnets or data centers](/2013/05/simplify-your-disaster-recovery-with.html) without changing the physical network configuration.

Major hypervisor vendors already support the concept: VMware NSX-T edge nodes can run BGP or OSPF[^NSXV], and Hyper-V gateways can run BGP. Like it or not, we'll have to accept these solutions in the near future -- here's a quick survival guide.
<!--more-->

[^NSXV]: For a trip down the memory lane, read the _[Routing Protocols on NSX Edge Services Router](/2013/08/routing-protocols-on-nsx-edge-services.html)_ blog post that describes VMware NSX-V implementation.

### Don't Use Link-State Routing Protocols

Link-state routing protocols rely on shared topology database flooded between participating nodes (routers). The whole link state domain is a single trust zone -- a single node going bonkers can bring down the whole domain.

**Conclusion:** don't use link-state routing protocols between mission-critical physical network infrastructure and virtual appliances. BGP is the only safe choice.

### Peer With a Cluster of Route Servers

BGP configuration of a virtual appliance or a physical network device shouldn't have to change when the application stack fronted by the virtual appliance moves into a different subnet. The virtual appliances should therefore peer with route servers using fixed neighbor IP addresses[^MIGT].

[^MIGT]: VMware NSX-T solves this with preconfigured BGP sessions between bare-metal edge nodes and adjacent ToR switches. There are no BGP sessions between virtual appliances and physical world -- IP prefixes of all applications stacks using an edge node are advertised by that edge node.

Here's an anycast design that ensures a virtual appliance always finds a path to a route server regardless of where it's moved to:

-   Assign the same IP address to loopback interfaces of multiple BGP route servers and advertise these addresses with varying IGP costs (or you might get interesting results when ECMP kicks in ;). Obviously you'd use two anycast IP addresses for redundancy.
-   When a virtual appliance establishes a session with the closest BGP route server, it announces its prefixes with the BGP next hop set to the physical IP address of the appliance. Assuming you run IBGP between your physical nodes, all routers in your data center get optimal routing information.

The route servers obviously have to accept BGP sessions coming from a range of IP addresses -- _dynamic BGP neighbors_ are a perfect solution.

{{<note info>}}If the routers or layer-3 switches you use don't support dynamic BGP neighbors, use Cisco's Cloud Services Router  or a Linux virtual machine running FRR as a route server.{{</note>}}

For even more details, read the [Running BGP between Virtual Machines and Data Center Fabric](/2022/02/bgp-on-virtual-machines.html) blog post.

### EBGP or IBGP?

I would usually recommend running EBGP between your network and a third-party appliance, but IBGP might turn out to be simpler in this particular case:

-   If you want to peer with a cluster of route servers you need multihop BGP sessions[^BME]. IBGP sessions are multihop by default, and some virtual appliances/gateways might not support multihop EBGP sessions[^IBGPS].
-   IBGP sounds more complex (you need route reflectors), but it's usually perfectly OK to advertise the default route to the virtual appliance ... or you might decide to use DHCP-based default routing in which case you don't have to send any information to the virtual appliance.
-   IBGP allows you to use MED and local preference to influence route selection if necessary.

[^BME]: Running direct EBGP sessions between bare-metal VMware NSX-T edge nodes and adjacent ToR switches is obvious perfectly fine

[^IBGPS]: OTOH, some virtual appliances or virtual network edge nodes might not support IBGP. Sometimes [you just can't win](https://wiki.c2.com/?YouJustCantWin).

### Don't Trust, Verify

You wouldn't want just any VM that happens to be connected directly to a physical VLAN to have BGP connectivity to your route servers, would you? Use MD5 authentication on dynamic BGP sessions.

Likewise, you probably don't want to accept routes at face value from untrusted nodes. Filter BGP updates received from virtual appliances, and accept only prefixes from specific address range assigned to virtual appliances having specific subnet size (for example, /64 in IPv6 world or /32 to /29 in IPv4 world).

### Need More Information?

* [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinar includes a deep dive into BGP routing between NSX-T edge nodes and physical fabric.
* [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar describes BGP routing between AWS and external destinations as well as BGP routing between AWS transit gateways and virtual appliances.
* [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) describes BGP routing between Microsoft Azure and external destinations as well as BGP routing between Azure Route Server (or Virtual WAN) and virtual appliances.

### Need Help with Your Network Design?

Check out my [BGP case studies](https://www.ipspace.net/ExpertExpress_Case_Studies) that you get with the [yearly subscription](http://www.ipspace.net/Subscription).

### Revision History

2023-02-01
: * Added several reference to NSX-T 
  * Explained the difference between routing with virtual appliances and bare-metal edge nodes
  * Streamlined the discussion with reordered sections
