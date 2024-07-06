---
title: "Rant: Broadcom and Network Operating System Vendors"
date: 2021-02-02 06:35:00
tags: [ switching ]
---
Minh Ha left the following rant as a comment on my 5-year-old _[What Are The Problems with Broadcom Tomahawk?](/2016/05/what-are-problems-with-broadcom.html)_ blog post. It's too good to be left gathering dust there. Counterarguments and other perspectives are highly welcome.

---

So basically a lot of vendors these days are just glorified Broadcom resellers :p. It's funny how some of them try to up themselves by saying they differentiate their offerings with their Network OS. 
<!--more-->
First off, since all the heavy-weight data forwarding is done in the LC and the fabric, their devices, regardless of brand name, are essentially Broadcom routers/switches first and last. No matter how their OS is written, they will get stuck with Broadcom-provided fabric architecture and forwarding pipeline, with all of its limitations, sometimes severe ones like the horrible fabric scheduler that get pointed out in the Mellanox test.

I won't go into too much detail here as it will dilute the bigger point I'm trying to get at, but as we've discussed before, providing line-rate for 64-byte packet at 100Gbps is mostly mission impossible, considering that packets arrive every 6.7 ns and you have probably less than half that time to finish an IP lookup if you want to make it in time. Couple that with a port count of 32 or 64, and basically classic crossbar fabric arbitration using central scheduler doesn’t work anymore, as the scheduler will become both the bottleneck and power hot-spot, and one will have to use distributed schedulers to scale. 

From what Enrique observed and the way it played out accordingly in the Mellanox test, Broadcom's approach to scheduling -- basically centralized and attempt to compensate for its inefficiency by using grouping with 2 schedulers -- is nonsensical and pathetic. Why bother promoting 400Gbe when you’re clearly incapable of handling 100Gbe properly? And believe it or not, small-packet line-rate processing is very important; DDOS survival for ex, needs that, plus it means when you start providing value-added classification besides basic IP lookup, your router won’t fall over.

Second, when it comes to Network OS, Cisco and Juniper have been in business for 36 and 24 years respectively, and as they got all the highest-class protocol implementers like Dave Katz and Henk Smit working for them during their formative years, their core routing and switching codes had matured and stabilized before some of the new vendors even came to be, so for younger vendors trying to differentiate themselves using the OS is laughable. Who trusts their code to be bug-free, esp. when it comes to complex protocols like OSPF, BGP, and yes, xLFA :p.

All in all, these 2 points make it totally unjustifiable for merchant-silicon vendors these days to charge a premium for what amounts to essentially commoditized, off-the-shelf products.

Monopoly is never good for any industry, and networking is no exception. Among other things, it stiffens innovation. And the result is what we've been witnessing for a long time now, lazy networking and second-tiered products. Many vendors hardly invent anything these days anymore except crappy 'new' encapsulation formats. And Broadcom, as they don't have any sizable competitor that can threaten their domination, they won't feel the need to improve and fix all the nasty dogshit in their chipsets anymore.

And vendors still have to wonder why cloud companies are taking their business away :p. They only have themselves and their laziness to blame. The prize for not reinventing yourself is a one-way ticket to oblivion.

On that note, vendors like Cisco and Juniper, who're trying hard the old-school way, to produce their own silicons, are worth admiring, no matter what the quality of their products. They deserve credit for at least trying.