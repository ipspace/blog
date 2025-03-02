---
date: 2019-10-16 08:18:00+02:00
networking-fundamentals_tag: history
tags:
- networking fundamentals
title: How Did We End With 1500-Byte MTU?
url: /2019/10/how-did-we-end-with-1500-byte-mtu/
---
A subscriber sent me this intriguing question:

> Is it not theoretically possible for Ethernet frames to be 64k long if ASIC vendors simply bothered or decided to design/make chipsets that supported it? How did we end up in the 1.5k neighborhood? In whose best interest did this happen?

Remember that Ethernet started as a shared-cable 10 Mbps technology. Transmitting a 64k frame on that technology would take approximately 50 msec (or as long as getting from the East Coast to the West Coast). Also, Ethernet had no tight media access control like Token Ring, so it would be possible for a single host to transmit multiple frames without anyone else getting airtime, resulting in unacceptable delays.
<!--more-->
Eventually, you have to send the traffic to WAN links. Either you do fragmentation on WAN edge routers (bad) to reduce the transmission latency, or you have to limit frame size on LAN to something reasonable.

There's also the bit error rate. The probability of receiving a 1.5K frame without errors is approximately 40x (64/1.5 to be precise) higher than the probability of receiving a 64K frame without errors. I'm oversimplifying, and I should really use the inverse probability to N-th power (watch the awesome [Reliability Theory](https://www.ipspace.net/Reliability_Theory:_Networking_through_a_Systems_Analysis_Lens) webinar for more details), but with low-enough error rate, I'm not far off. For even more details, see the excellent comment by Innokentiy below.

Finally, there's the buffering problem. Without the hardware capability to split incoming packets into smaller chunks (call them cells, fragments, segments, or whatever else you want), every buffer has to be as large as the largest frame. That's not a good idea if you have 1MB of memory in a mini-mainframe supporting 30 interactive users like the VAX 780 I used in the early 1980s.

{{<note>}}
The buffering problem totally blindsided me in an early SDLC deployment where the customer, in their infinite wisdom, used 9K frames on low-speed serial lines. No problem, let's increase the MTU size. Oops, now we have one buffer (or whatever the size of the HUGE buffer pool was in Cisco IOS in those days) *per router*. Not good.
{{</note>}}

After the original thick-cable Ethernet became a great hit, someone within IEEE got the wonderful idea that whatever they do afterward has to be compatible with that initial implementation. That's why we still have 1500-byte MTU and half-duplex Gigabit Ethernet messing up P2P links ;))\... and Innokentiy explained in his comment why we never got past 9K MTU.

Interested in more details like these? Check out the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar!
