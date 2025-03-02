---
date: 2021-04-21 08:20:00+00:00
networking-fundamentals_tag: deep
tags:
- switching
- networking fundamentals
title: 'Response: Is Switching Latency Relevant?'
---
Minh Ha left another extensive comment on my *[Is Switching Latency Relevant](/2021/04/switching-latency-relevant/)* blog post. As is usual the case, it's well worth reading, so I'm making sure it doesn't stay in the small print (this time interspersed with a few comments of mine in gray boxes)

---

I found Cisco apparently manages to [scale port-to-port latency down to 250ns for L3 switching](https://www.cisco.com/c/dam/en/us/products/collateral/switches/nexus-3550-series/esg-white-paper-ultralowlatency.pdf), which is astonishing, and way less (sub 100ns) for L1 and L2.

I don't know where FPGA fits into this ultra low-latency picture, because FPGA, compared to ASIC, is bigger, and a few times slower, due to the use of Lookup Table in place of gate arrays, and programmable interconnects.
<!--more-->
{{<long-quote>}}
No-one is talking about this in public (for obvious reasons), but what I've heard pointed in the direction of pre-processing data streams in FPGA before they even hit the switch-to-server links, probably to reduce the server CPU load/latency. 

You could do that in a switch or in a server NIC, and you could get plenty of bandwidth into a server these days, so the solution you're trumpeting depends on what you're selling ;)
{{</long-quote>}}

In any case, looking at their L2 and L1 numbers, it's too obvious the measurement was taken in zero-buffer and non-contentious situations. In the real world, with realistic heavily bursty, correlated traffic, they all perform way less than their ideal case. But regardless, L3 switching at 250ns even under ideal condition is highly impressive, given Trident couldn't achieve it in any of their testing scenarios.

{{<long-quote>}}To be fair, Trident chipset was not designed for ultra-low-latency environment. It's like comparing Ford Fiesta with Porsche 911 -- one of them is much faster, but also a bit more expensive.{{</long-quote>}}

Again, I'm not bashing Broadcom. It's just I find it laughable reading their apologies in their report you linked to, wrt how they don't "optimize" for 64-byte packets (love their wording), and how they manage to find a way to make their competitor finish far behind in the tests. Granted, Mellanox was trying the same thing in their test against Broadcom, so they're all even, and we should only take these so-called vendor-released testing reports with a grain of salt.

{{<long-quote>}}Yet again, not many people care about 64-byte packet forwarding performance at 100 Gbps speeds. The only mainstream application of 64-byte packet forwarding I found was VoIP.

It's a bit hard to generate large packets full of voice if you have to send them every 20 msec (the default interval [specified in RFC3551](https://tools.ietf.org/html/rfc3551#page-12)), and it's even harder to generate 3.2 Tbps of voice data going through a single top-of-rack switch. Unless my math is wrong, you'd need over 100 million concurrent G.729A-encoded VoIP calls to saturate the switch. Maybe we should focus on more realistic use cases.{{</long-quote>}}

The elephant in the room that you alluded to, is most likely endpoint latency. It's pretty irrelevant to talk about ns middlebox-latency when the endpoints operate in the ms range :p . And endpoint latency gets even worse when features like interrupt coalescing and LSO/GRO are in place. Must be part of the reason why the Cloud's performance for scientific apps sucks, and funny enough, they actually admit it as I found out recently.

But IMO, that only means the server operating system, the hypervisor, the software switch etc, are the ones that need innovation and up their game, instead of using their pathetic latency figures as an excuse not to keep bettering routers' and switches' performance. Overlay model is notoriously slow because it's layer on top of layer (think BGP convergence vs IGP convergence), and as mentioned in your previous post, Fail fast is failing fast: "If you live in a small town with a walking commute home, you can predictably walk in the front door at 6:23 every evening. As you move to the big city with elevators, parking garages, and freeways to traverse, it's harder to time your arrival precisely," that kind of overburderned, complex architecture is not deterministic and no good for applications with real-time requirements. Infiniband shied away from TCP/IP for the same reason, and used a minimal-stack model to keep their latency low.

The Cloud and their overlay model is a definitely a step backward in terms of progress. By doing it cheap, they make it slow. Good for their greedy shareholders, sucks for consumers who truly need the numbers.

{{<long-quote>}}Don't blame the shareholders for what the customers are not willing to pay for. Public cloud is like public transport -- it will eventually get you reasonably close to where you want to go at a reasonable price.

If you need to get there faster, or if you want to get to a weird place far away from public transport, you take a taxi (bare-metal instance), and if you move around so much that taxies become too expensive, you buy a car. Using any utility in the way it was not designed to be used (because it's cheaper that way) and complaining about the results you deserve is ridiculous.{{</long-quote>}}

Well, I guess I can stop complaining now that bare-metal instances are a thing. But yeah, taken as a whole, basically technology winter seems to continue. These days about the only kind of progress we have is corporate-PR progress.

Speaking of HFT, there seems to be a lot of fanfare going on there when it was big some 10 yrs ago. FPGA was often mentioned as the way they sped up their end-to-end latency. But I ran across comments of some of the guys who actually did HFT for a living sometime back, and they said it's all hot-air, with most of the stuff they try to optimize being on the software level, such as doing away with message queuing (and so, safely getting rid of locks) to unburden their programs of concurrency synchronization, which is a big latency killers. Staying away from language that performs garbage collection is another thing, as there's no one-size-fit-all garbage collection algorithm that's optimized for all use case, and regardless, it's an additional layer compared to explicit memory management, and more layer means slower.

{{<long-quote>}}I would suspect that not all HFT players are equal. Some of them sit at a stock exchange, and try to make money by being as fast as possible. For example, IEX [claims](https://en.wikipedia.org/wiki/IEX#Operating_principles) it can *execute trades* in 320 microseconds and uses equal-length fiber cables to all participants to ensure fairness. Shaving off microseconds makes perfect sense in such an environment.

Others work globally, care about latency on trans-continental links, and optimize their software stack. Using FPGAs makes no sense if your baseline latency is 50 msec.{{</long-quote>}}

From what I know of RenTech, one of the biggest if not the biggest HFT (they also do other algorithmic trading besides HFT), they rely on software with big-data models, not fancy hardware.