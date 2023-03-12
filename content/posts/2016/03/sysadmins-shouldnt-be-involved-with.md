---
date: 2016-03-22 08:56:00+01:00
dcbgp_tag: server
multihoming_tag: server
series:
- dcbgp
- multihoming
series_weight: 700
tags:
- data center
- BGP
title: Sysadmins Shouldn’t Be Involved with Routing
url: /2016/03/sysadmins-shouldnt-be-involved-with.html
---
I had a great chat with [Enno Rey](https://twitter.com/Enno_Insinuator) the morning before [Troopers 2016](https://www.troopers.de/troopers16/) started in which he he made an interesting remark:

> I disagree with your idea of running BGP on servers because I think sysadmins shouldn't be involved with routing.

As (almost) always, it turned out that we were still in violent agreement ;)
<!--more-->
We quickly agreed that [running OSPF on servers is a patently bad idea](https://blog.ipspace.net/2016/03/dont-run-ospf-with-your-customers.html), and expecting hosts to act as peers in network path calculations is another one.

Then there's the gray area of hypervisor connectivity. Like it or not, hypervisors are really the new network edge, and you can link them with the physical networks in one of three ways:

-   You pretend they aren't there, and give them simple IP connectivity which they can use to build whatever-over-IP tunnels (aka *overlay virtual networking*);
-   You allow them to dump [whatever \*\*\*\* they have into the network](https://blog.ipspace.net/2011/12/vmware-vswitch-baseline-of-simplicity.html) and deal with the consequences (aka *VLAN-based virtual networking*);
-   You accept them as the new network edge and start treating them as PE-routers (the [*Project Calico* way](https://blog.ipspace.net/2015/06/project-calico-is-it-any-good.html)). Unfortunately, this approach works well only when you can enforce the residential ISP mentality in your service offering (*Here's your IP address, take it and stop complaining. And no, you cannot move it*), otherwise you're quickly stuck in a quagmire of host routes or end-to-end paths (VLANs, tunnels or LSPs).

However, coming back to the original question: Should we run a routing protocol on a regular (application) server? As I said, I don't think we should... and yet I'm advocating running BGP on those same servers. I must be confused, right?

Not really. BGP (at least in that particular use case) is not a routing protocol (as in *figuring the best end-to-end path* tool), but a service advertisement protocol -- a host is advertising its service (encoded in an IP address because some people still can't spell DNS) and receiving default route (or not even that) in return. While doing that you're also solving the host multihoming problem (more about that in another blog post).

Assuming we can't fix the application code, so we're stuck with "IP address = service" paradigm, we could use a variety of tools to get that job done. BGP just happens to be a convenient one:

-   It fulfills the requirements (although you're admittedly using a cannon to kill a fly, but then virtual cannons are cheap);
-   It's available in many ToR switches (excluding greedy vendors who want to slap SP tax on everyone using BGP).
-   It's available in every Linux distribution (not sure about Windows Server, comments most welcome).

Finally, if you want to know how the whole thing works, watch the [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar; guest star Dinesh Dutt covered numerous implementation details in his part of the session.
