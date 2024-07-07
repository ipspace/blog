---
anycast_tag: intro
date: 2021-11-24 07:15:00+00:00
series:
- anycast
series_weight: 900
tags:
- IP routing
title: Anycast Fundamentals
---
I got into an interesting debate after I published the _[Anycast Works Just Fine with MPLS/LDP](/2021/11/anycast-mpls/)_ blog post, and after a while it turned out we have a slightly different understanding what *anycast* means. Time to fall back to a [Wikipedia definition](https://en.wikipedia.org/wiki/Anycast):

> Anycast is a network addressing and routing methodology in which a single destination IP address is shared by devices (generally servers) in multiple locations. Routers direct packets addressed to this destination to the location nearest the sender, using their normal decision-making algorithms, typically the lowest number of BGP network hops.

Based on that definition, any transport technology that allows the same IP address or prefix to be announced from several locations supports anycast. To make it a bit more challenging, I would add "_and if there are multiple paths to the anycast destination that could be used for multipath forwarding[^UCMP], they should all be used_".
<!--more-->
It's also worth noting that outside of a single link-state area[^LEV], and in particular while looking at the routing or forwarding table, it's often impossible to differentiate between an anycast prefix (prefix being advertised from multiple locations), redundantly connected site or autonomous system, or a topology that provides multiple equal-cost paths to the same destination. As is usually the case, the proof is left as an exercise for the reader.

[^UCMP]: ... getting ECMP versus UCMP discussion out of the way

[^LEV]: ... or level depending on your terminology

With the terminology being out of the way, it's time to turn to an excellent comment left by Minh Ha on the original blog post (the footnotes are mine).

---

While those who study transport mechanics in internetwork quickly realize the *[anycast doesn't work with traditional MPLS]* claim is incorrect based on first principles, it's always nice to see a conclusive proof laid out with step-by-step instructions and empirical data.

MPLS is Transport, and Transport is more concerned about addressing, routing, synchronization etc, while anycast, taken to its root, is a naming issue, so one can quickly realize there's no fundamental reason that prevents MPLS from supporting anycast. Any limitation is strictly implementational, not technological. So it's not too surprising how even old LDP code can take on anycast.

"*MPLS is not a pure packet switching technology, but has a control plane based on virtual circuit switching.*"[^Q1] ... while I can see why Dmytro might have come to this conclusion, it's not really true either. It's true that MPLS is an evolution of ATM, and therefore, is not tunnel, but VC -- never understand the pointless debates about whether MPLS is tunnel or VC as the people who claim it's tunnel obviously don't understand its history -- but MPLS is more like loose VC. MPLS relies on a functional routing protocol to discover the paths, and LDP -- if it can be called MPLS control plane as MPLS control plane can consist of way more than LDP -- assigns the labels for the prefixes, so MPLS in an IP network is essentially packet-switching, not VC. If a core switch breaks down in a VC network, the VC traversing it breaks[^ED], but in MPLS IP network, the LSP adjusts itself based on the underlying routing topology. LDP itself is a simplistic label assignment protocol, AFAIK it doesn't perform any function central to a VC control plane, so all in all MPLS deviates a fair bit from traditional VC network.

[^Q1]: Minh Ha is quoting the blog post that triggered my initial response.

[^ED]: Slightly edited to make it easier to understand to audience not familiar with telco terminology.

But the most important part is: MPLS is more general than both VC and packet-switch, because it's Transport, and this point is crucial. MPLS can therefore be generalized to support non-packet-switch network, in VC style or what not[^EOM]. So all of these points make it obvious that nothing would stop MPLS from supporting anycast routing, or any form of routing, for that matter. And the reason this needs to be clearly identified is so vendors can't use that as an excuse to sell SR for the wrong reason.

[^EOM]: Want an absurd example? Look no further than [RFC 3251](https://datatracker.ietf.org/doc/html/rfc3251).

And I never understand what the excitement is with SR, given that it's a product of SDN, itself a misconception(or a flight of fantasy) from the start[^SR]. SR is more like a point solution for a few special cases, and it tries to overcome the state problems by introducing more constructs into the network, like SRGB and global segments, that can lead to tight binding and confusion, esp. at large scale.

[^SR]: As I explained in [other blog posts](/tag/segment-routing/) (and videos), [SR-MPLS does make sense](/2019/04/why-is-mpls-segment-routing-better-than/) if you want to run MPLS transport as it simplifies the MPLS control plane (no IGP-LDP dependencies). [SRv6 is obviously a different story](/2019/01/srv6-one-tool-to-rule-them-all/).

In fact Dmytro's post already mentioned 3 deficiencies of SRGB mismatch. Introducing more moving parts, esp. global ones, into big distributed systems, always leads to complexity and unintended consequences. SR will run into problem with MPLS network where label is no longer just an abstract concept with no physical reality, but has to match the underlying resources. This 'fitting the data' requirement and SRGB can contradict each other, leading to much headache. And if one has to add a controller to SR to do TE, then one will run into all the scaling problems of centralized routing that SDN proponents have learnt the hard way.