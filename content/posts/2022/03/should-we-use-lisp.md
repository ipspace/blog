---
title: "Should We Use LISP?"
date: 2022-03-10 08:21:00
tags: [ LISP, BGP ]
---
LISP started as yet-another ocean-boiling project focused initially on solving the "_we use locators as identifiers_" mess ([not quite](/2022/03/lisp-false-economy.html)), and providing scalable IPv6 connectivity over IPv4-only transport networks by adding another layer of indirection and thus yet again proving RFC 1925 rule 6a. At least those are the diagrams I remember from the early "look at this wonderful tool" presentations explaining for example how Facebook is using LISP to deploy IPv6 (more details in [this presentation](https://archive.nanog.org/meetings/nanog50/presentations/Tuesday/NANOG50.Talk9.lee_nanog50_atlanta_oct2010_007_publish.pdf)).

Somehow that use case failed to gain traction and so the pivots[^SLFP] started explaining how one can use LISP to solve IP mobility or IP multihoming or [live VM migration](/2011/06/inter-dc-ip-based-vmotion-with-lisp.html), or to implement IP version of conversational learning in Cisco SD-Access. After a few years of those pivots, I started dismissing LISP with a short "*[cache-based forwarding never worked well](/2022/02/cache-based-forwarding.html)*" counterargument.
<!--more-->
[^SLFP]: Also known as "solutions looking for a problem"

Looks like the team developing LISP came to the same conclusions. According to [Bela Varkony](/2022/02/cache-based-forwarding.html#1048):

> Nowadays [LISP] is used with reliable transport and full PubSub. There is no caching behavior at all. Each xTR has a full routing table.

Also, engineers with exposure to LISP (but no skin in the game) view it as an alternative to existing VPN control-plane mechanisms (smart people used it as replacement for DMVPN years ago). [Back to Bela](/2022/03/lisp-false-economy.html#1064):

> My view of LISP is not a solution for the global public Internet. In this aspect I agree, that it has a a lot of issues. I see a potential in LISP as a private overlay replacing MPLS VPN solutions with something that is better in performance and has a built-in support for multi-link mobility. In that environment LISP has a much better performance and scalability then BGP... I agree that in some aspect LISP is a kind of a next generation BGP when PubSub is used with reliable transport.

Time to go back to the first principles. In any VPN control plane solution you have:

* Egress edge nodes that collect local reachability information using MAC learning, DHCP/ARP/ND snooping, or routing protocols. Egress edge nodes advertise that information to some central repository
* (Hopefully redundant) central repository that distributes local reachability information received from the edge nodes to other edge nodes.
* Ingress edge nodes that receive information from one or more repository servers, select information they're interested in (based on local VPN configuration), compare it with local reachability information to deal with multihomed endpoints, and install the results into the forwarding table.

The above description applies equally well to L3VPN or EVPN BGP address families, PubSub LISP, or most SD-WAN implementations.

Bela is effectively saying "_LISP does this faster than BGP_" and even [mentions a reason or two](/2022/03/lisp-false-economy.html#1064):

> There it is a big advantage that there is no best path selection. So it is very fast for mobility.

Well, you still have to compare remote information with local information, but if you want to go down the path of "*the last update we received from the controller cluster is the one we believe*" I see no reason why the same mechanism couldn't be implemented in something like *BGP Lite* should that be a problem worth solving. Maybe we're due for another round of "_IS-IS is better than OSPF_" arguments that were somewhat justified just because the team writing IS-IS code for a major vendor happened to be slightly better than the team writing OSPF code (or so it was explained to me).

Back to LISP and BGP. There are still some things where BGP seems to be better than LISP. It looks like at least Cisco and Juniper implemented Route Target Constrained Route Distribution ([RFC 4684](https://datatracker.ietf.org/doc/html/rfc4684))[^FIX] whereas [Bela claims a corresponding feature is still missing in LISP](/2022/02/cache-based-forwarding.html#1062):

> The future opportunity is to use selective subscription in LISP. Then you can have a full control of destinations that are interesting for you. So you can still reduce the memory needs, you do not need to have a full routing table everywhere, but you will not suffer by the generic caching algorithm issues. Your LISP map-cache will be under your full control [...] Unfortunately, selective subscription implementation is lagging behind. But it might come soon...

Looking at all of the above, I have a funny feeling that we're dealing with another instance of [XKCD Standards](https://xkcd.com/927/). I'm not working with sufficiently-large-scale fabrics and will stick with BGP[^NXOS], if you decide to deploy LISP please let me know how it worked out.

[^FIX]: Or I got it all wrong, in which case please fix my ignorance (= write a comment) and I'll update the blog post.

[^NXOS]: Potentially avoiding [implementations that need up to 300 seconds to set up a BGP session with 2000 VNIs](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/vxlan/configuration/guide/b-cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-93x/b-cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-93x_chapter_0101.html#reference_j35_15m_yfb).