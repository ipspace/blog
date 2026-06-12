---
title: "Goodbye, Leaf-and-Spine Networks?"
subtitle: Of course not
date: 2026-06-10 07:42:00+0200
tags: [ data center, fabric ]
lastmod: 2026-06-12 19:51:00+0200
---
A friend of mine sent me links to a [new paper published by AWS engineers](https://arxiv.org/abs/2604.15261), and an [associated LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7465785618414051328/) which claims:

> We got lean, resilient, massive aggregation fabrics that provide 33% better throughput with 69% fewer routers, savings 27% of costs, cutting power usage by 40%, and reducing CO2 emissions.

The obvious question one should ask after reading the hyperventilated [Radical Network Redesign](https://www.aboutamazon.com/stories/aws-random-graph-theory-data-center-network-design) blog post is thus: is this the end of leaf-and-spine networks? Of course not. Let's go into the details.
<!--more-->
{{<long-quote>}}
**Update:** In less than a day after I published the blog post, Giacomo Bernardi (one of the authors) reached out and provided the crucial bits of information I missed. I added them to the blog post (in gray boxes), reworded a few things a bit, and plan to do a more detailed follow-up.
{{</long-quote>}}

**What exactly did they do?** They rediscovered the way [Plexxi tried to build data center fabrics](https://blog.ipspace.net/2013/09/the-plexxi-challenge-or-dont-blame-tools/). Instead of spine switches, Plexxi tried to connect leaf switches directly, first with CWDM (they were dreaming about dynamic leaf-to-leaf bandwidth), later with a prewired middlebox (what AWS engineers call ShuffleBox). 

{{<long-quote>}}
While the idea is the same, AWS RNG wires switches differently. As the authors explained in the clarification they sent me, the Plexxi network was a *union of rings*; AWS RNG is an *optimal expander*.
{{</long-quote>}}

Obviously, you'd waste a lot of bandwidth that way, as there are always some leaf switches that do not exchange traffic even though they have a direct link. Plexxi solved that with unequal-cost multipathing (the traffic also uses longer paths, not just direct links); the AWS blog post calls that Routing through Randomness.

As anyone who has tried to understand [LFA](https://blog.ipspace.net/2012/01/loop-free-alternate-ospf-meets-eigrp/) knows, [unequal-cost multipathing](https://blog.ipspace.net/2021/03/ucmp-link-state-protocols/) only gets you so far. If you want further increases in link utilization, you need "proper" traffic engineering, which requires virtual circuits (and thus an extra layer of encapsulation). Whether you use MAC frames[^MF], MPLS, SRv6, or pigeons for that extra layer does not matter.

[^MF]: Using destination MAC address as virtual circuit ID. Sounds crazy, but I've seen crazier things.

**How could a prewired ShuffleBox be random?** Yeah, that was the first major trigger of my bullshit meter. First, I thought they were using optical switches (which might turn out to be as expensive as traditional spine switches due to lower production volumes), but after reading the article, I got the impression they split the switch uplinks into individual lanes (for example, there are four 100GE lanes in a 400GE uplink port), and prewired the lane-to-lane matrix in the ShuffleBox, which makes it as random as the [XKCD random number generator](https://xkcd.com/221/). It's worth noting that [Plexxi did exactly the same thing](https://blog.ipspace.net/2013/09/plexxi-psi-mau-at-gigabit-speed/) to get rid of CWDM costs, and that lane splitting is an ancient method we used more than a decade ago to ~~make our lives miserable~~ build larger leaf-and-spine fabrics ([some details](https://blog.ipspace.net/2023/03/leaf-spine-theory-reality/)).

{{<long-quote>}}
While there's nothing random in ShuffleBox, they can increase overall randomness with randomized switch-to-ShuffleBox and inter-ShuffleBox connections.
{{</long-quote>}}

They claim they used optimization methods to find the best partial mesh between N switches having D uplinks. The result is probably optimal (under some constraints) and might look random to a casual observer, but there's nothing random in it. The arXiv paper correctly calls it a Quasi-Random Graph; that nuance is lost, for obvious reasons[^HRP], in the blog posts and similar promotional material.

[^HRP]: A research paper published by a hyperscaler is often a thinly-veiled recruitment drive. See also [OpenFlow @ Google](https://blog.ipspace.net/2012/05/openflow-google-brilliant-but-not/) and [Google BeyondCorp](https://blog.ipspace.net/2018/03/before-commenting-on-someone-mentioning/).

**Could they get better throughput than leaf-and-spine fabrics?** In an apple-to-apple comparison, of course not. I [explained that ages ago](https://blog.ipspace.net/2012/04/full-mesh-is-worst-possible-fabric/), but of course nobody reads old stuff, so let's do another simple thought experiment:

* You build a leaf-and-spine fabric with N:1 oversubscription on leaf switches -- the total bandwidth of edge ports is N times higher than the total bandwidth of uplinks. N is usually set to three.
* The spine (or superspine fabric) of your fabric has no oversubscription. The only congested resources are the leaf switch uplinks.
* The traffic from any endpoint to any other endpoint in the leaf-and-spine fabric thus has to traverse exactly two leaf switch uplinks plus a non-oversubscribed fabric.
* The traffic in the Plexxi or AWS solution might have to traverse more than two leaf switch uplinks (when they use other leaves as relay nodes).

In an environment with many small flows (to make load balancing work well), it's thus IMPOSSIBLE to get better total throughput in a partial mesh than in a leaf-and-spine fabric with no core oversubscription, and it DOES NOT MATTER what the traffic profile is as long as the leaf switch uplinks are the congestion points. The details are left as an exercise for the curious reader.

**But they claim they got better throughput in the arXiv paper!** Yeah, I tried to figure that out, but failed. It looks like they used a simulation to generate the throughput graphs, but the source code is not available[^TS], so for someone not familiar with the topic, it's hard to know exactly what they did. Also, they compare their solution to *fat trees* without defining the parameters of the fat trees they're using; let's assume they mean "multi-layer non-oversubscribed leaf-and-spine fabric."

[^TS]: In the clarifications the authors sent me, they said, "The throughput simulations are implemented as linear programs (multi-commodity flow), a standard approach whose formulation is described in the paper."

I could think of several relatively simple explanations for their results:

* The spine layer (or the core fabric) in their fabric is oversubscribed.
* The load balancing in their leaf-and-spine fabric is suboptimal (some uplinks are congested while the others are idle). There are multiple ways to solve this challenge before moving to packet spraying; Cisco ACI supposedly uses one of them, and I wrote several blog posts on the topic in case you're interested in the details.
* They use load balancing *across virtual paths* in their solution, which results in a higher number of alternate paths and thus better load balancing performance.
* They use a routing algorithm that takes link load into account, resulting in more equally congested links.
* They use packet spraying (sending packets of the same session across multiple paths) in their solution, but not in the baseline leaf-and-spine fabric.

{{<long-quote>}}
I missed a crucial point in the paper: they need more uplinks on the leaf switches to achieve the same oversubscription ratio as a comparable leaf-and-spine fabric. From Section 2 of the paper: "_But an expander that is performance-equivalent to a fat tree may need more ToR uplinks (fabric-facing ports) because some uplink capacity is consumed by traffic relayed for other ToRs._"

That requires more leaf switches, but a big enough fabric still uses fewer active elements (switches), resulting in lower power consumption. On the _cost reduction_ side, they're calculating savings from fewer fabric switches but do not mention the total cost of the fabric, including ShuffleBoxes.

Other than that (and unequal-cost multipathing), they use the same multipath transport protocol ([SRD](https://blog.ipspace.net/2022/12/quick-look-aws-srd/)) in both cases, but not any extra tricks like packet spraying.
{{</long-quote>}}

I would love to believe there's some magic solution out there that works better than an optimally implemented leaf-and-spine fabric, but I don't think the laws of physics agree with that sentiment. However, according to [Clarke's First Law](https://en.wikipedia.org/wiki/Clarke%27s_three_laws), I could also be missing something obvious; in that case, please leave a comment.

**Does it matter?** It's an interesting approach, and most probably more than good enough for most use cases. After all, I always told people to connect four leaf switches into a full mesh instead of wasting time on a spine layer. I don't believe it gives you more throughput, but I totally agree it uses less power (ShuffleBoxes are probably passive elements).

Should we expect similar solutions in enterprise-sized data centers? Probably not. There might be a reason Plexxi got nowhere[^HPA]. Also, as long as Fortune 50 companies need [less than a dozen switches to build two data centers](https://blog.ipspace.net/2021/09/4-switch-fabric/) (based on a true story), optimizing the fabric design might not be the best investment of everyone's time.

On the other hand, if you build fabrics with tens of thousands of switches, you should definitely take a closer look. If you do, I'd love to hear your comments.

[^HPA]: If you believe in the unlimited magic of novel approaches, please feel free to blame the HP acquisition.