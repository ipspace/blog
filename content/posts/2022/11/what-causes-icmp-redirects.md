---
title: "ICMP Redirects and Suboptimal Routing"
date: 2022-11-30 07:25:00
lastmod: 2022-12-01 16:30:00
tags: [ IP routing ]
---
A while ago, I wrote a blog post [explaining why we should (mostly) disable ICMP redirects](/2022/02/nexus-icmp-redirects.html), triggering a series of comments discussing the root cause of ICMP redirects. A few of those blamed static routes, including:

> Put another way, the presence or absence of ICMP Redirects is a red herring, usually pointing to architectural/design issues instead. In this example, using vPC Peer Gateway or, better yet, running a minimal IGP instead of relying on static routes eliminates ICMP Redirects from both the problem and solution spaces simultaneously.

Unfortunately, that's not the case. You can get suboptimal routing that sometimes triggers ICMP redirects in well-designed networks running more than one routing protocol.
<!--more-->
### Suboptimal Routing and ICMP Redirects

{{<note update>}}I badly mismanaged the details in the original version of this section. Fortunately, I have attentive readers like Henk who are [quick to set me straight](/2022/11/what-causes-icmp-redirects.html). Thank you!{{</note>}} 

Let's define *suboptimal routing* first. In the context of this blog post, *suboptimal routing* happens when a router has to send a packet back to the ingress interface because the upstream router (or host) sent it to a suboptimal next hop.

Suboptimal routing was a big deal in the days of early Ethernet networks and CPU-based packet forwarding, and the designers of IPv4 tried to solve the simpler case (host using a default route pointing to a suboptimal first-hop router) with ICMP redirects. The rules for generating ICMP redirects are set out in [RFC 792](https://www.rfc-editor.org/rfc/rfc792); here's a slightly rephrased version:

> If the next hop router and the host identified by the internet source address of the datagram are on the same network, a redirect message is sent to the host.

In most sane cases, that means that the routers send ICMP redirects to directly-connected hosts. As we'll be talking about suboptimal routing between core and edge routers, we shouldn't worry about ICMP redirects, but (somewhat surprisingly) not disabling them might kill the performance of your network. Here's what's going on behind the scenes.

It was easy to check for ICMP redirects in the days of software-based packet forwarding -- the packet forwarding software could compare ingress and egress interfaces after performing the FIB lookup, do an additional check on the source IP address, and punt the packet to the _IP process_ to generate the ICMP redirect if needed[^NFP].

[^NFP]: The code generating an ICMP redirect has to allocate memory for the additional packet, and that was usually a Mission Impossible in the (interrupt-driven) fast forwarding path.

Now imagine trying to emulate the above algorithm with an ASIC. Complex-enough ASICs would be able to perform all the necessary checks in hardware and send the packet to the CPU only when absolutely needed. Less capable ASICs (or hasty implementations) would send all packets that would have to exit through the ingress interface to the CPU whenever ICMP redirects are enabled on the interface (just in case an ICMP redirect has to be sent). 

{{<note>}}Now would be a perfect time to leave a comment telling me to stop worrying because all modern ASICs deal with the above now-hypothetical scenario, and all vendors implemented it correctly for ages, but you simply cannot tell me the details due to the NDAs you had to sign.{{</note>}}

Old-timers might remember the **ip route-cache same-interface** command that disabled that behavior on Cisco IOS; the more things change the more they stay the same.

### Back to Suboptimal Routing

Now let's get back to the simple data center network that triggered the discussion, and imagine that:

* E1 and E2 are routers connected to the global Internet. For whatever reason they have the full BGP table.
* C1 and C2 are core layer-3 switches. They are not expensive enough to be able to install the entire BGP table into the forwarding ASIC.
* E1, E2, C1, and C2 are connected to a shared transit VLAN.

{{<figure src="/2022/02/icmp-redirect-layer-3.png" caption="Abstract layer-3 connectivity">}}

You could use a [variety of mechanisms](/2022/05/living-small-forwarding-tables.html) to make C1 and C2 work with suboptimal information. In most cases, you'd run an IGP between the four devices, keep the complex stuff limited to E1/E2, and advertise the default route from E1 and E2 toward C1/C2.

The traffic sent through C1/C2 toward the Internet will sometimes land on the wrong edge router -- the core switches simply don't have enough information to select the optimal forwarding path. The edge router receiving such traffic has to forward it to the other edge router. There are several ways you could meet that requirement:

* Use the shared VLAN between E1, E2, C1, and C2 to forward the misdirected traffic;
* Add another VLAN connecting E1 and E2.

If you use the shared VLAN to forward the misdirected traffic between E1 and E2, the egress interface on the first-hop edge router matches the ingress interface, and based on how the packet forwarding is implemented in that router, the packet might have to be switched by the CPU (or dropped to the slow forwarding path).

**Takeaways:**
* ICMP redirects have nothing to do with static routes.
* Suboptimal routing might not trigger ICMP redirects, but could result in degraded performance if ICMP redirects are not disabled.
* While it's possible to design networks that suboptimal routing, it could happen in well-thought-out designs.
* Disable ICMP redirects on all segments that don't have directly-connected hosts, and everywhere you use a first-hop redundancy protocol or anycast gateway[^ER].

[^ER]: The proof of the last claim is left as an exercise for the reader.

Finally, would it be possible to generate ICMP redirects on E1 and E2 even though there are no hosts connected to that segment? Of course, but I'll leave the details as an exercise for the interested reader.