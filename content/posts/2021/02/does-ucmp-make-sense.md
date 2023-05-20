---
date: 2021-02-25 07:22:00+00:00
sd-wan_tag: details
eigrp_tag: deploy
series:
- UCMP
tags:
- IP routing
- SD-WAN
- EIGRP
title: Does Unequal-Cost Multipathing Make Sense?
---
Every now and then I'm getting questions along the lines "*why doesn't X support unequal-cost multipathing (UCMP)?*" for X in [ OSPF, BGP, IS-IS ]. 

To set the record straight: BGP does support some rudimentary form of unequal-cost multipathing with the *[DMZ Bandwidth](https://tools.ietf.org/html/draft-ietf-idr-link-bandwidth-06)* community, but it only works across multiple egress points from a single autonomous system. [Follow-up nerd knobs](https://tools.ietf.org/html/draft-mohanty-bess-ebgp-dmz-00) described how to use the same community over EBGP sessions; not sure whether anyone implemented that part (comments welcome).
<!--more-->
Now for a more generic question: Why is EIGRP the only protocol with built-in support for unequal-cost multipathing? Why did no-one implement that for OSPF? After all, an OSPF router knows the whole topology of the network, and could "easily" figure out what's safe to use. How about "it doesn't work in real life"?

Imagine a generic solution where a random router in a network performs unequal-cost multipathing. Most modern load balancing solutions use 5-tuple load balancing to spread the load across multiple links as evenly as possible. Sounds perfect for an UCMP deployment, right? 

Well, there is this tiny physical problem called *[latency](https://blog.ipspace.net/2020/02/video-end-to-end-latency-is-not-zero.html)* (yeah, [again](https://blog.ipspace.net/2015/01/latency-killer-of-spread-out.html)). Unequal-cost links probably don't have the same bandwidth or latency (or they wouldn't have unequal costs), and using the generic 5-tuple load balancing some sessions going from a single client to a single server would land on one path and some on the other... in the end resulting in user experience almost equivalent to being on the slower path (as always, the margins of this blog post are too slim for an extensive proof, but do [consider the way most web browsers render a page](https://developer.mozilla.org/en-US/docs/Web/Performance/How_browsers_work)). Alternatively client-to-server traffic could go over the low-latency link, and the server-to-client traffic would return over the high-latency link. Doesn't sound like a win, does it?

OK, so we could limit our design to links with comparable latency. What would make then unequal-cost then? Probably one of them has higher bandwidth.

Now imagine a scenario where the link bandwidth (and not the Mathis formula) is the limiting factor for TCP throughput. Would you really want some sessions to land on the low-bandwidth link and others on the high-bandwidth one in a seemingly random fashion? That would be a great troubleshooting experience, right?

Does that mean that it makes no sense to use multiple unequal uplinks? Absolutely not, the trick is to use them wisely -- identify application requirements, figure out what resources are available, and map the applications to uplinks. This is what SD-WAN is supposed to be doing, and it's how [multipath TCP (MP-TCP) could be used](https://blog.ipspace.net/2019/03/multipath-tcp-on-software-gone-wild.html) for [latency-critical applications](https://blog.ipspace.net/2014/03/ios-uses-multipath-tcp-does-it-matter.html) like Siri. 

As always, the [complex decisions belong to the network edge](https://blog.ipspace.net/2011/05/complexity-belongs-to-network-edge.html), ideally next to the application stack ([not that anyone would listen](https://blog.ipspace.net/2013/06/network-virtualization-and-spaghetti.html)), while the network core should be kept as simple as possible. Anything else will give you job security and frantic midnight phone calls. The choice is yours.