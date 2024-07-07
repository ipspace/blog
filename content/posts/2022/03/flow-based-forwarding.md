---
date: 2022-03-08 06:12:00+00:00
series:
- forwarding
tags:
- networking fundamentals
- switching
title: Flow-Based Packet Forwarding
---
In the _[Cache-Based Packet Forwarding](/2022/02/cache-based-forwarding/)_ blog post I described what happens when someone tries to bypass the complexities of IP routing table lookup with a forwarding cache. 

Now imagine you want to implement full-featured fast packet forwarding including ingress- and egress ACL, NAT, QoS... but find the required hardware (TCAM) too expensive. Wouldn't it be nice if we could send the first packet of every flow to a CPU to figure out what to do with it, and download the results into a high-speed flow cache where they could be used to switch the subsequent packets of the same flow. Welcome to *[flow-based packet forwarding](/2015/12/is-flow-based-forwarding-just-marketing/)*.
<!--more-->
The first company (I'm aware of) that tried this approach was Ipsilon Networks. They wanted to use an ATM fabric to compete with IP routers, quickly figured out that one cannot implement the required functionality in ATM, and tried to bypass the limitations of their hardware with [Flow Management Protocol](https://www.rfc-editor.org/rfc/rfc1953.html). Never heard of Ipsilon Networks? That should tell you how well that idea worked.

The initial failure didn't discourage the designers of Catalyst 5000. When trying to ~~paint layers of lipstick on an ugly pig~~ convert a layer-2 switch into a layer-3 switch someone got a fantastic idea: what if we would attach a router-on-a-stick to the switch, and let the router do all the hard work, offloading the results to the forwarding hardware. Thus Netflow Switching was born (later renamed to Multilayer Switching[^MLS]), and the later models repackaged the external router into a supervisor daughterboard ([more details](https://web.archive.org/web/20200623042013/http://etutorials.org/Networking/Lan+switching+fundamentals/Chapter+3.+Catalyst+Switching+Architectures/In+the+Beginning-Catalyst+50005500+Project+Synergy/) saved from the oblivion by the Internet Archive).

Everyone who's old enough to have hands-on experience with Catalyst 5000 probably also has nightmares about corner cases where MLS broke and Cisco TAC had to tell you about a secret nerd knob that fixed the problem even though you never understood what exactly was going on behind the scenes. It turns out that you have to solve more than just the obvious problem of cache sizes and cache trashing when you want to cheat and implement a full-blown router with a flow cache. The next attempt: repackage a full-blown Cisco 7500 router into a Catalyst 5000 linecard called [Route Switch Module (RSM)](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-5000-series-switches/10578-56.html#architecture). That worked (of course it did) but inter-VLAN packet forwarding was limited by the forwarding performance of the RSM.

[^MLS]: At least that's how I remember that particular marketing exercise. Please feel free to correct my errors.

After Catalyst 5000 died (based on some EOL documents I found it might have been around 2008) it seemed like the networking industry learned the lesson and moved on... until the next generation of academics who failed to learn from past mistakes reinvented flow forwarding with OpenFlow[^OF]. The initial OpenFlow idea looked surprisingly simple (in PowerPoint):

[^OF]: OpenFlow could be used to implement sane architectures, but for whatever reason every PowerPoint I've seen in those days described flow forwarding. It was too easy to point out why it would never work...

* Send the first packet of every flow to an SDN controller
* Figure out what to do with the flow
* Install flow entries to all switches in the path.

They even managed to solve global load balancing with that... at an [astonishing scale of several VoIP calls per minute](/2011/10/openflow-and-state-explosion/). In reality, most OpenFlow implementations managed to insert about [1000 flow entries into the forwarding hardware per second](/2012/01/fib-update-challenges-in-openflow/) -- a bit slow for a terabit switching fabric.

But surely that's just a hardware limitation; [software-based flow based forwarding should work just fine](/2013/04/open-vswitch-under-hood/)... or so the authors of Open vSwitch thought until they tried to make it work in production. Cache trashing and dismal performance were the obvious results until they decided to [implement megaflows](https://networkheresy.com/accelerating-open-vswitch-to-ludicrous-speed/) which [brought the forwarding performance to a *ludicrous speed* of 1 Gbps](/2014/11/open-vswitch-performance-revisited/) at the time when VMware managed to push 40 Gbps of VXLAN traffic out of a single server. In a later release, they implemented an even better flow-matching algorithm which boosted the flow cache matching performance, but they were still far away from what one could do in those days with an optimized packet forwarding implementation (example: [20 Gbps *per CPU core*](/2016/03/x86-based-switching-at-ludicrous-speed/) in 2016)[^OVSP]. 

[^OVSP]: Have to admit I got bored after that and walked away. If you happen to have recent OVS performance figures please post a comment.

### But It Does Work Sometimes

[Erik Auerswald](https://www.linkedin.com/in/erik-auerswald-2b8b73171/) made some excellent remarks about real-life flow-based forwarding in a comment to the _[Cache-Based Packet Forwarding](/2022/02/cache-based-forwarding/)_ blog post:

> Firewalls, i.e., devices where network topology is just a small part of the forwarding decision, often employ flow caches (for individual data flows) for performance optimization. In some "high-end" firewalls this flow cache is offloaded to hardware. Since per flow offload is often the best such a device can use, it is done in practice, and usually works well enough.

Apart from good engineering (which was somewhat lacking in the early versions of Open vSwitch), the difference between firewall-based flow forwarding and Catalyst 5000 has to do with the problem they're trying to solve. Firewalls usually filter unicast IP flows, whereas we were throwing all sorts of crazy scenarios at Catalyst 5000, from unicast flooding to IP multicast. Imagine how much fun it must be to generate a flow record for a flooded flow that's filtered on some outgoing ports and NATed at some others.

Speaking of hardware offload, Arista implemented the ultimate solution in its [DirectFlow Assist for Palo Alto firewalls](https://www.arista.com/assets/data/pdf/Whitepapers/AristaPAN_Solution_Brief.pdf). An Arista switch would monitor firewall syslog messages and install flow entries into TCAM to bypass the firewall for accepted high-volume flows like backups. I have never heard of anyone using that solution though.

Erik also mentioned interesting experience with Enterasys switches:

> Regarding networking devices primarily used for routing and bridging, the Enterasys Networks N-Series and their successors, K-Series and S-Series, based on CoreFlow resp. CoreFlow2 ASICs, used caching of individual flows in hardware forwarding tables as their only forwarding architecture. In practice, those switches worked well in the "enterprise" networks they were designed for. Of course it was possible to create overload with specific tests to demonstrate the potential for problems.

It's nice to hear someone made hardware flow-based forwarding work in production networks (I never heard anything bad about Enterasys), but it's also worth keeping in mind that we're talking about gigabit campus edge devices with approximately 200 Gbps of throughput ([source](https://www.networkworld.com/article/2201700/enterasys-bolsters-switches-with-automation--access-control.html)). Assuming an average flow generates 1 MB of traffic, we're talking about ~25.000 flow setups (packet inspections) per second, which still seems to be a bit on the high side considering you'd be attaching individual users and access points to those gigabit ports. Anyway, you can get it done with a decent CPU and well-engineered hardware architecture that enables to CPU to push that many flow records into forwarding hardware.

There's another benefit of using (large enough) hardware flow cache: it can be [implemented as a hash table instead of TCAM](/2022/02/packet-forwarding-header-lookup/) -- the device could implement complex policies in software and use cheaper hardware for high-speed packet forwarding. Back to Erik:

> Since per flow hardware offload allowed implementing complex, but still high performance, traffic filtering policies, replacing CoreFlow(2) based devices with networking devices using topology based forwarding often provided challenges regarding traffic filtering policies (i.e., either keep complex line-rate traffic filters, or use a different networking device with faster interfaces and topology based forwarding, but not both).

## Remain Skeptical

Flow-based forwarding is a tool like any other, but it has to be used correctly. Unfortunately, we've seen too many failed attempts to implement flow-based forwarding to accept vendor claims at face value. Whenever someone starts selling you the beauties of a revolutionary product based on flow forwarding, remember to:

* Remain skeptical
* Start by adding "_Works Best In PowerPoint_" to the marketing message
* Do you homework and figure out the limitations
* Run thorough tests to validate the claims.



