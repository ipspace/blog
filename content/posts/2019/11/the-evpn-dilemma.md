---
date: 2019-11-26 08:20:00+01:00
dcbgp_tag: rant
evpn_tag: rant
series:
- dcbgp
tags:
- bridging
- VXLAN
- EVPN
- WAN
title: The EVPN Dilemma
url: /2019/11/the-evpn-dilemma/
---
I got an interesting set of questions from a networking engineer who got stuck with the infamous "*[let's push the \*\*\*\* down the stack](/2013/04/this-is-what-makes-networking-so-complex/)*" challenge:

> So, I am a rather green network engineer trying to solve the typical layer two stretch problem.

I could start the usual "*[friends don't let friends stretch layer-2](/2012/05/layer-2-network-is-single-failure/)*" or "*[your business doesn't need that](/2013/01/long-distance-vmotion-stretched-ha/)*" windmill fight, but let's focus on how the vendors are trying to sell him the "perfect" solution:
<!--more-->
> One thing I hear over and over from everyone (vendors especially) is how EVPN will solve all of my problems.

Now and then vendors go on a lemming run promoting a miraculous technology. A few years ago, it was either TRILL or SPB (depending on which chipset you were trying to sell); now it's EVPN... which is a shame because EVPN is a decent technology.

The "*solving all your problems*" is the necessary component of this fairy tale. You would never buy from a vendor who would drop by and say, "*we can solve one of your problems, and you have to restructure your applications to get rid of the other 100*", right?

> All I need to do is ditch my current IGP in favor of BGP

[Another lemming run](/2017/11/bgp-as-better-igp-when-and-where/), this time along the lines of "*[if Petr Lapukhov did it at Microsoft it must be good](/2018/05/is-ospf-or-is-is-good-enough-for-my/)*". While you could get a pretty minimalistic and simple design if you make [BGP the only routing protocol in your fabric](https://www.ipspace.net/Data_Center_BGP/BGP_Fabric_Routing_Protocol), you better do that with an [implementation that was adapted to the new use of BGP](/2015/02/bgp-configuration-made-simple-with/), not decades-old code base that needs a gazillion of tweaks and just the right values of nerd knobs to make it work.

Oh, and some vendors [messed up their implementation really badly](/2019/04/dont-sugarcoat-challenges-you-have/), so they started promoting [IBGP-over-EBGP](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) (EVPN address family on IBGP sessions running between loopbacks advertised with IP address family on EBGP sessions running on point-to-point links) and [using schizophrenic **local-as** mechanisms](/2018/05/dissecting-ibgpebgp-junos-configuration/) just to make it work. Oh, and then another vendor told the customers to run EBGP sessions on point-to-point links to exchange loopback prefixes and *another set of multihop EBGP sessions* between the loopback interfaces of the same boxes to exchange the EVPN prefixes.

> ... and well, BGP is hard to configure, so I also need to invest in an automation solution.

That's another thing vendors are really good at - promoting the right stuff for the wrong reasons. Network automation is the right way to go, but if it's sold as the only way to build BGP configurations for your data center fabrics (because of the copious amount of nerd knob settings you need), you chose the wrong vendor.

There are vendors focusing on [making data center EVPN+BGP+MLAG configurations as simple as possible](/2019/10/auto-mlag-and-auto-bgp-in-cumulus-linux/), but they lack the marketing muscles of the big guys and glitzy customer events that CIOs love to mingle at. Just saying...

{{<note info>}}It\'s also worth mentioning that most open-source BGP products like BIRD and goBPG support similar BGP configuration simplifications as FRR, so it\'s not that hard to implement them.{{</note>}}

> One other thing... EVPN doesn't play well between vendors, so there's probably going to be lock-in.

Well, the vendors are telling me they're running interoperability workshops to make sure the least-common-denominator EVPN implementations interoperate. But honestly, why would you want to build your data center fabric with switches from two vendors?

Unless you're a [member of the FANG club](/2016/03/you-want-your-network-to-be-like/) (in which case you'd probably run your own software on top of standardized products from two sources anyway), you'll probably lose more money than you saved dealing with operational complexity of running two platforms with two operating systems (I would, however, avoid using proprietary vendor features as much as possible). It's like mixing AIX, Solaris, and Linux on your servers. Who would ever want to do that unless a database company forces them to do it due to their licensing and litigation practices?

