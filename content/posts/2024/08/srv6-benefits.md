---
title: "Repost: The Benefits of SRv6"
date: 2024-08-20 07:44:00+0200
tags: [ segment routing, IPv6 ]
---
_I love bashing SRv6, so it's only fair to post a (technical) counterview, this time coming as a [comment from Henk Smit](https://blog.ipspace.net/2024/07/bgp-evpn-vxlan-srv6/#2343)._

---

There are several benefits of SRv6 that I've heard of.
<!--more-->
1. You'll have one address space for addresses and labels. Some people like that.
2. You have network programmability inside your SIDs. You can do stuff like NFV, etc. I have no idea how many networks really use this.
3. You can have non-SRv6 speakers in your SRv6 network. As the destination-addresses, which are SIDs/locators, are still just IPv6-addresses, any router that does IPv6 but not SRv6, can still be deployed in your SRv6 network.

    Personally I don't care about that reason. I really dislike it when a nice clean new technology gets mucked up, just so it is a bit easier to migrate an existing network. The migrations will be finished within a few years. And then you have those ugly details and hacks remaining for the next 3 decades.

4. You can summarize locators.

This is the big benefit in my eyes. We know how to build a network with a 1000 or so routers, in one IGP domain. But once we go bigger, things are not trivial anymore. We can use BGP to glue parts of the network together. We can divide an IGP into areas. But that causes other problems or inefficiencies. E.g. if you do SR-MPLS, what MPLS labels are your L1L2 routers gonna advertise? They'll need to advertise all MPLS labels for all the loopbacks in the L1 area. And the other way around (L2->L1) is even worse (even more loopbacks). We can not (really) summarize MPLS labels in the control plane. And we sure as hell can not summarize MPLS labels in the dataplane.

With SRv6, this problem is solved. The L1L2 routers can summarize not only the regular prefixes in the area, but also the locators, the flex-algo locators, etc. The only remaining problem is when BGP-speakers expect to see /32s (or /128s) for every peer they talk to. There are no elegant solutions for this yet, so it would be the next problem to fix.

You probably don't care about summarizable locators, or networks with 10k+ routers. But in the end: "the only problem is scalability". (I though that was a quote from Randy Bush. But Google can't find it. So not sure)[^TQ]. My big interest in my career has been scalability in routing protocols. (And performance, robustness and convergence, as they are all closely related). So I like it when SRv6 locators can be summarized.

[^TQ]: It's probably a quote from Mike O'Dell from his [May 16th, 2000 lecture](https://www-users.cse.umn.edu/~odlyzko/isources/odell-transcript.txt).

Or maybe someone with a lot of cash to spend on new routers can ask their supplier for summarizable MPLS labels? :) In today's companies, nobody will listen to a simple engineer as myself. But if a large ISP or hyperscaler, with a fat wallet, asks for something, that could make a difference. :) But then, nobody asked for summarizable MPLS labels during the last 25 years, so I expect nobody will any time soon.

---

To recap, the only good reason to use SRv6 is to eliminate hierarchical MPLS (or is it seamless MPLS?). Is that worth the effort (and the investment into new ASICs)? I don't know.

Also, I'm still persuaded that using NSH or SRv6 to implement service insertion is not much better than VLAN chaining, but of course, you're most welcome to leave a pointer to a real-life (as opposed to PowerPoint-based) counterexample in the comments.