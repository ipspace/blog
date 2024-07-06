---
title: "Opinion: Do You Care about MPLS in 2022?"
date: 2022-04-06 07:11:00
tags: [ MPLS ]
---
One of my readers asked for my opinion about this question...

{{<figure src="/2022/04/tweet-mpls.jpg">}}

... and I promised something longer than 280 characters.
<!--more-->
There seem to be two correct answers to this question: 

* I don't think that word means what you think it means
* It depends

Let's start with the first answer.

## What Does MPLS Mean?

For whatever reason some people understand _MPLS_ to mean _MPLS/VPN-based layer-3 connectivity services delivered by a service provider_[^MPLSWORD], in which case "_do you care about MPLS?_" should really be "_are you buying/using MPLS/VPN services?_". That's an easy question -- as I explained last week, [MPLS/VPN is unnecessarily complex](/2022/03/mpls-vpn-too-complex.html) (for a mix of good, bad, and ugly reasons), and so I'd prefer using anything else that meets the requirements[^CE].

[^MPLSWORD]: For a deep dive into "_that is not what MPLS means_", read the _[You’re Probably Using The Term MPLS Wrong](https://www.networkfuntimes.com/youre-probably-using-the-term-mpls-wrong/)_ by Chris Parker.

[^CE]: Keeping in mind that Carrier Ethernet is WAN bridging in disguise, so be careful how you use it.

As always, there are exception to every rule-of-thumb:

* MPLS/VPN could be the only reasonable service you can get.
* MPLS/VPN could be way more reliable than Internet access[^IA].
* IP routing (MPLS/VPN) is a better option for low-speed or high-latency links than bridging (Carrier Ethernet). I haven't seen Carrier Ethernet over Frame Relay or satellite links yet.
* You might need two providers for resiliency/business continuity reasons, and [combining a fast-and-cheap Internet uplink with a slower, more expensive, but a bit more reliable MPLS/VPN one](/2015/07/reliability-of-sd-wan-and-hybrid-wan.html) is not a bad idea. If you can afford it, use both as pure IP transport, and add routing over tunnels on top of that IP transport (see also: DMVPN or [SD-WAN](/2015/06/software-defined-wanwell-orchestrated.html)).
* Your purchasing team just signed a 10-year contract to get a 3% discount
* Add your own reason in the comments ;)

[^IA]: I'm not saying that applies to your residential Internet circuit, I'm just saying that the future is not evenly distributed, and there are still pockets of abhorrent connectivity.

## Who Uses MPLS?

On the "_do you care about MPLS as technology_" front: regardless of what the [SD-WAN pundits are telling you](/2015/07/some-ridiculous-sd-wan-claims.html) (because they belong to the "_MPLS doesn't mean what you think it means_" crowd), MPLS encapsulation is one of the most elegant encapsulations out there, and the idea to classify traffic at ingress and use labels to indicate the Forward Equivalence Class (FEC) and/or egress next hop is still perfectly valid.

We should also distinguish between the data plane mechanisms (encapsulation and label switching) and the control-plane protocols[^CPMPLS]. LDP is slowly going away in favor of SR-MPLS control plane mechanisms (IGP, BGP, PCEP...). L3VPN might be eventually replaced by EVPN (but not any time soon), but wherever the bandwidth is expensive enough (example: outside of the data centers), the underlying encapsulation is still predominantly MPLS.

[^CPMPLS]: Should we call control-plane protocols needed to support MPLS encapsulation "MPLS"? I don't think so, we should be more precise.

Now that we got the pedantry out of the way, let's see who (still?) uses MPLS technology in 2022. I don't think that landscape has changed significantly in the last decade.

Many large service providers use MPLS-based solutions internally to:

* [Build BGP-free core](/2021/05/segment-routing-mpls-bgp-free-core.html)
* Implement traffic engineering
* Have [fast reroute capabilities](https://my.ipspace.net/bin/list?id=Net101#FRR), either using MPLS FRR, remote LFA or Topology Independent LFA
* Build services on top of MPLS transport (even Carrier Ethernet is often implemented on top of MPLS)
* Increase the utilization of their peering links with Egress Peer Engineering.
* Add your favorite use case in the comments.

I know enterprises that had to build their own multi-tenant VPN infrastructure, and [used MPLS/VPN](/2011/03/mplsvpn-over-gre-over-ipsec-does-it.html) instead of the SD-WAN pixie dust. If you want to have a standard-based architecture, MPLS/VPN is still the best way to do it.

Finally, even some hyperscale web properties use MPLS encapsulation to steer traffic from their web proxies to the optimal egress link (similar to Egress Peer Engineering).

Whether you care about MPLS (the technology) in 2022 thus depends on the environment you're working in, but it's alive and doing quite well in many large-scale environments.

