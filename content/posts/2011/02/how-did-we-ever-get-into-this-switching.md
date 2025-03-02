---
date: 2011-02-08 09:17:00.002000+01:00
networking-fundamentals_tag: rant
tags:
- bridging
- switching
- IP routing
- networking fundamentals
title: How Did We Ever Get Into This Switching Mess?
url: /2011/02/how-did-we-ever-get-into-this-switching/
---
If you're confused about the numerous meanings of a *switch*, you're not the only one. If you wonder how the whole mess started, here's the full story (from the biased perspective of a [grumpy GONER](http://etherealmind.com/network-dictionary-goners/)):

In the early 1980s, there were no bridges or routers. Hosts communicated directly with each other or used intermediate nodes (usually hosts, sometimes dedicated devices called *gateways*) to pass traffic. Networking engineers' lives would have remained simple were it not for a few overly bright engineers at DEC who decided their application ([LAT](http://en.wikipedia.org/wiki/Local_Area_Transport)) would run directly on layer 2 to make it faster.

{{<note>}}Their company imploded (actually, it was [sold in pieces](http://en.wikipedia.org/wiki/Digital_Equipment_Corporation#Final_years)) in the previous millennium, but their eagerness to cut corners still haunts every one of us.{{</note>}}
<!--more-->
When someone managed to sell too many devices to a single customer (probably ignoring every design recommendation ever made \... isn't that how progress is made?), and they could no longer fit onto the same [thick Ethernet](http://en.wikipedia.org/wiki/10BASE5) segment, [DEC built a transparent bridge](/2010/07/bridges-kludge-that-shouldnt-exist/) (and Radia Perlman designed STP).

At the same time, the number of protocols running on Ethernet (and other now-extinct technologies, including [ARCNET](http://en.wikipedia.org/wiki/Arcnet) and [LocalTalk](http://en.wikipedia.org/wiki/Appletalk#Physical_implementation)) exploded (the early CCIEs might "fondly" remember all the protocols we had to configure in the lab). Each of these protocols needed its own gateway (= router) devices and [Bill Yeager](http://en.wikipedia.org/wiki/William_Yeager) at Stanford got a brilliant idea: let's make a dedicated device that will serve as a gateway to all of them \... and thus multiprotocol routers (initially still called *gateway*; that how [AGS](http://steverossen.com/a-picture-worth-sharing/) got its name) and [Cisco](http://en.wikipedia.org/wiki/Cisco#Corporate_history) were born.

Routers were way more complex (and expensive) than bridges, so someone got the next bright idea: let's use bridges to connect remote sites. While that might be survivable ([but still stupid](/2009/05/vpls-is-not-aspirin/)) for a few small remote sites today. We used very slow WAN links in those days (64 kbps was a high-speed link), and the crazy and overly brave engineers building large bridged networks produced numerous catastrophic failures. Based on those events, *bridge* became a much-hated word, and everyone understood that *routers are good, bridges are bad*.

Fast-forward a few years. Twisted pair attachments to hubs replaced thick and thin coax Ethernet cables, and several startup companies had another great idea: let's replace a hub with a bridge; it will boost performance and decrease the number of collisions (and potentially transmission errors).

{{<note>}}Of course, they forgot to mention increased latency (or played with the *cut-through switching*), but let's not go there.{{</note>}}

These startups faced a serious problem: They had a bridge, but nobody wanted to buy one (because bridges are bad), so some fateful marketing department invented a switch. The new mantra is: hubs are slow, switches are fast.

Even in those early days, some people figured out not every host (or user) belonged to the same LAN segment. They wanted to implement LAN segmentation and decided to do it with higher-speed routers (Cisco 7000 was a pretty popular option). The design worked but had a significant drawback: high-speed multi-protocol routers were always expensive. The mantra changed again: *routers are expensive, switches are more cost-effective*.

{{<note>}}Some newbies who firmly believed marketing claims made by various vendors decided (yet again) to build WAN networks with switches (because routers were expensive) and (predictably, inevitably, and sometimes quite spectacularly) failed.{{</note>}}

Because the routers were so expensive (and switches already had hardware-based forwarding), networking vendors tried to combine the best of both worlds. Some of you might still remember the early days of Netflow and Multi-Layer Switching (where the router would inspect initial packets in a session and download the flow specification to the switches \... the craziness later resurrected in OpenFlow).

Finally, someone managed to implement cost-effective layer-3 forwarding in hardware, resulting in high-speed, reasonably-priced routers \... only you couldn't call those devices *routers* anymore because *routers are expensive*, so they stretched the definition of switching to include *layer-3 switching* (the process formerly known as *routing*).

Is there a way out of this switching mess? Unfortunately, it looks like we're way past the [point of no return](http://en.wikipedia.org/wiki/Point_of_no_return).

**But remember**: regardless of how you decide to call the physical (or virtual) device that forwards the data across your network, it's essential to understand whether it forwards the data based on *physical layer-2 addresses* (we called that *bridging*) or based on *logical, hierarchical layer-3 addresses* (what we called *routing* 20 years ago) because there are [significant differences between routing and bridging](/2010/07/bridging-and-routing-is-there/) ([maybe even more than you think](/2010/07/bridging-and-routing-part-ii/)).
