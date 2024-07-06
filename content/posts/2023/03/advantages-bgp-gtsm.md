---
title: "Advantages of Using Generalized TTL Security Mechanism (GTSM) with EBGP"
date: 2023-03-16 07:56:00
tags: [ BGP, security ]
---
A few weeks ago I [described why EBGP TCP packets have TTL set to one](/2023/03/ebgp-ttl-history.html) (unless you configured EBGP multihop). Although some people claim that ([like NAT](/2011/12/is-nat-security-feature.html)) it could be a security feature, it's not a good one. Generalized TTL Security Mechanism (GTSM, described in [RFC 5082](https://datatracker.ietf.org/doc/html/rfc5082)) is much better.

Most BGP implementations **set TTL field in outgoing EBGP packets to one**. That prevents a remote intruder that manages to hijack a host route to an adjacent EBGP peer from forming a BGP session as the TCP replies get lost the moment they hit the first router in the path.
<!--more-->
Unfortunately, there's nothing one can do (apart from strict ACLs, but we know that's not going to happen) to stop a remote intruder from sending a flood of TCP SYN packets to a BGP router. Those packets would waste router's CPU cycles and potentially saturate its TCP session table[^SC]. You could try to implement control-plane policing that would check TTL on incoming BGP packets, but it's always possible to fine-tune the TTL on the sending host to get the desired value at the attack target.

Even better[^ISP], the TCP SYN+ACK packets sent as a response to the incoming spoofed TCP SYN packets would waste CPU cycles on the adjacent router that has to respond with an RST packet to any incoming packet that is not part of a known TCP session.

As the router CPUs tend to be way slower than laptop CPUs, it's trivial to hose two routers with a TCP SYN flood, and the only reason we don't see that in the wild is the abundance of lower-hanging fruit.

Please note that MD5 or TCP-AO session protection won't help you -- the router still has to process incoming TCP SYN packets and figure out they're invalid. It might drop them instead of sending a TCP SYN+ACK packet though.

[^SC]: Assuming the TCP implementation in that router does not use [SYN cookies](https://en.wikipedia.org/wiki/SYN_cookies).

[^ISP]: From the intruder standpoint

Generalized TTL Security Mechanism (GTSM) **sets TTL field to 255** and expects **incoming EBGP packets to have TTL set to 255**[^254]. It's pretty hard to get that done if you're not adjacent to the router you want to attack, and it's easy to filter packets to TCP port 179 that have TTL less than 254 with a hardware ACL (including control-plane protection). Mission accomplished, the remote intruder cannot attack the router's control plane anymore[^ET].

You can also use GTMS to protect IBGP sessions by checking that the TTL value exceeds 255-N with N being the expected number of hops across your network. While it's better than nothing, this is a weaker check than the EBGP one. A close-enough intruder could still wreak havoc -- another reason to have strict ACLs on the network edge interfaces.

Unfortunately, most routers remain vulnerable to denial-of-service attacks from a directly connected intruder -- the incoming TCP SYN packet with TTL set to 255 could come through another interface or through a tunnel[^MTTL]. The only way to stop that attack vector is to deploy unicast reverse path forwarding (uRPF) checks or strict edge-facing ACLs.

[^254]: Or 254, depending on the implementation.

[^ET]: At least not the BGP daemon. Unless you configure strict ACLs on every network edge interface, you're leaving doors wide open for denial-of-service attacks on most control-plane daemons.

[^MTTL]: Bonus points if you don't propagate MPLS TTL back into IP TTL, or if you're [using VXLAN on unprotected VTEPs](/2015/04/omg-vxlan-encapsulation-has-no-security.html).