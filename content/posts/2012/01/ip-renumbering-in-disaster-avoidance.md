---
date: 2012-01-20 12:03:00+01:00
dr_tag: stretch
high-availability_tag: dr
lastmod: 2020-11-17 16:49:00
series:
- dr
tags:
- data center
- load balancing
- virtualization
- high availability
title: IP Renumbering in Disaster Avoidance Data Center Designs
url: /2012/01/ip-renumbering-in-disaster-avoidance/
---
It’s hard for me to admit, but there just might be a [corner use case for split subnets and inter-DC bridging](/2011/08/quotes-of-week/): even if you move a cold VM between data centers in a controlled disaster avoidance process (moving live VMs [rarely makes sense](/2011/09/long-distance-vmotion-for-disaster/)), you [might not be able to change its IP address](http://www.yellow-bricks.com/2012/01/19/avoid-changing-your-vms-ip-in-a-dr-procedure/) due to hard-coded IP addresses, be it in application code or configuration files.

Disaster recovery is a different beast: if you’ve lost the primary DC, it doesn’t hurt if you instantiate the same subnet in the backup DC.
<!--more-->
However, before jumping headfirst into a misty pool filled with unicorn tears (actually, a [brittle solution](/2011/12/large-scale-l2-dci-true-story/) with too many moving parts that [usually makes no sense](/2011/11/busting-layer-2-data-center/)), let’s see if there are alternatives. Here are some ideas in exponentially decreasing order of preference:

**Ever heard of DNS?** If the application uses hardcoded addresses in its clients or between servers, there’s not much you can do, but one would expect truly hardcoded addresses only in home-brewed craplications ... and masterpieces created by those “programming gurus” that never realized *hostnames* should be used in configuration files instead of *IP addresses*.

If your application is somewhat well-behaved, there are all sorts of [dynamic DNS](http://en.wikipedia.org/wiki/Dynamic_DNS) solutions that you can use to automatically associate server’s new IP address with its DNS FQDN. [Windows clusters do that automatically](/2011/06/multisite-clusters-done-right-by-none/), many DHCP servers automatically create dynamic DNS entries after client address allocation, and there are [numerous Linux clients](http://dyn.com/support/clients/linux/) that you can use even with static IP addresses.

{{<note>}}Use low TTL values if you’re changing DNS records, or the clients won’t be able to connect to the migrated servers due to stale local DNS caches.{{</note>}}

**Host routes?** For whatever reason some people think host routes are worse than long-distance bridging. They’re not – if nothing else, you have all the forwarding information in one place ... and modern L3 switches use hosts routes for directly connected IP hosts anyway.

Automatic network-side configuration of host routes is mission impossible. [Local Area Mobility (LAM) worked years ago](/2011/02/local-area-mobility-lam-true-story/), but was not supported in data center switches until Cumulus Networks reinvented it with [Redistribute ARP](/2015/08/layer-3-only-data-center-networks-with/). 

{{<note info>}}As of late 2020, most data center switching vendors support some variant of routing on IP host addresses in their EVPN implementations. For more details, watch [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.{{</note>}}

... and the only other mechanism I could think of that wouldn’t involve loads of homemade scripting glue is [OpenFlow-driven RIB modification supposedly working on Juniper MX routers](/2011/11/openflow-deployment-models/).

**Routing protocols?** Routing protocols running on servers were pretty popular years ago (that’s how [IBM implemented IP multipathing on mainframes](http://www-03.ibm.com/support/techdocs/atsmastr.nsf/WebIndex/PRS1708)). Instead of configuring hardcoded IP address on server’s LAN interface, configure it on a loopback, and [run BGP between servers and adjacent ToR switches](https://my.ipspace.net/bin/list?id=Clos#ROUTING_SERVERS)... and whatever you do, [please don't use OSPF](/2013/08/virtual-appliance-routing-network/). Some IBM mainframes were a single link failure away from becoming the core data center router.

Yeah, I know, a stupid solution like this requires actual changes to server configurations ... and it’s so much easier to pretend the problem doesn’t exist and claim that the network should support whatever we throw at it ;)

**Route Health Injection on load balancers?** Same idea as server-side routing protocols, but implemented in front of the whole application infrastructure.

Assuming your application sits behind a load balancer and you’re doing a cold migration of all application components in one step, you can preconfigure all the required IP subnets in the disaster recovery site (after all, they’re hidden behind a load balancer) and rely on the load balancer to insert the publicly visible route to the application’s public IP address once everything is ready to go.

**The universal duct tape – NAT**. If the clients use DNS to connect to the servers, but the servers have to use fixed IP addresses, use NAT to hide server subnets behind different public IP addresses (one per site).

Obviously you have to move the whole application infrastructure at once if you want to use this approach or things will break really badly.

Apart from the usual NAT-is-bad and NAT-breaks-things mantras, there are a few additional drawbacks:

-   Clients have to rely on changed DNS records as you cannot insert a host route into the outside network like a load balancer can with RHI.
-   NAT devices usually don’t support dynamic DNS registration, so you have to change the DNS entries “manually”.

**Virtual appliances?** Duncan Epping [proposed using vShield Edge as a NAT device](http://www.yellow-bricks.com/2012/01/19/avoid-changing-your-vms-ip-in-a-dr-procedure/). 

While that idea didn't sound so great when I wrote the original blog post, that's how most overlay virtual networks implement overlay-to-physical gateways, and at least VMware decided to [use BGP as the only routing protocol in this scenario](/2013/06/dynamic-routing-with-virtual-appliances/).

**Anything else?** I’m positive I’ve missed an elegant idea or two. Your comments are most welcome ... including those telling me why the ideas mentioned above would never be implementable.

### Revision History

2020-17-11
: Cleaned up the blog post, removed references to LISP VM mobility, and inserted pointers to routing based on host IP addresses, and running BGP on servers.