> Oh and your current network equipment will need to be replaced as well.

Like when you're trying to figure out whether to buy a new car, you have two options:

-   Stick with the old stuff and live with the lack of features available in the new models;
-   Invest in the new model and get the new features.

Funnily, if you happen to have a decent-sized installation under a vendor support contract, it might be cheaper to ditch the old stuff and buy the new switches. We had customers who would make money just on that swap in a few years due to cheaper boxes and (consequently) lower support costs.

> What's the problem with a solution like GRE? I can leverage my current IGP, all of my equipment already supports it... and it works between vendors.

While there are plenty of vendors doing whatever-over-GRE (but maybe not on recent data center switches), and I\'m told at least some Broadcom ASICs support NVGRE (but [how would we know](/2016/05/what-are-problems-with-broadcom/)), I'm not aware of anyone shipping bridging-over-GRE in hardware. If you plan to stretch your layer-2 domain over 100 Mbps or 1 Gbps link (so you could use software-based forwarding), I have just one word for you: DON'T.

The question makes perfect sense once you replace GRE with VXLAN (see below).

> Maybe trying to "tunnel" away all of our problems is the wrong solution to begin with. What are your thoughts on this?

There's always RFC 1925 Rule 6A, but in the case of layer-2 segments [artificially stretched beyond recognition](/2018/01/revisited-need-for-stretched-vlans/) (= [beyond a single cable](/2019/04/commentary-were-stuck-with-40-years-old/)) tunneling makes perfect sense.

You could either try to bend the laws of physics and make bridging-with-STP work in an environment it was never designed for (what data center vendors tried to do with [large-scale MLAG](/2010/10/multi-chassis-link-aggregation-basics/) using proprietary technologies like VSS, vPC, IRF, VCF...), or you could give up, realize a routed fabric will always be more stable than a bridged hodgepodge, and start looking for a way to implement one.

In theory, you could build a routed fabric using MAC addresses (SPBM), yet another layer-3 protocol ([TRILL](/2010/07/why-is-trill-not-routing-at-layer-2/)), or IP (VXLAN). I would go for VXLAN, as we've been debugging IP routing protocols and IP forwarding for decades, and thus, they tend to work pretty well.

You could be smart and use VXLAN with preconfigured flooding lists and dynamic MAC learning (and I know people [doing that in large-scale environments with great success](/2018/03/could-we-build-ixp-on-top-of-vxlan/)), or you could buy into another vendor fairy tale that VXLAN with EVPN solves every problem you ever had.

Yet again, I'm not saying that EVPN is a flawed technology or that you wouldn't benefit from using it (it might be very handy in larger fabrics or if you still insist on stretching the VLANs across WAN links), but in some cases [the simplest solution is all you need](/2018/02/using-evpn-in-very-small-data-center/), and VXLAN on top of whatever IP routing protocol you're familiar with (even RIP would work) gets you pretty close to that goal.

### More Information

You might find these webinars (part of [ipSpace.net subscription](https://www.ipspace.net/Subscription/)) useful if you want to master the technologies I mentioned in this blog post:

-   [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers)
-   [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
-   [VXLAN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
-   [Data Center Interconnects](https://www.ipspace.net/Data_Center_Interconnects)
-   [Designing Active-Active and Disaster-Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)
-   [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics)
-   [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) (includes routing protocol selection)
-   [FRRouting Architecture and Features](https://www.ipspace.net/FRRouting_Architecture_and_Features)

These webinars and many more are included in our [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.

---

Many thanks to [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt) and [Nicola Modena](https://www.ipspace.net/Expert:Nicola_Modena) for fact-checking and improving the blog post.
