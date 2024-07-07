---
date: 2018-09-06 09:56:00+02:00
dcbgp_tag: abstract
series:
- valley-free
- dcbgp
tags:
- design
- BGP
- IP routing
title: Valley-Free Routing
url: /2018/09/valley-free-routing/
---
Reading academic articles about Internet-wide routing challenges you might stumble upon *valley-free routing* – a pretty important concept with applications in WAN and data center routing design.

If you’re interested in the academic discussions, you’ll find a pretty exhaustive list of papers on this topic in the *Informative References* section of [RFC 7908](https://tools.ietf.org/html/rfc7908); here’s the over-simplified version.
<!--more-->
### The Challenge

Imagine a typical multi-layer somewhat-hierarchical routing structure. It could be a hierarchical WAN design, data center fabric, or the global Internet (we’ll focus on the latter in this blog post). You’d expect the traffic to flow from the source leaf node up the layers until it hits a path toward the destination leaf node where it makes a turn and starts flowing down the layers until it gets to the destination leaf node.

{{<figure src="/2018/09/s550-VF_Ideal.png" caption="Correct traffic flow">}}

Unfortunately life isn’t always as neat and tidy. For example, a dual-homed customer could create a route leak due to incompetence or fat-finger incident and become a transit AS between *ISP Left* and *ISP Right*. Assuming our understanding of routing hierarchy is correct, the traffic from *Customer-A* toward *Customer-B* goes uphill, **then dips into a valley** (*dual-homed customer*), goes uphill again, and finally goes downhill to reach *Customer-B*.

{{<figure src="/2018/09/s550-VF_Valley.png" caption="Entering a valley due to a route leak">}}

**Loose definition**: A routed network with no traffic flow valleys for any source-destination pair has *valley-free routing*.

### Removing the Valleys

Two mechanisms are commonly used to remove traffic flow valleys from a hierarchical network:

-   If you can’t influence the routing protocol policies, install a peer link between elements at the same hierarchical level to create a lower-cost path than a path through the valley.

{{<figure src="/2018/09/s550-VF_PeerLink.png" caption="Removing a valley with a peer link">}}

-   Ideally, you’d use routing protocol policies to stop (or at least discourage) route leaks that result in traffic flow valleys. As explained in tedious details in [RFC 7454](https://tools.ietf.org/html/rfc7454), the two ISPs in our example should filter transit routes received from their shared customers. In an environment that favors reachability over stability or predictable traffic patterns, a better solution might be to increase the cost (or reduce local preference) of routes that would result in traffic flow valleys.

{{<figure src="/2018/09/s550-VF_RouteFilters.png" caption="Removing a valley with route filters">}}

### Getting Formal

I’m positive at least one of the academic papers listed in RFC 7908 contains a rigorous definition of valley-free routing (pointers welcome); here’s a pretty loose attempt:

Assuming we can assign hierarchical *level* to network nodes such that the core nodes have the lowest level and the edge nodes have the highest level, a valley-free traffic flow traverses nodes in non-increasing order of levels until it reaches the innermost node, at which point it starts traversing nodes in non-decreasing order of levels.

Here’s an alternative definition assuming we can figure out the contractual relationships between autonomous systems (good luck with that):

-   Number links between autonomous systems as (+1,0,-1) for (provider, peer, customer).
-   A valley-free path has a sequence of +1s, followed by at most one 0, followed by a sequence of -1s.

{{<note info>}}Interesting in graph applications in networking? Check out [*Network Connectivity, Graph Theory, and Reliable Network Design*](https://www.ipspace.net/Network_Connectivity,_Graph_Theory,_and_Reliable_Network_Design) webinar by [dr. Rachel Traylor](https://www.ipspace.net/Author:Rachel_Traylor).{{</note>}}

Assigning hierarchical levels to network nodes is a fun problem to solve. You could do it manually, automate the process, or try to deduce node’s level in the hierarchy based on its surroundings – [RIFT](/2018/03/data-center-routing-with-rift-on/) and [OpenFabric](/2018/04/openfabric-with-russ-white-on-software/) are both trying to do that to enable plug-and-pray fabric autoconfiguration.

The challenge is relatively easy to solve if you’re allowed to label the core (or edge) nodes. This is how you could do it in the Internet case:

-   Assume we could agree on a list of Tier-1 providers;
-   Anyone connected to Tier-N provider is Tier-N+1 provider;
-   Anyone at tier N not having a connection to a tier N+1 network is an edge node. Whether they want to be called *customers* is not a technical question ;)

The real fun starts when you’re trying to figure out the hierarchical levels of network elements based solely on network topology… and you have to deal with peer links on any level of hierarchy.

Anyways, I’m an old-school micromanager and prefer to have a structured network design and automated deployment. If you’re like me, you’ll find a [data center fabric automation use case](https://my.ipspace.net/bin/list?id=NetAutUC#CS_DC_FABRIC) by Dinesh Dutt in [Network Automation Use Cases](https://www.ipspace.net/Network_Automation_Use_Cases) webinar, deep dive into the tool he used in [*Ansible for Networking Engineers*](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar… or you could go for a [full-blown course on designing, developing and deploying a network automation solution](https://www.ipspace.net/Building_Network_Automation_Solutions).
