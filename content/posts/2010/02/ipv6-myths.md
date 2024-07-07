---
date: 2010-02-26 09:06:00+01:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- workshop
title: IPv6 Myths
url: /2010/02/ipv6-myths/
---
Once you've spent a few hours trying to understand the implications of IPv6, you quickly realize that the only significant change is the increase in the address length. All the other goals that some people had been talking about were either forgotten or failed due to huge mismatch between idealistic view of the Internet IPv6 developers had 15 years ago and today's reality. However, you still find mythical properties of IPv6 propagated across the Internet. Here are a few I've found; add your favorites in the comments.

{{<note info>}}Numerous IPv6 topics are covered in my [Enterprise IPv6 - the First Steps](https://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) webinar.{{</note>}}

**IPv6 provides service/location separation.** Total nonsense. The only mechanism used to find services is still DNS and it's still used from the wrong position in the protocol stack.
<!--more-->
**IPv6 will reduce IP routing tables.** Not true. IETF had 15 years to solve multihoming issues, but failed to do so. SHIM, SCTP and friends are still in a very experimental stage. If anything, the situation will only get worse, as everyone will try to get PI address space.

**IPv6 will reduce BGP problems.** Just the opposite. Not only will the size of the IPv6 global routing table increase, IPv6 BGP tables use more space (and more bandwidth) than the corresponding IPv4 BGP tables.

**IPv6 has better quality of service.** Total nonsense; the only widespread QoS mechanism is DiffServ that uses DSCP.

**IPv6 has better security.** Not true. IPSec might be better integrated in IPv6 headers, but there's nothing you can do with IPv6 IPSec that you cannot do with IPv4 IPSec.

**Residential IPv6 is less secure because it does not require NAT.** Anyone who thinks NAT is a security feature deserves to become part of a botnet.
