---
title: "Does Small Packet Forwarding Performance Matter in Data Center Switches?"
date: 2021-05-13 07:39:00
tags: [ data center, switching ]
---
**TL&DR**: No.

Here's another never-ending [vi-versus-emacs-type](https://en.wikipedia.org/wiki/Editor_war) discussion: merchant silicon like [Broadcom Trident cannot forward small (64-byte) packets at line rate](/2014/05/how-line-rate-is-line-rate.html). Does that matter, or is it yet another stimulating academic talking point and/or red herring used by vendor marketing teams to justify their high prices?

Here's what I [wrote about that topic](/2021/04/response-switching-latency.html) a few weeks ago:
<!--more-->
{{<long-quote>}}
Not many people care about 64-byte packet forwarding performance at 100 Gbps speeds. The only mainstream application of 64-byte packet forwarding I found was VoIP.

It’s a bit hard to generate large packets full of voice if you have to send them every 20 msec (the default interval specified in RFC3551), and it’s even harder to generate 3.2 Tbps of voice data going through a single top-of-rack switch. Unless my math is wrong, you’d need over 100 million concurrent G.729A-encoded VoIP calls to saturate the switch. Maybe we should focus on more realistic use cases.
{{</long-quote>}}

Not surprisingly, Minh Ha disagreed with me:

{{<long-quote>}}
TCP ACK is min-size 64 bytes, and small packet 200-300 bytes or less are quite common in DC, including FB DCs. TCP ACKs take up a fair amount of traffic in the Internet and also inside a DC, so for this reason alone it's worth having a chipset capable of processing 64-byte packets efficiently. And since 100GE links are normally aggregate links, they accumulate even more of those small packets from different sources. That makes small-packet processing even more important.
{{</long-quote>}}

It's obviously time to step back and do some Fermi estimates. Let's take [Juniper QFX5130 switch](https://www.juniper.net/us/en/products-services/switching/qfx-series/qfx5130/) (supposedly [built on Trident-4](https://blogs.juniper.net/en-us/engineering-simplicity/juniper-networks-introduces-new-400g-dc-switch-to-power-customized-services)). They claim 25.6 Tbps and 5.68 Gpps forwarding performance. Dividing these two results in  line-rate forwarding performance for packets longer than 560 bytes... but they're using marketing math[^1], counting each packet as it enters the switch and leaves it, so the real line-rate forwarding performance starts around 280-byte packets. The true minimum packet size is probably a bit smaller due to FCS and inter-frame gap (yes, vendor marketers include them in bandwidth-focused forwarding performance).

[^1]: Considering that they claim 25.6 Tbps forwarding performance on a switch with 32 x 400GE ports (= 12,8 Tbps of bandwidth), I'm pretty sure we can use the lower number.

Anyway, that performance is still good enough for *200-300 byte packets*. What about TCP ACKs? As it turns out, TCP usually sends an ACK packet for every data packet, which means that there could never be more 64-byte ACK packets than large (1500-byte) data packets. Assuming that mix, the average packet size would be around 780 bytes -- yet again, Broadcom silicon's performance is more than good enough.

But what if I'm wrong and there are tons of smaller TCP data packets? In that case there's either something badly wrong with your TCP stack, or you're running some sort of request-response protocol using small packets, in which case you won't be able to saturate the fabric links anyway due to RTT and endpoint latency. The details are left as an exercise for the reader.

Could there be another scenario that would result in gazillions of small packets? Probably -- and I'd love to hear about it. If you're aware of a real-life application that can generate 12.8 Tbps worth of small packets on servers connected to a single ToR switch, please leave a comment.

For everyone else, here's the TL&DR version of this debate: Broadcom doesn't implement line-rate forwarding of small packets because their target audience knows they don't need it, and implementing it would just make their silicon unnecessarily expensive.

But what if you're running one of those ultra-high-speed unicorn applications that I haven't heard of yet? Stop complaining, figure out your traffic profile, and use fewer ports on the switch if needed. Problem solved.
