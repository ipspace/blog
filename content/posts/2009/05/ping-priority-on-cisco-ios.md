---
date: 2009-05-20T06:29:00.001+02:00
tags:
- network management
- SLA
title: Ping priority on Cisco IOS
url: /2009/05/ping-priority-on-cisco-ios/
---
Every now and then, a really interesting question appears on the cisco-nsp mailing list. A while ago I’ve seen this one:

> I've heard that Cisco devices handle ICMP at a low priority. I found one post describing it handled in process-switching and not fast-switching. Does anyone have an article that explains that process and is it configurable?

Most packets sent to the router are handled in process switching (the packet is queued in the input queue of one of the IOS processes), the obvious exceptions being GRE and IPSec packets (unless they're fragmented).

Packets sent to the router can also be rate-limited with a [control plane policy](/2008/11/control-plane-protection-overview/).

The IOS processes perform their job between interrupts (packets being CEF- or fast switched). A reply to an ICMP packet is therefore a lower-priority task than regular packet forwarding.
