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

{{<long-quote>}}
To recap, the only good reason to use SRv6 is to eliminate hierarchical MPLS (or is it seamless MPLS?). Is that worth the effort (and the investment into new ASICs)? I don't know.

Also, I'm still persuaded that using NSH or SRv6 to implement service insertion is not much better than VLAN chaining, but of course, you're most welcome to leave a pointer to a real-life (as opposed to PowerPoint-based) counterexample in the comments.

Anyway, in a follow-up comment, [Henk explained](https://blog.ipspace.net/2024/07/bgp-evpn-vxlan-srv6/#2345) what he meant with "network programmability within a SID".
{{</long-quote>}}

The 2nd argument requires a bit more knowledge about SR6v. Remember, SRv6 locators are just IPv6 addresses. An operator reserves a prefix to cut locators out. So suppose they assign a /48 for the locators. Lets say we use 1:2:3::0/48. Then you need to cut individual locators for each router. Let's take 16 bits for that. So now the locator for router N is 1:2:3:N::/64. Now you want to assign locators for flex-algos. Let's use 8 bits for that. So the locator for router N, flex-algo F is: 1:2:3:N:F0::/72. That's it. That's the bits you need for SRv6 routing.

But you still have the last 56 bits that are zeros. Unused. You could use them. The idea is that you can but "instructions" into those 56 bits. An operator and a parameter. Or an operator and two parameter. And you might be able to fix more than one instruction in those 56 bits. The instructions could be: "this packet needs to go through a firewall". Or "this packet needs to go through NAT". I don't know much about real world application, but that is the idea.

You're not gonna be able to do this with SR-MPLS. With SR-MPLS you get 20 bit address-space. And that is it. Not enough to do fancy things. (Unless you go stack a shitload of labels, maybe).

{{<long-quote>}}
Finally, SRv6 headers take more space than MPLS labels, potentially resulting in hardware limitations (number of SIDs you can insert into a packet). However, [according to Henk](https://blog.ipspace.net/2024/07/bgp-evpn-vxlan-srv6/#2346), you might not need more than a few SIDs.
{{</long-quote>}}

For TI-LFA 2 SIDs is usually enough (for the P-node and the Q-node). For uloop-avoidance, 1 or 2 SIDs, is usually enough. For VPNs you might need 2 SIDs. Only for real TE you might need more. I've heard in the real world, have 2-3 SIDs is usually enough for TE. Also, I think MTUs are huge these days. So the overhead of a few SIDs doesn't matter. The only issue is how many SIDs can a router deal with itself? (I have no idea, tbh. I am not a hardware guy).

---

Comments? Counterarguments? You know where to leave them ;)
