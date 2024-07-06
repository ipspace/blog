---
date: 2022-11-17 06:51:00+00:00
multihoming_tag: session
series:
- multihoming
tags:
- networking fundamentals
- LISP
title: Multihoming Cannot Be Solved within a Network
---
Henk made an [interesting comment](/2022/11/worth-reading-routing-never-solved-problem.html#1487) that finally triggered me to organize my thoughts about network-level host multihoming[^SM]:

[^SM]: Site multihoming is an even more gruesome beast that we'll carefully avoid in this blog post.

> The problems I see with routing are: [hard stuff], **host multihoming**, [even more hard stuff]. To solve some of those, we should have true identifier/locator separation. Not an after-thought like LISP, but something built into the layer-3 addressing architecture.

Proponents of various clean-slate (RINA) and pimp-my-Internet (LISP) approaches are quick to point out how their solution solves multihoming. I might be missing something, but it seems like that problem cannot be solved within the network.
<!--more-->
**TL&DR**: You cannot solve host multihoming within the network layer while having summarizable network addresses. You have to solve it somewhere at the upper edge of the transport layer[^WC].

[^WC]: I might have missed something significant, in which case please free to point it out in a comment.

Imagine a mobile phone with a WiFi and 5G connection provided by two different ISPs. Those ISPs have some upstream ISPs until a pair of them meets at some exchange point.

{{<ascii>}}
 Host
┌────┐   ┌───────────┐    ┌───────────┐    ┌─────┐
│    │   │           │    │           │    │     │
│   A├───┤   ISP-A   ├────┤   ISP-C   ├────┤     │
│    │   │           │    │           │    │     │    ┌────────┐
│    │   └───────────┘    └───────────┘    │     │    │        │
│ H  │                                     │ IXP ├────┤ Server │
│    │   ┌───────────┐    ┌───────────┐    │     │    │        │
│    │   │           │    │           │    │     │    └────────┘
│   B├───┤   ISP-B   ├────┤   ISP-D   ├────┤     │
│    │   │           │    │           │    │     │
└────┘   └───────────┘    └───────────┘    └─────┘
{{</ascii>}}

The host (mobile phone) could use node- or interface addresses. Let's start with the assumption that [IPv6 was the worst decision ever](/2022/09/ipv6-worst-decision-ever.html), and that node-level addresses of something like CLNP [would save the world](/2020/09/worth-reading-clns-failure.html) and bring multihoming to the masses.

Under that scenario, host would be known only by its node address (H). Everyone between the bifurcation point (IXP) and the host needs to know that there are two paths toward the host, and what their state is. That includes ISP-A, ISP-B, and all upstream ISPs including upstream ISPs directly connected to IXP[^PER]. Clearly not the brightest idea for ISPs with millions of customers.

{{<note info>}}Please note that no amount of lipstick will make this piglet any prettier. Either you'll end with a widespread state explosion, or you'll reinvent IP multihoming and have a home agent within one of the ISPs -- making the end-customer happiness dependent on that ISP not having a bad-hair day.{{</note>}}

[^PER]: The proof is left as an exercise for the reader.

OK, maybe IPv6 isn't as bad as some people would like us to believe. Back to the drawing board. What if we would have two addresses on the multihomed host (one belonging to each ISP), and then (according to RINA) build an overlay network with global host addresses on top of that? Congratulations, you just proved [RFC 1925](https://www.rfc-editor.org/rfc/rfc1925) rule 6a and reinvented LISP.

There are two ways to implement the overlay network idea: either you keep the host TCP stacks unchanged and build the overlay solution within the network (LISP) or you modify the host networking stack.

Let's stick with the network-based solution for a moment. Regardless of how you plan to implement it, you'll need a proxy between the "native" protocol stack on the inside (private network) and the "layered" protocol stack on the outside (global Internet). That proxy will have to keep mappings between all underlay and overlay address of all external devices accessing the internal servers. Now ask yourself how big a proxy Facebook would need. Why do you think they never deployed LISP in production?

On top of that, you'll have to deal with two small details: path liveliness checks (is the remote underlay address reachable?) and cache invalidation (is the remote host mapping still valid?). The latter is supposedly one of the [hard problems in computer science](https://martinfowler.com/bliki/TwoHardThings.html). For more details, read the _[Architectural Implications of Locator/ID Separation](https://datatracker.ietf.org/doc/html/draft-meyer-loc-id-implications-01)_ IETF draft[^NORFC].

[^NORFC]: Reading it, you'll probably realize why (like the _[Operators and the IETF](/2021/10/worth-reading-ietf-operators.html)_ draft) it was never published as an RFC ;)

Back to the drawing board (take two). What if we'd implement multihoming within the hosts? Congratulations, finally you realized that _[complexity belongs to the network edge](/2011/05/complexity-belongs-to-network-edge.html)_ (see also: [RFC 3439](https://www.rfc-editor.org/rfc/rfc3439)). Not surprisingly, there are widely-deployed solutions using this approach, for example [MP-TCP](/2019/03/multipath-tcp-on-software-gone-wild.html)[^SIRI].

As much as I like MP-TCP, the limitations of its environment force it to remain a half-baked solution. It has to emulate the TCP socket API and thus has to establish the first TCP session with a well-known server IP address, so the server cannot be multihomed to multiple providers. The only way to fix that is to [change the socket API](/2009/08/what-went-wrong-socket-api.html) (fat chance) and hopefully [add session layer to TCP/IP protocol stack ](/2009/08/what-went-wrong-tcpip-lacks-session.html)while doing that.

[^SIRI]: Not sure whether MP-TCP is widely deployed? When was the last time you've seen [someone using Siri](https://support.apple.com/en-us/HT201373)?

### Revision History

2022-11-18
: Added TL&DR summary
