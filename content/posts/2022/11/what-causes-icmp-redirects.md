---
title: "What Causes ICMP Redirects?"
date: 2022-11-30 07:25:00
tags: [ IP routing ]
---
A while ago, I wrote a blog post [explaining why we should (mostly) disable ICMP redirects](https://blog.ipspace.net/2022/02/nexus-icmp-redirects.html), triggering a series of comments discussing the root cause of ICMP redirects. A few of those blamed static routes, including:

> Put another way, the presence or absence of ICMP Redirects is a red herring, usually pointing to architectural/design issues instead. In this example, using vPC Peer Gateway or, better yet, running a minimal IGP instead of relying on static routes eliminates ICMP Redirects from both the problem and solution spaces simultaneously.

Unfortunately, that's not the case. You can get ICMP redirects in well-designed networks running more than one routing protocol.
<!--more-->
Before going into the details, please remember that a router generates an ICMP redirect every time it has to forward a packet back through the ingress interface -- a clear indication that the packet sender has suboptimal routing information that the ICMP redirect is trying to augment.

Now let's get back to the simple data center network that triggered the discussion, and imagine that:

* E1 and E2 are routers connected to the global Internet. For whatever reason they have the full BGP table.
* C1 and C2 are core switches. They are not expensive enough to be able to install the entire BGP table into the forwarding ASIC.

{{<figure src="/2022/02/icmp-redirect-layer-3.png" caption="Layer-3 connectivity">}}

You could use a [variety of mechanisms](https://blog.ipspace.net/2022/05/living-small-forwarding-tables.html) to make C1 and C2 work with suboptimal information. In most cases, you'd run an IGP between the four devices, keep the complex stuff limited to E1/E2, and advertise the default route from E1 and E2 toward C1/C2.

The traffic sent through C1/C2 toward the Internet will sometimes land on the wrong edge router -- the core switches simply don't have enough information to select the optimal forwarding path. The edge router receiving such traffic has to forward it to the other edge router. There are several ways you could meet that requirement:

* Use the shared VLAN between E1, E2, C1, and C2 to forward the misdirected traffic;
* Add another VLAN connecting E1 and E2.

If you use the shared VLAN to forward the misdirected traffic between E1 and E2, the egress interface on the first-hop edge router matches the ingress interface, and that router will generate ICMP redirects (unless you turned them off).

**Takeaways:**
* ICMP redirects have nothing to do with static routes
* While it's possible to design networks that avoid ICMP redirects, they could happen in well-thought-out designs.
* Disable ICMP redirects on all segments that don't have directly-connected hosts, and everywhere you use a first-hop redundancy protocol or anycast gateway[^ER].

[^ER]: The proof of the last claim is left as an exercise for the reader.
