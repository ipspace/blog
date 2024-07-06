---
date: 2019-01-31 08:46:00+01:00
tags:
- IPv6
- segment routing
title: 'SRv6: One Tool to Rule Them All'
url: /2019/01/srv6-one-tool-to-rule-them-all.html
---
I got some interesting feedback from one of my readers on Segment Routing with IPv6 extension headers:

> Some people position SRv6 as the universal underlay and overlay due to its capabilities for network programming by means of feature+locator SRH separation.

Stupid me replied "*SRv6 is NOT an overlay solution but a source routing solution.*"
<!--more-->
{{<note info>}}Want to get a second (or third or fourth) opinion? Check out:

* _[SR(x)6 - Snake Oil Or Salvation?](/2020/08/worth-reading-srx6-snake-oil.html)_
* _[Do We Need Segment Routing?](/2021/10/worth-reading-need-segment-routing.html)_
{{</note>}}

#### So where would I need source routing?

Considering that, where would you need source routing (the ability to specify intermediate hops in the path)? For example, it doesn't work well with service chaining unless your VNFs support it

There are some supposed use cases where you could use your ISP as global transport backbone even when your end sites are connected to another ISP. This might even make sense...

Then there are actual use cases for source routing in WAN edge of large content providers -- they want to send the traffic to from their web proxy servers to some destinations over multiple uplinks. Not surprisingly, every solution along these lines that I'm aware of uses either L2 tricks or MPLS because they work (as opposed to works-with-engineering-code-in-PowerPoint technologies).

#### Back to one-tool-to-rule-them-all

I should have known better. Here's what I got back from the same reader:

> I guess their point is that in case of SRv6 you get a single mechanism that can be used for underlay (like MPLS transport in fabric) and for overlay (send instructions to particular end points where l3vpn should start for example), so instead of MPLS or VXLAN+IP you get SRv6 with IPv6 :)

RFC 1925 Rule 5 immediately comes to mind:

> It is always possible to agglutinate multiple separate problems into a single complex interdependent solution. In most cases this is a bad idea.

In plain English: Just because you could doesn't mean that you should.

In a word: Don't.

Also, if you're looking for a universal tool, why don't you start with this one... and once you cut down a tree with it, and make a table out of that tree, while brushing your teeth, cutting your fingernails, and opening a bottle of wine, do let me know how it worked out.

{{<figure src="/2019/01/s1600-Universal+Tool.jpg">}}
