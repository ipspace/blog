---
date: 2015-06-23 08:04:00+02:00
tags:
- SD-WAN
- SDN
- WAN
title: Software-Defined WAN:Well-Orchestrated Duct Tape?
url: /2015/06/software-defined-wanwell-orchestrated/
sd-wan_tag: myth
---
One of the Software Defined Evangelists has declared 2015 as the Year of SD-WAN, and my podcast feeds are full of startups explaining how wonderful their product is compared to the mess made by legacy routers, so one has to wonder: is SD-WAN really something fundamentally new, or is it just another old idea in new clothes?
<!--more-->
### Read This First

Don't misinterpret this blog post. I am not against SD-WAN; in fact, I love some of the ideas I've seen so far and the clean and unified architecture of some of the products.

I am, however, disgusted by all the hype cloaked as technical discussions and think the networking *engineers* (as opposed to marketers or managers) should approach SD-WAN like [any other technology](/2015/03/response-why-technology-still-matters/) and try to understand how it really works and what the real challenges and solutions are.

### What Is SD-WAN?

With no definition from a respectable body, let's fall back to the [description on Open Networking User Group web site](http://opennetworkingusergroup.com/onug-spring-2014-use-cases/software-defined-wide-area-network-sd-wan/). Looking at their diagrams, it looks like SD-WAN is the thing that allows you to use the public Internet in parallel with private WAN to reduce the costs.

Wait, what? We've been doing that for ages, and most our customers weaned themselves off MPLS/VPN years ago, using solutions like IPsec, DMVPN, or even [MPLS/VPN-over-GRE-over-IPsec](/2011/03/mplsvpn-over-gre-over-ipsec-does-it/).

The marketing gurus working for SD-WAN vendors will quickly tell you that what they do is fundamentally different: the thing we've been doing in the past is *hybrid WAN* and the new thing is *software defined*, uses central controller, and therefore doesn't have to use a complex plethora of protocols like IKE, IPsec, GRE, NHRP, NBAR, IP SLA, PBR or routing protocols like BGP or OSPF. All that is replaced by some secret sauce proprietary to each startup (yeah, that's a comforting thought right there).

### SD-WAN Behind the Scenes

In its simplest incarnation, SD-WAN (as promoted by a large crowd of startups) allows you to use two WAN transport networks for optimal end-to-end transport.

{{<figure src="/2015/06/s500-File+12-06-15+17+13+17.png" caption="Typical SD-WAN architecture">}}

Let's see what needs to be done to make this work.

As you cannot advertise the non-public address ranges used on your sites to the transport networks (at least not to the public Internet), every SD-WAN solution builds an overlay network. Whether they use **GRE, VXLAN, IPsec tunnel mode** or any other encapsulation technology is irrelevant.

Some customers want direct connectivity between every pair of sites, requiring a full mesh of tunnels or a multi-access tunnel technology like **DMVPN**. The details don't really matter, and in most cases the tunnels get provisioned automatically (not dissimilar to what Open vSwitch or VXLAN implementations do).

You wouldn't want to transport your internal traffic across Internet unencrypted, would you? Every SD-WAN solution has to solve the traffic encryption problem (hint: there's a standard way of doing it, called **IPsec**) and key distribution problem (aka **IKE** in multi-vendor world).

Before you can start using the SD-WAN overlay network, the SD-WAN network needs to learn the topology of your network. Let's ignore for the moment the challenges of integrating SD-WAN edge devices with the traditional on-site L2/L3 devices and focus on what's going on within the SD-WAN cloud.

When an SD-WAN edge node powers up, it has to connect to the controller and register its outside (WAN) IP addresses with the controller. We used **NHRP** to do that in standard-based networks.

Next, the controller needs to learn the local prefixes available on every site. Whether you use a **routing protocol**, REST API or a proprietary vendor-specific protocol to exchange those prefixes doesn't really matter... unless you happen to care about multi-vendor interoperability, which you won't see in the SD-WAN world for a long time.

{{<note>}}It's so entertaining listening to people who once touted the benefits of multi-vendor networks suddenly promoting the benefits of undocumented proprietary solutions "because they are so much better than routing protocols."{{</note>}}

After discovering the prefixes available on each SD-WAN site, the controller decides which prefixes to use, and sends the best prefixes together with transport network next hops to SD-WAN edge nodes. If this doesn't sound like description of **BGP route reflector**, I don't know what does (apart from the minor detail that almost all SD-WAN vendors use proprietary mechanisms -- but I guess you already got that point).

In the ideal case, every site reaches every other site over more than one uplink, so it has to select the best uplink to use, either based on reachability or more complex measurements -- the job of legacy tools like **BFD** or **IP SLA**.

Finally, once the quality of the links is known, the user traffic has to be sorted into application classes (aka **NBAR**) and forwarded to the same destination SD-WAN node across one of the uplinks based on pre-programmed policy (does **Policy Based Routing** sound familiar)?

Some SD-WAN solutions go way beyond simple PBR and use smart congestion measurement, packet retransmission, or even forward error correction to make the best use of available bandwidth while retaining acceptable end-to-end quality. These technologies are nothing new; we've seen them in **WAN optimization devices** for years (and you might remember people who loved to rant how broken WAN optimization is).

### Summary

Every SD-WAN solution has to reinvent all the wheels we use in *hybrid WAN* networks -- tunneling, encryption, key exchange, registration of edge nodes, exchange of reachability information, next-hop reachability and end-to-end link quality measurements, application recognition and packet forwarding based on policies, so please don't tell me how revolutionary these solutions are (RFC 1925 sections 2.11 and 2.5 quickly come to mind).

There is, however, a fundamental difference between a hodgepodge of traditional protocols that were force-fit into a hybrid WAN architecture and SD-WAN -- the architects of SD-WAN products were not burdened with legacy implementations, or forced to reuse code base that was meant to solve a totally different problem or protocols that were suboptimal for the job (why is anyone using OSPF in DMVPN networks when it's clear that BGP scales much better?). The individual features that they use to reinvent the wheels are also tightly integrated, because they were designed from day one to be used together.

The architecture of most SD-WAN products is thus much cleaner and easier to configure than traditional hybrid networks. However, do keep in mind that most of them use proprietary protocols, resulting in a [perfect lock-in](/2015/01/lock-in-is-inevitable-get-used-to-it/).

### More Details

* [Software-Defined WAN (SD-WAN) Overview](https://www.ipspace.net/SD-WAN_Overview) webinar ([free](https://www.ipspace.net/Subscription/Free)) describes the basics of SD-WAN and typical SD-WAN components and architectures.
* [Cisco SD-WAN Foundations and Design Aspects](https://www.ipspace.net/Cisco_SD-WAN_Foundations_and_Design_Aspects) webinar ([free](https://www.ipspace.net/Subscription/Free)) describes Cisco's SD-WAN solution (formerly known as Viptela)
* You'll find my [grumpy take on SD-WAN](https://my.ipspace.net/bin/list?id=SDNUseCases#WAN) in the [SDN Use Cases](http://www.ipspace.net/SDNUseCases) webinar ([subscriber-only](https://www.ipspace.net/Subscription)).

### About the Title

Read [this tweet](https://twitter.com/ioshints/status/10449562829328384) in case you haven't figured out the joke in the blog post title. Here's its gist in case Twitter disappears:

> Everything can be solved with a right combination of NAT, GRE and PBR ;) Duct tapes of networking.
