---
title: "AMS-IX Outage: Layer-2 Strikes Again"
date: 2023-12-06 08:18:00
tags: [ switching ]
---
On November 22nd, 2023, AMS-IX, one of the largest Internet exchanges in Europe, experienced a significant performance drop lasting more than four hours. While its peak performance is around 10 Tbps, it dropped to about 2.1 Tbps during the outage.

AMS-IX published a [very sanitized and diplomatic post-mortem incident summary](https://www.ams-ix.net/ams/outage-on-amsterdam-peering-platform) in which they explained the outage was caused by *LACP leakage*. That phrase should be a red flag, but let's dig deeper into the details.
<!--more-->
Reading the incident report, it seems to me (and I would love to be corrected) that Juniper switches used by AMS-IX forward LACP packets received on a non-LAG port to other bridged[^SP] ports on the same switch. As much as I'm trying, I can't figure out in which universe that would be anywhere close to a sane choice.

[^SP]: Let's stop pretending: a layer-2 switch is really an IEEE bridge with too many nerd knobs that can evidently cause significant harm.

LACP (Link Aggregation Control Protocol) was designed to be used between adjacent devices. While I know we have to live with [abominations like two devices pretending they're a single system](https://blog.ipspace.net/series/mlag.html), I lack polite words to describe the idea of forwarding layer-2 control packets that are supposed to be used between adjacent devices onto other links. Unfortunately, I'm also aware of potential MacGyver-type use cases for that monstrosity: let's buy two Carrier Ethernet links and pretend we can bundle them into an end-to-end Link Aggregation Group.

However, even if the vendor account teams dazzled by a humongous purchase order can get persuaded that a bridge needs such a dangerous nerd knob, one would hope that configuring it would be hard and would generate all sorts of "_if you do this, the universe might collapse into a black hole_" type of warnings[^GWAF]; one can only hope flooding packets sent to well-known IEEE-defined MAC addresses is not the default behavior, but then [boxes from the same company happily talk BGP with total strangers](https://blog.ipspace.net/2023/10/reject-unknown-bgp-session.html#ugly). Feedback from anyone familiar with Junos layer-2 implementation would be most welcome.

[^GWAF]: If that's the case on Juniper boxes, then AMS-IX got what they had asked for.