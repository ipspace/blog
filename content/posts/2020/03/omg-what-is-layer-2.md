---
title: "OMG: What Is Layer-2"
tags: [ bridging, overlay networks ]
date: 2020-03-23 08:12:00
inspiration: https://www.iquila.com/About/What-is-Layer2/
---
Found this "gem" describing the differences between layer-2 and layer-3 on an unnamed $vendor web site.

> Layer 2 is mainly concerned with the local delivery of data frames between network devices on the same network or local area network (LAN).

So far so good...
<!--more-->
> As soon as data needs to travel outside of the LAN it needs to be encoded into a data packet that can be forwarded, using a router, between computer networks.

And how was data encoded before that? Wrapped in an ethereal mist? But wait, it gets better...

> The data is then sent across the Internet (Layer 3), bouncing off any number of servers, trying to find the fastest path to its intended target.

Excuse me? Servers, routers, bouncing... potayto, potahto?

> Once it reaches its target the packet is decoded back into a data frame by the router and is now able to move around the host LAN on Layer 2.

This is not how I was told things work, but who knows...

> Until now, without using either an MPLS or Ethernet line (both of which have significant drawbacks), [long distance] Layer 2 was not possible.

I remember laughing at Cisco's Lan Extenders decades ago, and bridging over GRE or VXLAN is shipping with every Linux distro. VMware NSBU would also disagree - they shipped L2VPN with NSX-V years ago.

> Within a LAN on Layer 2 the data is in its original, intended form. As soon as it needs to pass over Layer 3 it gets encoded, sent out, bounced off any number of servers, received, decoded and sent on.

And now I understand the obsession some people have with stretched VLANs. They want to keep data in its original, intended form.

> On this journey across the Internet, the data will try to find the path of least resistance, in order to get to its destination as quickly as possible. This can cause latency issues for various data hungry applications and can mean the quality of service suffers.

And I think we have a winner ;))

In case you're wondering what product this company is shipping, here's a high-level overview:

> $VENDOR has developed a unique protocol to deliver Layer 2 without MPLS lines or Ethernet lines. In essence, your organization can connect remote workers, satellite sites, branches and offices in any location as if they were plugged in to a LAN port in your head office.

Yeah, that makes perfect sense the moment someone starts a broadcast storm, but let's not go there.

Regardless of that last bit... Is it just me, or should we expect people promoting their products to have some baseline understanding of what they're doing? It's not like there would be a dearth of information on [how networks really work](https://www.ipspace.net/How_Networks_Really_Work) - several good textbooks are freely available on the Internet (check the "Textbooks" part of [this page](https://my.ipspace.net/bin/list?id=Fundamentals)), but of course it does take a bit of mental effort to understand what's in them.