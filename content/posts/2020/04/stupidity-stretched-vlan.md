---
date: 2020-04-15 06:32:00+00:00
ha-cloud_tag: stretch
series_weight: 800
series:
- ha-cloud
tags:
- cloud
- vMotion
- bridging
- LISP
title: When All You Have Are Stretched VLANs...
---
Let's agree for a millisecond that you can't find any other way to migrate your workload into a public cloud than to [move the existing VMs one-by-one without renumbering them](/2020/02/the-myth-of-scaling-from-on-premises.html). Doing a clumsy cloud migration like this will get you the headaches and the cloud bill you deserve, but that's a different story. Today we'll talk about being clumsy the right and the wrong way.

There are two ways of solving today's challenge:
<!--more-->
* You could realize that your problem is **IP address mobility** and solve it by implementing routing on host IP addresses instead of routing on IP subnets ([turning IP into CLNP](/2015/05/reinventing-clns-with-l3-only-forwarding.html), but that's yet another story).
* You could take the shiniest hammer in your toolbox ([stretched VLANs implemented over L2VPN](/2020/02/live-vmotion-into-vmware-on-aws-cloud.html)) and use it no matter what problem you're trying to solve. It's so much fun attacking Phillips screws with a sledgehammer.

Let's start with the _IP routing on host addresses_ camp:

* At least one startup solved the challenge years ago (and had a shipping products).
* I know networking engineers who built their own solution (it's not that hard to do).
* Microsoft Azure productized it in two ways: [using LISP on CSR-1000V](https://github.com/microsoft/Azure-LISP), or using a [simpler solution that needs just two VMs and a bit of orchestration](/2019/11/stretched-layer-2-subnets-in-azure.html).

Then you have the vendors with shiny hammers (or engineers believing in _[Flat Ethernet Everywhere](/2011/09/large-scale-bridging-nuked-earth.html)_ mantra). The worst idea I've seen in this category is probably (now long gone) Nexus 1000v Intercloud - custom NICs in cloud VMs connecting to another cloud VM that acted as a virtual switch (linecard) for on-premises supervisor VM. Not surprisingly, it worked as reliably as trying to make a T-shirt out of spaghetti bolognese.

Slightly less convoluted is the [stuff VMware is promoting these days](/2020/02/live-vmotion-into-vmware-on-aws-cloud.html): stretched VLANs using L2VPN in NSX-T, which turns out to be Ethernet-over-GRE-over-IPsec. Not only are you exposed to the usual flooding fun and occasional forwarding loop (with the slight difference that now you're billed by the flooded packet by your friendly cloud vendor), you also have to deal with challenges like _local egress_ which was solved in NSX-V but is [still missing in NSX-T 2.x](/2019/08/brief-history-of-vmware-nsx.html), and _local ingress_ which is [mostly unsolvable](/2016/02/vmware-nsx-update-on-software-gone-wild.html) until you admit you have a _routing_ not a _bridging_ problem.

Not surprisingly, solving all these challenges with _routing on IP addresses_ approach is a breeze... apart from the minor detail that no sane ISP would ever carry your host routes, but of course you can use LISP to solve that problem and get [even better job security](/2013/09/sooner-or-later-someone-will-pay-for.html). After all, it's just routing as usual with few extra tricks (more about that in another blog post).

So why doesn't everyone use the same (seemingly sane) approach? As always, there are tradeoffs. All solutions based on IP routing give you _unicast IP_ communication. No multicast for cluster discovery, no weird protocols, no IP address sharing. The networking world would be a better place if we could limit ourselves to what makes sense, but when you start promising your customers a seamless migration of whatever \*\*\*\* they're running into a public cloud, you're bound to deal with a few weird cases.

And then there's another subtle challenge: when you [move a _running_ VM](/2020/03/the-myth-of-lossless-vmotion.html) into another subnet, it has ARP cache populated with MAC addresses from the old subnet, so it won't be able to reach anyone in the new subnet (including the first-hop router) unless you fake the MAC addresses somehow. Cue _one Ethernet to rule them all_ jingle. 

You could solve that challenge with [cold VM migration](/2013/02/hot-and-cold-vm-mobility.html) (shut down, move, restart), or with an agent running on the VM (VMware Tools comes to mind) that would flush the ARP cache and the routing table (if so instructed) after the hot VM move, but that would require actual coding and testing work. Sometimes it's much easier to write a marketing story to persuade everyone why using [an inferior and risky solution](/2012/09/dear-vmware-bpdu-filter-bpdu-guard.html) is so much better.

**Long story short**: as always, understand what problem you're trying to solve, find the best tool for the job, and use it correctly. Recycled and remarketed technologies (see RFC 1925 rule 11) might not be the best fit, regardless of how well they [look in PowerPoint](/2011/09/long-distance-irf-fabric-works-best-in.html) or work in demos.