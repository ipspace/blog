---
title: "Flow-Based Packet Forwarding"
date: 2022-03-08 06:12:00
tags: [ networking fundamentals, switching ]
series: forwarding
---
In the _[Cache-Based Packet Forwarding](https://blog.ipspace.net/2022/02/cache-based-forwarding.html)_ blog post I described what happens when someone tries to bypass the complexities of IP routing table lookup with a forwarding cache. 

Now imagine you want to implement full-featured fast packet forwarding including ingress- and egress ACL, NAT, QoS... but find the required hardware (TCAM) too expensive. Wouldn't it be nice if we could send the first packet of every flow to a CPU to figure out what to do with it, and download the results into a high-speed flow cache where they could be used to switch the subsequent packets of the same flow. Welcome to *[flow-based packet forwarding](https://blog.ipspace.net/2015/12/is-flow-based-forwarding-just-marketing.html)*.
<!--more-->
The first company (I'm aware of) that tried this approach was Ipsilon Networks. They wanted to use an ATM fabric to compete with IP routers, quickly figured out that one cannot implement the required functionality in ATM, and tried to bypass the limitations of their hardware with [Flow Management Protocol](https://www.rfc-editor.org/rfc/rfc1953.html). Never heard of Ipsilon Networks? That should tell you how well that idea worked.

The initial failure didn't discourage the designers of Catalyst 5000. When trying to ~~paint layers of lipstick on an ugly pig~~ convert a layer-2 switch into a layer-3 switch someone got a fantastic idea: what if we would attach a router-on-a-stick to the switch, and let the router do all the hard work, offloading the results to the forwarding hardware. Thus Netflow Switching was born (later renamed to Multilayer Switching[^MLS]), and the later models repackaged the external router into a supervisor daughterboard ([more details](https://web.archive.org/web/20200623042013/http://etutorials.org/Networking/Lan+switching+fundamentals/Chapter+3.+Catalyst+Switching+Architectures/In+the+Beginning-Catalyst+50005500+Project+Synergy/) saved from the oblivion by the Internet Archive).

Everyone who's old enough to have hands-on experience with Catalyst 5000 probably also has nightmares about corner cases where MLS broke and Cisco TAC had to tell you a secret nerd knob that fixed the problem even though you never understood what exactly was going on behind the scenes. It turns out that you have to solve more than just the obvious problem of cache sizes and cache trashing when you want to cheat and implement a full-blown router with a flow cache. The next attempt: repackage a full-blown Cisco 7500 router into a Catalyst 5000 linecard called [Route Switch Module (RSM)](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-5000-series-switches/10578-56.html#architecture). That worked (of course it did) but inter-VLAN packet forwarding was limited by the forwarding performance of the RSM.

[^MLS]: At least that's how I remember that particular marketing exercise. Please feel free to correct my errors.

After Catalyst 5000 died (based on some EOL documents I found it might have been around 2008) it seemed like the networking industry learned the lesson and moved on... until the next generation of academics who failed to learn from past mistakes reinvented OpenFlow. The initial OpenFlow idea looked surprisingly simple (in PowerPoint):

* Send the first packet of every flow to an SDN controller
* Figure out what to do with the flow
* Install flow entries to all switches in the path.

They even managed to solve global load balancing with that... at an [astonishing scale of several VoIP calls per minute](https://blog.ipspace.net/2011/10/openflow-and-state-explosion.html). In reality, most OpenFlow implementations managed to insert about [1000 flow entries into the forwarding hardware per second](https://blog.ipspace.net/2012/01/fib-update-challenges-in-openflow.html) -- a bit slow for a terabit switching fabric.

But surely that's just a hardware limitation; [software-based flow based forwarding should work just fine](https://blog.ipspace.net/2013/04/open-vswitch-under-hood.html)... or so the authors of Open vSwitch thought until they tried to make it work in production. Cache trashing and dismal performance were the obvious results until they decided to [implement megaflows](https://networkheresy.com/accelerating-open-vswitch-to-ludicrous-speed/) which [brought the forwarding performance to a *ludicrous speed* of 1 Gbps](https://blog.ipspace.net/2014/11/open-vswitch-performance-revisited.html) at the time when VMware managed to push 40 Gbps of VXLAN traffic out of a single server. In a later release, they implemented an even better flow-matching algorithm which boosted the flow cache matching performance, but they still aren't anywhere close to what one can do with an optimized packet forwarding implementation (example: [20 Gbps *per CPU core*](https://blog.ipspace.net/2016/03/x86-based-switching-at-ludicrous-speed.html) six years ago).

**Long story short**: whenever someone starts selling you the beauties of a revolutionary product based on flow forwarding, remember to add "_Works Best In PowerPoint_".