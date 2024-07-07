---
date: 2011-06-21 10:24:00.001000+02:00
tags:
- QoS
- WAN
title: Some More QoS Basics
url: /2011/06/some-more-qos-basics/
---
I got a really interesting question from one of my readers (slightly paraphrased):

> Is this a correct statement: QoS on a WAN router will always be on if there are packets on the wire as the line is either 100% utilized or otherwise nothing is being transmitted. Comments like "QoS will kick in when there is congestion, but there is always congestion if the link is 100% utilized on a per moment basis" are confusing.

Well, QoS is more than just queuing. First you have to *classify* the packets; then you can perform any combination of *marking, policing, shaping, queuing* and *dropping*.
<!--more-->
There's no way around *classifying* the packets into different groups if you want to perform any reasonable QoS on them. If they're all the same, just throw them into a FIFO queue and focus on other issues your network might have. Classification rules could be hard-coded (some switches can classify frames only based on 802.1p traffic classes) or you could have a rich set of configurable rules like those supported on software-based IOS platforms.

{{<note>}}Of course there are exceptions to every black-and-white rule. You might need to apply a single marking value (DSCP, EXP bits or 802.1p priority) to all the packets, or you might want to police or shape all traffic going over the WAN link.{{</note>}}

*Marking* and *policing* are always active. If you apply marking on a traffic class, the marking bits are always modified. Likewise, the traffic in a policed class is always measured and different actions can be applied to conformant, excessive or violating traffic (assuming you have dual token bucket algorithm). You can find lots of details in my [QoS policing](/kb/tag/QoS/QoS_Policing/) article.

*Shaping* combines three activities: metering the traffic (identical to policing), queuing the excess traffic and releasing the queued traffic based on token bucket algorithm. The queuing part of shaping obviously happens only if the amount of traffic exceeds the configured capacity as measured by the token bucket algorithm, which allows some short-term bursts.

You might want to read my [traffic shaping](/kb/tag/QoS/Traffic_Shaping/) article for more details. Also note that the [Hierarchical Queuing Framework](/2009/11/first-hqf-impressions-excellent-job/) dramatically improved the Cisco IOS shaping behavior -- packets are now released from the shaping queues at regular intervals, not in bucket-size bursts as before.

*Dropping* could happen as part of policing (see above) or as part of congestion-avoidance mechanisms like Weighted Random Early Drop (WRED). WRED starts dropping random packets (in small quantities) only when the output queue gets long enough. The default dropping threshold depends on interface type and bandwidth; usually the interface has to experience significant bursts or sustained congestion for WRED to kick in.

{{<note>}}WRED is usually applied to individual FIFO queues, not to the whole queuing system.{{</note>}}

Finally, there's *queuing*. One would expect queuing to kick in as soon as there are at least three packets in an interface's output queue (one being transmitted, two waiting for transmission). That might actually be the case if the platform uses hardware-based queuing. After all, if the classification, queuing and dequeuing is done in hardware, it costs you nothing if you do it all the time.

Software-based platforms are usually different. They use hardware FIFO queue and resort to fancier software queuing mechanisms only when the FIFO queue grows beyond a configured length (**tx-ring-limit** on most routers running Cisco IOS). Yet again, you'll find in-depth details in my [Queuing Principles ](/kb/tag/QoS/Queuing_Principles/) article. I also got a few interesting test results when [measuring jitter and delay with various **tx-ring-limit** values](/kb/tag/QoS/TX-Ring-Limit/).

Last piece of the QoS puzzle: *link efficiency mechanisms*. I don't think I have to write too much about *compression*. It's still supported on serial interfaces (HDLC or PPP) and can use several different algorithms. You can also install hardware compression modules in some older routers to enable compression over higher-speed links. *TCP header compression* is a special case -- TCP header (40 bytes) can be minimized to \~5 bytes due to very high level of header data redundancy on a slow-speed WAN link with only a few TCP sessions. The TCP header compression works only with TCP, leaves the payload intact (so it works best for interactive sessions like Telnet or SSH) and becomes useless as the number of TCP sessions increases.

*Link Fragmentation and Interleaving (LFI)* is a more interesting beast. The transmission delay of maximum-MTU (1500 bytes by default) packets on low-speed links can increase the latency and jitter beyond the VoIP usability thresholds. To cope with that, the LFI mechanisms (*Frame Relay Fragmentation* and *Multilink PPP Fragmentation and Interleaving*) use ATM-like approach: packets are sliced into reasonably sized fragments and the small high-priority packets (for example, VoIP packets) bypass the regular output queue and get inserted between fragments of larger packets. The queuing latency of a VoIP packet is thus determined by the maximum fragment size, not maximum MTU size.
