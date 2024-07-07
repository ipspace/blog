---
date: 2009-12-03 07:03:00.013000+01:00
more_blurb: true
tags:
- data center
- SAN
title: 'iSCSI and SAN: Two Decades of Rigid Mindsets'
url: /2009/12/iscsi-and-san-two-decades-of-rigid/
more_blurb: True
---
Greg Ferro asked a very valid question in his blog: "[Why does iSCSI use TCP as the underlying transport protocol](http://etherealmind.com/why-does-iscsi-use-tcp/)"? It's possible to design storage-focused protocol that uses connectionless lower layers ([NFS](http://en.wikipedia.org/wiki/Network_File_System_(protocol)) comes to mind), but the storage industry has been too focused on their past to see past the artificial obstacles they've set up themselves.

{{<figure src="/2009/12/s1600-History of SAN.png">}}
<!--more-->
It all started in 1981 with [SCSI](http://en.wikipedia.org/wiki/SCSI): a standard way of connecting storage to hosts with [ribbon cables](http://en.wikipedia.org/wiki/SCSI). They've made the first mistake when they've decided to replace ribbon cables with fiber: instead of developing a network-oriented protocol, they replaced physical layer (cable) with another physical layer and retained whatever was running on top of the ribbon cable ([SCSI command protocol](http://en.wikipedia.org/wiki/SCSI)). If they wanted this approach to work, the new transport infrastructure had to have similar characteristics to the old one: almost no errors, no lost frames and guaranteed bandwidth. And thus Fiber Channel was born.
<!--more-->
The focus on low frame loss rate is a consequence of the design of the SCSI command protocol. SCSI was working well in an environment where errors occurred rarely enough that a long timeout and simple retransmission scheme did not hurt the performance. SCSI performance would suffer badly with an error- and loss rate of Ethernet- or IP-based networks, so the storage industry had three options:

-   Change SCSI command protocol;
-   Insert a reliable transport protocol between SCSI and unreliable lower layers;
-   Invent a square wheel (design a lossless LAN).

Fiber Channel is option\#3 and iSCSI and FCIP are following option\#2. Now, keep in mind that both iSCSI and FCIP were designed by server/storage experts, not by internetworking experts. They didn't want to go into the dirty details of reliable protocol design, so they chose whatever was readily available (TCP) and forgot to consider the performance implications (primarily the required processing power) of TCP overhead.

Those of you that are ancient enough to have encountered SNA (among other crazy things I was developing 3274-compatible cluster controllers in those days) might remember the various ways of transporting SNA-over-IP. The standard (DLSw) transported LLC2 over TCP and Cisco also offered [FST](http://www.cisco.com/en/US/tech/tk331/tk336/tech_digest09186a0080091dca.html) which did not have the TCP-related overhead. However, there's a major difference between SNA (LLC2) and SCSI: SNA was designed for lossy environments (it was first used over low-speed modem links) and had acceptable and decently fast error recovery procedures. FST's only job was to ensure that the packets did not arrive out-of-order (an out-of-order packet caused immediate session reset).
