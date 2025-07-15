---
title: "ArubaCX: When BGP Soft Reconfiguration Becomes a No-Op"
date: 2025-07-25 07:58:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
Changing an existing BGP routing policy is always tricky on platforms that apply line-by-line changes to device configurations (Cisco IOS and most other platforms claiming to have *industry-standard CLI*, with the notable exception of Arista EOS). The safest approach seems to be:

* Do not panic when the user makes changes to route maps and underlying filters (prefix lists, AS-path access lists, or community lists).
* Let the user decide when they're done and process the BGP table with the new routing policy at that time.
<!--more-->
That second part traditionally involved *resetting a BGP session*, which is clearly a bad idea when the BGP table has a million entries. Cisco IOS solved that conundrum in the outbound direction ages ago with **soft reconfiguration** -- the router replays its BGP table and sends updated BGP paths or revokes them based on the current routing policy.

The inbound direction was more of a challenge until the vendors implemented [RFC 2918](https://datatracker.ietf.org/doc/html/rfc2918) (enhanced by [RFC 7131](https://datatracker.ietf.org/doc/html/rfc7313)), which allowed a router to ask its neighbor to resend its BGP table, which is then processed with the new inbound routing policy.

Most platforms I worked with when developing _netlab_ have both capabilities, but sometimes they tend to be implemented a bit creatively, as we discovered when debugging a lack of outbound changes on ArubaCX (more about that in another blog post).

ArubaCX **clear bgp** command has many options:

* You can reset BGP sessions with one or more peers (**clear bgp _ip_**, **clear bgp _peergroup_**, or **clear bgp \***)
* You can also clear one or all address families. This triggers *soft reconfiguration*, and you can specify the affected peers and the direction (for example, **clear bgp ipv4 unicast \* soft out**).

The inbound soft reconfiguration works as expected:

* ArubaCX sends a *route refresh* message with requested AFI/SAFI and subtype *normal route refresh request*
* The BGP peer responds with a *beginning of route refresh* message, followed by one or more update messages, and completes with an *end of route refresh* message.

{{<figure src="/2025/07/aruba-bgp-route-refresh.jpg" caption="Wireshark capture of BGP messages between ArubaCX and FRRouting">}}

However, the *outbound soft reconfiguration*, for example **clear bgp ipv4 unicast \* soft out** does *absolutely nothing*. You won't see an outgoing BGP update in the packet capture, regardless of how many times you execute that command. To add insult to injury, the box doesn't even tell you *I'm not doing that FR FR* 🤪 It keeps mum and pretends nothing happened. What else could one wish for when desperately trying to troubleshoot a BGP problem at 2 AM on a Sunday morning?

{{<next-in-series page="/posts/2025/08/aruba-bgp-route-map.md">}}Coming up next: ArubaCX creatively decided when you're done editing a routing policy{{</next-in-series>}}
