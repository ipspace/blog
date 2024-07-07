---
date: 2015-06-30 09:53:00+02:00
tags:
- data center
- cloud
- BGP
- IP routing
- virtualization
title: 'Project Calico: Is It Any Good?'
url: /2015/06/project-calico-is-it-any-good/
---
At least a dozen engineers sent me emails or tweets mentioning [Project Calico](http://www.projectcalico.org) in the last few weeks -- obviously the project is getting some real traction, so it was high time to look at what it's all about.

**TL&DR**: Project Calico is yet another virtual networking implementation that's a perfect fit for a particular use case, but falters when encountering the morass of edge cases.
<!--more-->
**What is Project Calico**? It's a virtual networking implementation for Linux, targeting high-density virtualization and container (Docker) environments. It comes with Neutron plug-in (and a few other plugins), making it immediately usable in OpenStack deployments.

**How does it work**? The virtual network is modeled as a single [microsegmented](/2015/03/microsegmentation-in-vmware-nsx-on/) flat VLAN with shared IP address space. *iptables* (packet filters implemented in Linux hosts) are used to implement tenant separation.

However, the creators of Calico know that a single flat VLAN doesn't scale, so they added an [interesting twist](http://docs.projectcalico.org/en/latest/datapath.html) almost identical to my [IPv6 microsegmentation](/2015/04/video-ipv6-microsegmentation/) ideas:

-   Every Linux host is an IP router running BGP;
-   Virtual machines (or containers) are attached to a virtual router, not a bridge (similar to what Juniper Contrail or [Microsoft Hyper-V](/2013/12/hyper-v-network-virtualization-packet/) are doing);
-   Host routes are used for end-to-end packet forwarding between customer endpoints and distributed between Linux hosts with BGP;
-   BGP route reflectors (also running on Linux hosts) are used to build a scalable routing control plane.

This architecture retains the properties of a flat layer-2 network (it's easy to move customer IP addresses between hosts), but scales much better -- the number of active endpoints on the layer-2 segment is equal to the number of physical hosts, not the number of virtual machines or containers.

The flooding across the physical layer-2 network is also reduced to a minimum. Unless you want to deploy IP multicast across customer workload, you won't see much more than ARP requests between physical hosts in the transport VLAN (it's highly unlikely that a hypervisor host remains silent for a long enough time to trigger unknown unicast flooding).

### The Obvious Problems

Project Calico uses a single microsegmented network, resulting in the [obvious drawbacks of microsegmentation](/2015/06/do-we-still-need-subnets-in-virtualized/):

-   **Single forwarding domain**, which makes [service insertion](/2014/02/service-insertion-with-openflow/) way harder to implement than multiple forwarding domains. You could (in theory) use *iptables* on Linux hosts to implement service insertion with PBR, but I'm positive I don't want to see the results or be involved in a troubleshooting session;
-   **Provider-coordinated IP addresses**. When multiple tenants share the same IP address space, someone has to coordinate the addresses, which means that you cannot simply migrate your existing workload into such a cloud (unless you're running new-age applications that rely exclusively on DNS and mechanisms like service registration and discovery);
-   **No overlapping IP addresses**. The creators of Project Calico recognized the problem and [proposed a "solution" using 464XLAT](http://docs.projectcalico.org/en/latest/overlap-ips.html) (emulating end-to-end IPv4 with a sequence of NAT46 and NAT64). I definitely wouldn't want to be anywhere nearby a cloud that uses this approach (see also RFC 1925, section 2.3);

If you're willing to accept these limitations, and offer cloud services where you force the tenants to use provider-supplied IP addresses (Amazon figured out years ago that they cannot do that), Project Calico might be a perfect fit for your private or public cloud... unless you want to build a scalable environment.

{{<note>}}I'm also wondering about the performance of the solution, as (based on my experience with virtual appliances) Linux IP stack isn't exactly the fastest IP forwarding mechanism in the universe, but maybe I'm wrong... or maybe few Gbps per host (which hopefully has 2 10Gbps uplinks) is [still ludicrous speed](/2015/02/performance-of-hypervisor-based-overlay/).{{</note>}}

### The Big Problems

The [router-in-hypervisor approach](/2011/04/vcloud-architects-ever-heard-of-mpls/) is definitely the right way to go (it's used by reasonably-scalable networks like [Amazon VPC](/2013/12/packet-forwarding-in-amazon-vpc/)), but the flat VLAN transport between hypervisor hosts kills the beauty of the concept for environments that need more than one or two switches -- you're forced to deploy fragile kludges like MLAG, proprietary layer-2 fabrics, or [concoctions that would make MacGyver proud](http://docs.projectcalico.org/en/latest/l2-interconnectFabric.html).

{{<note>}}Do I have to emphasize yet again that [every layer-2 domain represents a single failure domain](/2012/05/layer-2-network-is-single-failure/) and that [it inevitably fails sooner or later](/2015/06/another-spectacular-layer-2-failure/)?{{</note>}}

Alternatively, you could use a real IP fabric and dump all host routes into physical switches using BGP between hypervisor hosts and physical switches... and kill scalability because you'd become dependent on the L3 table sizes in physical switches.

Finally, you might decide to do route summarization on the ToR switches (resulting in an architecture very similar to my microsegmentation ideas), which seems to be the [next step that the Project Calico engineers are thinking about](http://docs.projectcalico.org/en/latest/l3-interconnectFabric.html), but then you'd lose the ability to migrate VMs... or you might get really smart and advertise out-of-rack host routes and summarize the in-rack routes.

### Can It Be Fixed?

Of course it might be possible to fix the Project Calico architecture to support true multi-tenancy and multiple routing domains:

-   Use overlay virtual networks to decouple hypervisor-based packet forwarding from the transport network;
-   Replace simple BGP with MPLS/VPN or EVPN.

If this description sounds a lot like an existing product, you're absolutely right. Fixing Project Calico to address the not-so-very-insignificant corner cases would turn its architecture into something very close to Juniper Contrail.

Unfortunately, I don't expect to see anything along these lines anytime soon. It's relatively easy to take existing open-source components and add some glue; writing a proper multi-tenant control plane (using BGP or something else) from scratch is a totally different ballgame.

For another perspective on these same issues, read the [blog post by Christopher Liljenstolpe](http://www.projectcalico.org/when-you-view-a-scale-out-network-through-a-1990s-enterprise-lens/), the original architect of Project Calico.
