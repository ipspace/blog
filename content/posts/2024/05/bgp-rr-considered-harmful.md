---
title: "BGP Route Reflectors Considered Harmful"
date: 2024-05-28 08:23:00+0200
tags: [ BGP, EVPN ]
evpn_tag: designs
---
The recent [IBGP Full Mesh Between EVPN Leaf Switches](/2024/05/evpn-designs-ibgp-full-mesh.html) blog post generated an [interesting discussion on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7199351613428236288/) focused on whether we need route reflectors (in small fabrics) and whether they do more harm than good. Here are some of the highlights of that discussion, together with a running commentary.

{{<note smallprint>}}Please note that we're talking about BGP route reflectors in reasonably small data center fabrics. Large service provider networks with millions of customer VPN routes are a completely different story. As always, what you read in a random blog post might not apply to your network design. YMMV.{{</note>}}
<!--more-->
Starting with [Pavel Lunin](https://www.linkedin.com/in/pavel-lunin-60868769/):

> The number of sessions that each leaf/edge would need to maintain in a full-mesh setup (N-1) is roughly the same as the number of sessions per RR (N). So, from the technical scalability point of view, it's not so much different from the RR-based design.

That's true. Also, most (vendor-validated) designs would run route reflectors on spine switches, and they usually have very similar CPUs to the leaf switches. From the scalability perspective, there's no difference.

> The whole problem of full-mesh scalability is configuring those sessions. But you can't run a fabric of more than 4-6 leaves without automatic inventory and leaf provisioning. Adding the sessions with all existing leaves is pretty trivial.

That is also true, although I would not be surprised to see environments running manually configured large fabric. Anyhow, if you automate the fabric deployment (and you should), route reflectors are unnecessary from the configuration consistency perspective.

One could argue, though, that route reflectors bring a bit more consistency. Once a leaf switch establishes a BGP session with a route reflector, all other leaf switches get the updates at approximately the same time. In a full mesh of BGP sessions, the initial updates could be staggered over an extended period of time. Does that matter? I have no idea.

Some might argue that you should run BGP route reflectors on dedicated off-path devices, and some might think that running them in virtual machines is a good idea. [It's not](/2021/10/circular-dependencies-considered-harmful.html), more so if they serve as the route reflectors for the fabric they are connected to. Apart from my *circular dependencies* considerations, Pavel Lunin [listed several other challenges](https://www.linkedin.com/feed/update/urn:li:activity:7199351613428236288?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7199351613428236288%2C7199496750540161025%29&replyUrn=urn%3Ali%3Acomment%3A%28activity%3A7199351613428236288%2C7199501227905232897%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287199496750540161025%2Curn%3Ali%3Aactivity%3A7199351613428236288%29&dashReplyUrn=urn%3Ali%3Afsd_comment%3A%287199501227905232897%2Curn%3Ali%3Aactivity%3A7199351613428236288%29):

* You need servers and ports to plug them.
* Unless you're running a VM copy of a networking device, you'll have to find a decent route reflector software with EVPN support.
* To run a route reflector in a virtual machine, you'll need a (well-maintained) virtualization environment.
* The RR in a VM won't see the physical interface state unless you use PCI pass-through.
* If you want to double-attach route reflectors, you should ensure they are never used as transit nodes by IGP.

As always, [Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/) added some phenomenal insights, some of them also applicable to large-scale service provider environments (slightly edited):

{{<long-quote>}}
A fully centralized RR is a dangerous single point of failure. Even with triple RR redundancy, I have seen severe meltdowns caused by software bugs and misconfigurations. 

If you have partial mesh with decentralized RR following the physical topology, then in many cases, your RR failure has only a local impact, but the rest of the network is still available. 

Somehow, the idea that RR is such a special feature that you need a special server for it has stuck in people's minds. However, in most enterprise networks, the size and complexity are not so great that any decent router could fulfill the RR role in an aligned topology.

Telco networks are a different animal, though. But even there, some decentralization of the RR function would be recommended. Hierarchical layered networks have been used in telephony or electricity networks for ages, and this would be a good approach for MPLS/SR cores, too, in very large networks. Then, RRs would reside in all network layers and each segment. This would contain the impact of an RR failure.

If you have a proper automation framework, decentralized RRs are manageable even in a large telco network. 
{{</long-quote>}}

Finally, [Kristijan Taskovski](https://www.linkedin.com/in/kristijan-taskovski/) pointed out that [route reflectors lose ECMP state](https://www.linkedin.com/feed/update/urn:li:activity:7199351613428236288?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7199351613428236288%2C7199496750540161025%29&replyUrn=urn%3Ali%3Acomment%3A%28activity%3A7199351613428236288%2C7199911414684110849%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287199496750540161025%2Curn%3Ali%3Aactivity%3A7199351613428236288%29&dashReplyUrn=urn%3Ali%3Afsd_comment%3A%287199911414684110849%2Curn%3Ali%3Aactivity%3A7199351613428236288%29) (unless you configure BGP Additional Paths). While that's true in IP routing, it's less applicable to EVPN environments using the Auto Route Distinguisher feature because each EVPN route (for the same MAC/IP address) contains uses a different RD and is thus a different prefix from the BGP perspective.

**Long story short:**

* From the scalability perspective, you don't need route reflectors in small EVPN data centers.
* You might still want to use them for consistency or to simplify troubleshooting. You don't want to check a full mesh of BGP sessions whenever a user reports a connectivity problem.
* You REALLY SHOULD automate the fabric configuration and SHOULD NOT use a BGP full mesh in manually configured fabrics having more than a few leaves.

Anything else? Please leave a comment.