---
date: 2014-07-28 08:06:00+02:00
tags:
- bridging
title: Is STP Really Evil?
url: /2014/07/is-stp-really-evil.html
---
Maxim Gelin sent me an interesting question:

> Can you please explain to me, why is STP supposed to be evil? What\'s wrong with STP?

STP's fundamental problem is that it's a fail-close, not a fail-open protocol.
<!--more-->
Ethernet bridges (later [renamed to *layer-2 switches*](https://blog.ipspace.net/2011/02/how-did-we-ever-get-into-this-switching.html)) were designed to be [transparent plug-and-pray devices](http://blog.ipspace.net/2010/07/bridges-kludge-that-shouldnt-exist.html) that you could drop anywhere into the network and hope they'll work. They could not rely on having a control-plane protocol between adjacent nodes (like most modern routing protocols do) -- lack of control-plane communication indicated lack of adjacent bridges.

That's all nice and dandy until a bridge loses its mind, and stops sending BPDUs ([control plane](https://blog.ipspace.net/2013/08/management-control-and-data-planes-in.html) activity) while still forwarding traffic (data plane activity). Adjacent bridges think they have hosts plugged into the affected ports (this is the *fail close* part), and start forwarding traffic through those ports, resulting in a nice forwarding loop (been there, seen that).

{{<note>}}A bridge with hung control plane would not forward BPDUs between its ports (which would stop the forwarding loop), because the forwarding entry for the [STP multicast address](http://en.wikipedia.org/wiki/Spanning_Tree_Protocol#Bridge_Protocol_Data_Units) still [punts](https://blog.ipspace.net/2013/02/process-fast-and-cef-switching-and.html) packets to the CPU.{{</note>}}

### Fail-Open or Fail-Close?

As Chris Marget mentioned in his comment, the "fail-open" or "fail-close" is a clunky terminology bound to be misunderstood.

Being an oldtimer, I always see computer networks as part of generic electrical circuits and switching landscape -- for me, "fail-close" = "pass current or traffic on failure" and "fail-open" = "stop passing current or traffic".

Other people think about computer networks in valve or door analogies. For them "fail close" means "the door or valve is closed on failure -- there's no traffic" and "fail open" obviously means "the door or valve is opened on failure, and the traffic passes".

In the context of this blog post "fail close" means "a failed/confused bridge continues to forward the traffic, and the bridged network will send the traffic across such bridge."

You might have a different opinion on what "open" or "close" means, and it's as valid as any... but quoting Cisco's documentation won't make your point any more valid (it just proves that the writer of that document agrees with your view of what opens or closes on failure). I would however appreciate a pointer to a more authoritative source (although I doubt it exists).

### Back to Bridging and STP

The solution to the *confused bridge traffic forwarding* problem is quite simple: Cisco IOS has [*bridge assurance*](http://www.netcraftsmen.net/blogs/entry/what-is-bridge-assurance.html) -- you configure a port to expect an adjacent bridge, and the port doesn't forward traffic if it doesn't receive BPDUs from the other end.

The generic solution to this particular problem (and a few others, including hosts turning into bridges) seems to be extremely simple: allow a switch port to be a host-facing port (implicitly configuring *BPDU guard* and a few other things) or a fabric port (implicitly configuring *bridge assurance* and VLAN trunking). Why hasn't [any vendor implemented such a simple concept](https://blog.ipspace.net/2022/02/vtp-insecure.html)? I can't figure it out -- your comments are most welcome!

### It Gets Worse

Fail-close nature of STP isn't its only drawback. The original STP had numerous other challenges, from slow convergence to lack of VLAN awareness. Unfortunately the IEEE decided to keep heaping kludges on top of STP until the whole thing nearly toppled over -- it's like trying to build the global Internet by tinkering with RIP *ad nauseam* instead of designing BGP.

### Revision History

2014-08-01
: Inserted *fail open or fail close* section to reduce the terminology confusion.

