---
date: 2012-07-24 07:25:00+02:00
tags:
- bridging
- data center
- service providers
- WAN
title: The Difference between Metro Ethernet and Stretched Data Center Subnets
url: /2012/07/the-difference-between-metro-ethernet/
---
Every time I rant about [large-scale bridging](/2012/05/layer-2-network-is-single-failure/) and [stretched L2 subnets](/2011/11/busting-layer-2-data-center/), someone inevitably points out that Carrier (or Metro) Ethernet works perfectly fine using the same technologies and principles.

I won't spend any time on the "_perfectly fine_" part, but focus on the fundamental difference between the two: the use case.
<!--more-->
### Typical Metro Ethernet Use Case

Engineers who know what they're doing connect individual sites to Metro Ethernet services with layer-3 devices (some others will [eventually figure it out](/2009/05/vpls-is-not-aspirin/) after a meltdown or two).

{{<figure src="/2012/07/s500-MetroEthernet.png">}}

It doesn't matter whether you call the site edge devices routers or switches, they perform several critical functions:

-   They split the *inside* (your site) and the *outside* (service provider transport network) into two separate L3 subnets and two failure domains;
-   They run routing protocols. Other devices attached to the same Metro Ethernet service can thus figure out whether a site is reachable or not;
-   They can find alternate paths (if they exist) after a link or service failure.

In principle, the routers connecting your sites to a Metro Ethernet service treat that service as one of the potential transport networks, and can use the routing protocols or BFD/CFM to figure out when the Metro Ethernet service is gone even if the local link status doesn't change.

Worst case, if the Metro Ethernet service falls apart, and you've provisioned backup links, your sites can still communicate with each other. If the Metro Ethernet service experiences a severe meltdown, the hosts inside your sites will not be affected (the routers might be due to heavy CPU load induced by broadcasts received from Metro Ethernet LAN).

**Summary**: it's perfectly safe to use layer-2 transport network as long as you terminate it with a layer-3 device.

### Typical Stretched Data Center Subnet Use Case

Hosts are directly attached to stretched layer-2 subnets (VLANs) in a typical layer-2 data center interconnect design, as shown in the next diagram.

{{<figure src="/2012/07/s450-L2DCI.png">}}

The servers (IP hosts) attached to stretched VLANs usually have no routing intelligence; all they know are two simple rules:

-   If the destination IP address belongs to the same subnet, use ARP to find the MAC address of the other host, and send the IP packet to that MAC address. If the ARP request fails, the other host is unreachable.
-   Otherwise, send the IP packet to the IP address of the default gateway.

The lack of routing intelligence in typical servers is not a software/OS issue. [Linux](http://lartc.org/howto/lartc.dynamic-routing.html) and [z/OS](http://www-03.ibm.com/support/techdocs/atsmastr.nsf/WebIndex/PRS1708) support routing daemons, and so did [Windows Server 2003](http://technet.microsoft.com/en-us/library/cc758016(v=ws.10)) until it got lobotomized (around the time of Windows Server 2008). However, it seems many engineers think [naked singularity](http://en.wikipedia.org/wiki/Naked_singularity) would materialize and gobble up their whole data center if they configured a routing protocol on a server (hint: [EBGP is better than OSPF](/2013/08/virtual-appliance-routing-network/)).

Typical IP hosts have no means of detecting the VLAN failure or partitioning, and cannot find alternate paths. They rely on network devices providing the connectivity, and with no layer-3 intelligence in the path, there's [only so much the networking devices can do](/2010/07/bridging-and-routing-is-there/).

The layer-2 data center interconnect thus becomes the most critical part of the whole data center infrastructure -- if it breaks, everything else stops working ([assuming the servers or VMs in the same subnet are on both ends of the failure](/2011/06/stretched-clusters-almost-as-good-as/)). Is that a good idea? Not in my book.
