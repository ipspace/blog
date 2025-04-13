---
title: "Response: Peer-to-Peer Communication in IPv6 World"
date: 2025-04-15 07:23:00+0200
tags: [ IPv6, firewalls, NAT ]
---
Daryll Swer [posted a very informative response](https://blog.ipspace.net/2025/04/response-nat-traversal/#2598) to my [NAT Traversal Mess](https://blog.ipspace.net/2025/04/response-nat-traversal/) blog post, focusing on:

> Punching holes through that firewall is equivalent to establishing NAT translations.

It would be a shame to let that response wither as small print at the bottom of a blog post; here it is:
<!--more-->
---
I would not say outright 'equivalent'. There are more than one form of NAT, clearly, and not all forms of NAT (PAT) are as simple as firewall punching, the worse offender often called “symmetric NAT”. You yourself, stated: “Decent stateful firewalls match on the full 5-tuple, which is functionally equivalent to symmetric NAT, but don’t change the UDP port numbers when packets traverse them (making them equivalent to ‌port-restricted cone NAT), so it’s easier to discover what hole your peer punched in their firewall.”

Every host in native IPv6 LANs, would have a unique /128 as a minimum (could also have /64 ia_pd routed to the host, but that's not common (yet? RFC9663) in LAN/Wi-Fi networks), the punching is per-unique /128 address (or host), no NAT/PAT aka shared single IP address occurs here across N number of nodes, preventing any kind of port exhaustion related issues and/or “Symmetric NAT-like” issues (which is the majority of default NAT configuration out there, even on CGNAT products excluding the exceptions like IOS-XE, A10 CGNAT etc), it is behaviourally, equivalent with port-restricted cone NAT which I do not disagree, but I disagree that it's a problem for 99% of IPv6-users, STUN has no problems dealing with port-restricted cone NAT behaviour on legacy IPv4 and certainly no problems with native IPv6 (where port exhaustion/re-write will never happen anyway) behind a firewall. I'd know, because I spent a lot of hours over the years, testing popular end-user applications that supports IPv6 P2P (usually VoIP/Video calling software because how much more P2P can we get if not telephony software of sorts!) and PCAPs showed successful src/dst IPs matching each peer's local-endpoint, i.e. ruled out TURN, behind stateful firewalls, of course STUN worked fine. However, I cannot replicate this on most CGNAT deployments that I don't control because the majority of ISPs never enabled EIM+EIF NAT on the CGNAT device, and it breaks further for intra-CGNAT traffic because they refuse to enable hairpining.

STUN/TURN/ICE/WebRTC aren't a joke — the people who wrote the code behind these tools, spent decades tweaking it, fixing it, just to make it work with CGNAT deployments and similar, simply because people fear native routed IPv6 - yes, there's people doing /128 IPv6 and NATting /64 ULAs because NAT is a firewall technology for security compliance [according to some](https://www.f5.com/resources/white-papers/the-myth-of-network-address-translation-as-security) (yes, sarcasm). 

Let's not start talking about NAT Slipstreaming attacks and the likes now, people need their /128s and NAT66es!

I should note, EIM-NAT alone isn't sufficient, you need it with EIF-NAT hand-in-hand + hairpinning as discussed, for the 'ideal' P2P friendly NAT/CGNAT deployments. Fortigate has a nice explanation for most people, if the RFCs are a bit confusing ([part 1](https://docs.fortinet.com/document/fortigate/7.4.6/fortinet-carrier-grade-nat-field-reference-architecture-guide/920625/endpoint-independent-mapping), [part 2](https://docs.fortinet.com/document/fortigate/7.4.6/fortinet-carrier-grade-nat-field-reference-architecture-guide/921514/endpoint-independent-filtering)).  

I don't know whether EIF works on IOS-XE, probably does, but if you have a Windows PC, you can test for RFC conformance using [this tool](https://github.com/HMBSbige/NatTypeTester) (someone probably can port it to Linux/macOS).

Long story short — life's easier with native routed IPv6, no matter how you (as in, anyone who's pro-NAT) try to spin NAT being the saviour of IP networking. It may have been a different reality, had EIM+EIF+Hairpinning = default on all popularly used NATting software/OSes.

Yes, IPv6 multihoming is pain, BGP is great (routed IPv6 over BGP!), but can't BGP everywhere, and there's no good solution here, NAT66/NPTv6 or not, maybe some source routing on the LAN could handle this bit, but not sure how load balancing from local-endpoint would work on source address selection basis (i.e., you have two ISPs, each gave you a unique /48 and your VLAN has two /64s configured for SLAAC/RAs, now the endpoint has two /128s from two separate /64s-ISPs, how would the endpoint know when to do which prefix here for load balancing and that introduces a complexity of its own).

An ISP owner friend of mine, recently discussed on DHCPv6 server HA complexity across N BNGs, and we joked that, life's easier if every residential CPE supported BGP, we could just BGP everything and call it a day and not worry about next-hop failures or DHCPv6 state sync issues. But such is life, I'd still take IPv6 any day over NAT. Particularly in ISP networks, when you have P2P gamers on an Xbox or PS, intelligent CGNAT (EIF+EIM+Hairpinning) with dual-stack IPv6 ensures you don't get support tickets about P2P or port exhaustion issues because there's 1000 CPEs behind a /32.

---

I can definitely relate to the "_running BGP everywhere would make life simpler_" idea; using DHCPv6 for IPv6 prefix delegation is one of the worst examples of the "_everything looks like a nail now that I have this hammer_" mentality.

In unrelated news, the same people who are [religiously opposed to DHCPv6 address allocation](https://blog.ipspace.net/2021/10/ipv6-multiple-addresses-per-interface/) are now telling the world how great it is to [use DHCPv6 IA_PD to allocate a prefix to every host](https://www.rfc-editor.org/rfc/rfc9663.html). It's so lovely to see how consistent they are in their beliefs and how easily they think they can justify assigning a /64 (or more) to a host that ([in their words](https://www.rfc-editor.org/rfc/rfc9663.html#name-applicability-and-limitatio)) *needs three to five addresses per host*.
