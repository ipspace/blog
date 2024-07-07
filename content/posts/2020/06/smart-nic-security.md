---
title: Security Aspects of Using Smart NICs
date: 2020-06-23 07:18:00
tags: [ cloud ]
---
After I published the blog post describing how infrastructure cloud provides (example: AWS) might use smart Network Interface Cards (NICs) as the sweet spot to implement overlay virtual networking, my friend Christoph Jaggi sent me links to two interesting presentations:

* [Can you still trust your network card](https://www.ssi.gouv.fr/uploads/IMG/pdf/csw-trustnetworkcard.pdf)
* [The Jedi Packet Trick Takes over the Deathstar](http://www.alchemistowl.org/arrigo/Papers/Arrigo-Triulzi-CANSEC10-Project-Maux-III.pdf)

Both presentations describe how you can take over a smart NIC with a properly crafted packet, and even bypass CPU on a firewall using smart NICs.
<!--more-->
## What Is a Smart NIC

If you've never heard about smart NICs, you might want to [start with the chat](/2019/03/smart-nics-and-related-linux-kernel/) we had with Or Gerlitz (Mellanox), Andy Gospodarek (Broadcom) and Jiri Pirko (Mellanox), and then look at the [technical part](https://vimeo.com/412089997) of the [Pensando presentation](https://techfieldday.com/appearance/pensando-presents-at-cloud-field-day-7/) from Cloud Field Day 7 (you can safely skip the "we are so awesome" part).

Or in you're short on time, here's the crux of the story:

* Dumb NICs take packets from a circular buffer (TX ring) and send bits from those packets to the wire... or the other way round (in which case the circular buffer would be called RX ring).
* Smart NICs include everything a dumb NIC has (someone obviously has to transmit and receive the bits), but they can be programmed to munge the packets, including all sorts of crazy lookups and content manipulations. Most smart NICs are programmable, and include plenty of memory and a general-purpose CPU.

{{<note info>}}I was told some high-frequency trading environments use smart(er) NICs (using FPGA if I remember correctly) to reduce the number of stock quotes in updates received from stock exchange to minimize the delay in processing the interesting quotes.{{</note>}}

## What Is the Problem?

We make mistakes. Sometimes the mistakes are burnt into hardware (see [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug)), most often they are hidden somewhere in software. History of IT security is littered with buffer overflows or code accepting inputs without any sanity check (see   [Heartbleed](https://en.wikipedia.org/wiki/Heartbleed)). 

Then there are those nasty bugs that need a very specific sequence of events and very specific timing (see: [Meltdown and Spectre](https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability))... and researchers keep discovering all sorts of variants of exploits of speculative execution). Finally, even the management software that handles software upgrades and the like is vulnerable (see: [Intel CSME vulnerability](https://thehackernews.com/2020/03/intel-csme-vulnerability.html)).

I think it's fair to say that it's only a question of time when we'll see another catastrophic smart NIC exploit. Oops, we already did - see [Broadpwn](https://www.blackhat.com/docs/us-17/thursday/us-17-Artenstein-Broadpwn-Remotely-Compromising-Android-And-iOS-Via-A-Bug-In-Broadcoms-Wifi-Chipsets.pdf).

Amazon might be in pretty good shape with AWS Nitro. A cloud service provider has to care about security more than a [typical enterprise vendor](/2020/06/sdwan-silver-peak-security/), and they [claim to have provable security](https://www.slideshare.net/AmazonWebServices/an-aws-approach-to-higher-standards-of-assurance-with-provable-security-fnd214-aws-reinforce-2019). As for smart NICs being used in enterprise servers, in particular those that can be programmed by the end-user, I have only one thing to say: expect some fun times.