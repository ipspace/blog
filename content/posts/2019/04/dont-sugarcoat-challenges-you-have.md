---
date: 2019-04-03 08:18:00+02:00
dcbgp_tag: rant
evpn_tag: rant
series:
- dcbgp
tags:
- BGP
- EVPN
title: Don’t Sugarcoat the Challenges You Have
url: /2019/04/dont-sugarcoat-challenges-you-have.html
---
Last year I got into somewhat-heated discussion with a few engineers who followed the advice to [run IBGP EVPN address family on top of an EBGP underlay](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics).

My main argument was simple: this is not how BGP was designed and how it's commonly used, and twisting it this way requires a schizophrenic BGP routing process, which introduces unnecessary complexity (even though it [looks simple in Junos configuration](https://blog.ipspace.net/2018/05/dissecting-ibgpebgp-junos-configuration.html)) and might confuse people who have to run the network after the brilliant designer is gone.
<!--more-->
What I got in return were personal attacks, an anonymous troll that was delighting everyone with a daily dose of irrelevance, but also a series of reasoned technical justifications that I still have a hard time buying.

> Junos could do whatever you want it to do

... so why don't you use the simplest possible approach that we used forever (IBGP+IGP) or two address families over EBGP?

> ... but if I add a new address family to a running fabric, it brings down my EBGP sessions.

Really? And you planned to add a new address family during prime time? I would think that turning on EVPN is a bigger risk than disrupting a BGP session and would use a maintenance window in which case I don't care if a BGP session goes down... and I have more than one leaf-to-spine connection anyway. Also, this might be a good moment to practice non-disruptive changes using BGP graceful shutdown ;)

> ... and on top of that IBGP scales better.

There might be a detail I'm missing, but I don't believe that (apart from implementation differences) IBGP scales that much better. If anyone knows a good argument why optimally-implemented IBGP would work better than optimally-implemented EBGP *run on the same set of boxes* (ignoring route reflectors or route servers running in a virtual machine) please let me know.

{{<note>}}I had interesting discussions with people close to actual BGP code when researching this delicious can of worms, and got totally opposite claims, so it seems there's a significant difference in how BGP is implemented on different platforms.{{</note>}}

> ... and you can use a route reflector that's not a spine switch.

And what's wrong with using a route server with EBGP connections to leaf switches (so the leaf switch doesn't have split personality) instead of a route reflector?

Also, did you consider that you have to run that route reflector somewhere and that the compute nodes on which you run route reflectors become critical infrastructure? All this might be needed in humongous deployments, but probably not in 99% of the environments out there, for which the CPU and RAM available on the spine switches is probably good enough.

BTW, all Junos examples I've seen had spines acting as IBGP route reflectors (which wouldn't work in [optimally-implemented EBGP underlay](https://blog.ipspace.net/2018/06/is-ebgp-really-better-than-ospf-in-leaf.html) anyway).

> ... but this is just bad implementation of a good design.

Sure. How about those implementations (seen in live fabrics) that used different AS numbers on spine switches (making EBGP almost as bad as OSPF) just to get [IBGP-over-EBGP to work](https://blog.ipspace.net/2018/09/valley-free-routing-in-data-center.html) because [valley-free-routing](https://blog.ipspace.net/2018/09/valley-free-routing.html) interfered with their ideas?

In the meantime, a friend of mine who's been working with EVPN for years sent me this explanation:

> Once I was asked to use eBGP (on Junos) for the EVPN control plane, and we stumbled on an incredible amount of complexity, problems and bugs (mostly in the ASIC programming). Since then I always use iBGP for the control plane.

I'm positive Juniper fixed most of those issues in the meantime, and most other vendors had similar issues (for example, another vendor couldn't do EVPN in IBGP-over-OSPF design), but that's not the point of this blog post.

What I really hate is that we are loath to admit why we're making the choices we're making. I would totally respect a networking engineer telling me for example "*I use this design which might be more complex and/or less elegant or whatever* *due to implementation details of the software I work with. This design has been tested by the manufacturer and thus* *works better than the alternatives.*" How about "*I got burned once, and IBGP worked for me, so I'm not going to risk experimenting again?*" Why do we have to invent convoluted explanations trying to sugarcoat the real challenges we faced? Everyone has problems, every software has bugs, it's how you deal with them that matters. Be honest to yourself and others and don\'t try to justify working around technical limitations with made-up explanations.
