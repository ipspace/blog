---
date: 2015-06-25 08:10:00+02:00
distributed-systems_tag: sdn
series:
- distributed-systems
series_weight: 1200
tags:
- SDN
- OpenFlow
title: More on Centralized Control and SDN
url: /2015/06/more-on-centralized-control-and-sdn.html
---
After I wrote a [comment on a LinkedIn discussion](https://www.linkedin.com/grp/post/77819-6014408274856722434) in the [Carrier Ethernet group](https://www.linkedin.com/grp/home?gid=77819) ([more details here](https://blog.ipspace.net/2015/06/centralized-control-is-not-centralized.html)), [Vishal Sharma](http://www.linkedin.com/in/vishalsharma) wrote an interesting response, going into more details of distinction between *centralized control* and *centralized control plane*.
<!--more-->
He started with a nice summary of my view:

> What I understood from what you is that it is ok to have a centralized entity to have (to use a much overused phrase) a \"single pane of glass\" view of the network. And, presumably, the central controller may have obtained this view by amalgamating inputs from various sources.

Couldn't agree more. Numerous [SDN architectures](https://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations) use this approach.

> Could it get the control plane details, for example, by acting as a peer of the CP running on the existing devices (switches/routers) in the network, so it has the same view of the network as they do, even if the control plane itself is not centralized in the controller per se?

That's exactly what many SDN solutions are doing.

Most of them use plain BGP, for example [Microsoft's data center solution](https://blog.ipspace.net/2013/10/exception-routing-with-bgp-sdn-done.html) (see [Centralized Routing Control in BGP Networks Using Link-State Abstraction](https://tools.ietf.org/html/draft-lapukhov-bgp-sdn-00) for more details), [Netflix' traffic analysis solution](http://blog.ipspace.net/2014/08/toolsmith-netflix-on-software-gone-wild.html), or [Border6 Non-Stop Internet](http://blog.ipspace.net/2014/10/border6-non-stop-internet-commercial.html).

Some other solutions use BGP-LS ([North-Bound Distribution of Link-State and TE Information Using BGP](https://tools.ietf.org/html/draft-ietf-idr-ls-distribution-11)), for example [Juniper's NorthStar controller](http://www.juniper.net/us/en/products-services/sdn/northstar-network-controller/).

> A centralized control plane, on the other hand, is the notion that all of the control computations be centralized in a single entity, which then programs elements in the (distributed) forwarding/data plane. And, your thought is that this latter entity does not make sense in the real world.

It's not the notion of centralized computation that's problematic. After all, tools like Cariden MATE or Juniper's NorthStar controller use centralized computation, and you could argue that every BGP route reflector or route server (used by numerous Internet Exchange Points) do the same.

The real problem is in the *other tasks that the control plane has to do*, like detecting byzantine link failures, sending periodic messages to external devices, or running host-to-network protocols like ARP/ND. Those tasks don't scale.

> I have to admit that (if I understood what you said above correctly) this is certainly a contrarian viewpoint, since, for most people, SDN is about centralizing the control plane itself. Now, we do have the notion of a \"logically centralized\" control plane, but centralized none-the-less. So, some light on this would be much appreciated!

You might call my viewpoint contrarian, I call it realistic -- and almost everyone who had to build and ship a production-grade product agrees with me.

{{<note>}}For more details, go to the product-specific part of the [previous blog post on this topic](https://blog.ipspace.net/2015/06/centralized-control-is-not-centralized.html).{{</note>}}

The real problem (as I see it) is that people who talk about *centralized control plane* don't really understand all the implications of this concept. You either *have* centralized control plane (including all the complications I mentioned above and in the previous blog post) or you don't. You can't have it both ways.

You could, of course, offload the periodic control plane functionality to edge nodes, and still run central path computation. [Juniper's QFabric did exactly that](https://blog.ipspace.net/2011/09/qfabric-part-2-control-plane-overview.html), as did most Frame Relay, SONET/SDH and ATM networks. The [SDN Architecture](https://www.opennetworking.org/images/stories/downloads/sdn-resources/technical-reports/TR_SDN_ARCH_1.0_06062014.pdf) document from ONF mentions this approach (and the real-life scalability concerns) very explicitly in sections 4.2 and 4.3. Let me quote straight from section 4.3.4 of that document (which more-or-less says the same things I've been saying for years)

> Although a key principle of SDN is stated as the decoupling of control and data planes, it is clear that an agent in the data plane is itself exercising control, albeit on behalf of the SDN controller. Further, a number of functions with control aspects are widely considered as candidates to execute on network elements, for example OAM, ICMP processing, MAC learning, neighbor discovery, defect recognition and integration, protection switching.

> A more nuanced reading of the decoupling principle allows an SDN controller to delegate control functions to the data plane, subject to a requirement that these functions behave in ways acceptable to the controller; that is, the controller should never be surprised. This interpretation is vital as a way to apply SDN principles to the real world.

However, do keep in mind that the current set of tools you could use (primarily OpenFlow) doesn't include a standard way of delegating control (at least not in OpenFlow 1.5), so anyone who solved this problem did it using proprietary extensions.

### More to Explore

You might want to read my other [SDN](https://blog.ipspace.net/tag/sdn.html)- and [OpenFlow](http://blog.ipspace.net/tag/openflow.html)-related blog posts. For even more details, explore my [SDN webinars and other SDN resources](http://www.ipspace.net/SDN):

-   Start with the free [Introduction to SDN](http://www.ipspace.net/Introduction_to_SDN) pack;
-   Explore [SDN architectures](http://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations) and their scalability challenges;
-   Find out all the [details of the OpenFlow protocol](http://www.ipspace.net/OpenFlow_Deep_Dive);
-   Get 20+ hours of SDN and network automation content with [Advanced SDN training](http://www.ipspace.net/Advanced_SDN_Training).
