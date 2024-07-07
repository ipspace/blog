---
date: 2013-06-17 07:28:00+02:00
tags:
- SDN
- data center
- overlay networks
- virtualization
title: Network Virtualization and Spaghetti Wall
url: /2013/06/network-virtualization-and-spaghetti/
---
I was reading [What Network Virtualization Isn't](https://web.archive.org/web/20160319201758/http://www.definethecloud.net/what-network-virtualization-isnt/)[^IA] from Jon Onisick the other day and started experiencing all sorts of unpleasant flashbacks caused by my overly long exposure to networking industry missteps and dead ends touted as the best possible solutions or architectures in the days of their glory:
<!--more-->
[^IA]: The original web site is gone, but I managed to find a saved copy on Internet Archive

-   X.25 gurus telling me how Telnet will never take off because TCP/IP header has much larger overhead than [X.29 PAD service](http://en.wikipedia.org/wiki/Packet_Assembler/Disassembler). X.25 is dead (OK, [maybe a zombie](/2022/04/x25-still-alive/)) and nobody complains about TCP/IP header overhead anymore. BTW, we solved the header overhead problem decades ago with TCP/IP header compression.
-   ATM gurus telling me how each application needs its own dedicated QoS settings and how the only way to implement that is to run ATM to the desktop. ATM to the desktop never took off, and [global QoS remains a providers' dream and vendors' bonanza](https://www.potaroo.net/ispcol/2012-06/noqos.html). In the meantime, we've watching Netflix videos and talk over Skype ... with absolutely no QoS guarantees from our ISPs.
-   IBM sales engineers telling my customers how it would be totally irresponsible to transport bank teller application data over a TCP/IP network (the data would still be in an SNA session, but transported across unreliable routed network). SNA is another zombie, and everyone is using TCP/IP protocol stack \... oh, and we're running e-banking over the Internet.
-   Alcatel guy telling us how it's absolutely impossible to run VoIP because you can never get the voice quality (and [MOS](http://en.wikipedia.org/wiki/Mean_opinion_score)) the customers are used to. Most of our customers run VoIP today because it's cheaper than ISDN, and Skype is more than good enough for most uses. Also, do I have to mention how the voice zealots dropped their standards when faced with realities of mobile calls? I usually get better voice quality with Skype than with my mobile phone.
-   An enterprise network designer who chose ATM LANE over Fast Ethernet (in the days when FE was still bleeding edge technology) \... and failed miserably \... because he believed ATM evangelists and wanted to transport data, voice and video over a common ATM campus backbone. In the end, they did use ATM on long-distance WAN links (where it made perfect sense) and Fast Ethernet in the campus.

All the above-mentioned technologies and architectures went extinct for a simple reason: whenever there's a clash between competing solutions, the ones that move the [complexity as far out to the edge](/2011/05/complexity-belongs-to-network-edge/) as possible usually win, and those that [tried to keep the complexity and micro-state in the core](/2012/05/virtual-networks-skype-analogy/) failed (X.25, ATM, traditional voice circuits) because keeping state is too expensive at scale. Draw your own conclusions, and remember that in a server virtualization environment [the edge is in the hypervisor](/2011/12/decouple-virtual-networking-from/), not in the ToR switch.

Does that mean the overlay virtual networks are a perfect solution? Far from it -- we're probably where TCP/IP and Internet were in the early nineties, and virtualization vendors [don't have a perfect track record when it comes to network virtualization](/2011/12/vmware-vswitch-baseline-of-simplicity/), but they're catching up fast.

In the meantime, I'm positive that numerous network-focused startups and traditional vendors trying to solve the network virtualization challenges in ToR switches or in the network core will launch great products trying to capture the legacy enterprise market (because the cloud providers already moved on). Some of those products will be well executed and highly profitable, but in the end all of them will go down the same path as X.25, ATM and LANE went a decade ago, because they're architecturally suboptimal.

Finally, if you're wondering why I mentioned the spaghetti wall in the title -- [that's how I feel](http://archive.psg.com/051000.sigcomm-ivtf.pdf) when being faced with a barrage of competing (and incompatible) ToR-based network virtualization solutions.

### Revision History

2022-06-20
: Fixed broken links

