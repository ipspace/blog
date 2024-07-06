---
date: 2014-05-28 11:41:00+02:00
lastmod: 2021-02-15 15:00:00 
tags:
- data center
- fabric
title: How Line-rate Is Line-rate?
url: /2014/05/how-line-rate-is-line-rate.html
---
During yesterday's [*Data Center Fabrics Update*](http://www.ipspace.net/Data_Center_Fabrics_Update) presentation, one of the attendees sent me this question while I was talking about the Arista 7300 series switches:

> Is the 7300 really non-blocking at all packet sizes? With only 2 x Trident-2 per line card it can\'t support non-blocking for small packets based on Trident-2 architecture.

It was an obvious example of vendor bickering, so I ignored the question during the presentation, but it still intrigued me, so I decided to do some more research.
<!--more-->
#### What exactly is non-blocking?

I struggled to find a rigorous definition of *non-blocking architecture* that would apply to networking devices (the original definition came from circuit switching and is obviously irrelevant in our context). Weird, considering every vendor claims to have non-blocking architecture ;)

A [15 year old presentation](http://lhcb-comp.web.cern.ch/lhcb-comp/daq/postscript/switchperf_june99.pdf) was the best I could come up with (additional links are obviously most welcome -- please write a comment). It defines non-blocking as:

> A switch is non-blocking if all output-contention free switching patterns are non-blocking.

In other words, packets sent from port A to port B are never hindered by traffic sent from port C to port D.

#### Trouble in Trident land?

The comment made by the attendee could indicate that [Trident II chipset](http://www.broadcom.com/products/Switching/Carrier-and-Service-Provider/BCM56850-Series) (BCM56850 series) cannot perform linerate forwarding at low packet sizes.

{{<note info>}}Architectures with a single lookup pipeline would become blocking when the load exceeds their packet-per-second rating; the proof is left as an exercise for the reader.{{</note>}}

I couldn't find any packet forwarding performance figures on Broadcom's web site (if your GoogleFoo is better than mine, please share the link), the most technical document I found was a [marketing blabber claiming linerate performance](http://www.broadcom.com/collateral/pb/56850-PB03-R.pdf).

{{<note>}}As it's impossible to get anything out of Broadcom without signing an NDA with your blood, ~~the gentleman making the comment probably violated the NDA his employer signed with Broadcom~~. Broadcom's behavior is also an excellent breeding ground for vendor FUD. Great job, everyone! One has to love this industry.

**Update 2014-05-29**: The small packet forwarding limitations of Trident 2 architecture were publicly documented @ Cisco Live US 2014, see BRKARC-2222 session for more details; the attendee pointing them out was thus not disclosing non-public information as I incorrectly assumed.{{</note>}}

Fortunately, Arista believes in sharing their performance figures (although I doubt anyone actually measured forwarding performance of thousands of 10GE ports since [Juniper did their QFabric test](http://www.spirent.com/About-Us/News_Room/Press-Releases/2012/2012_03_07_Juniper_QFabric)) and [hardware architecture](http://go.arista.com/l/12022/2013-11-05/jt883/12022/97342/Arista_7250X_7300_Multichip_Switch_Architecture.pdf).

The specifications for their [7300 series switches](http://www.arista.com/en/products/7300-series) are pretty clear: a switch with four linecards (512 10GE ports) has 10Tbps switching capacity and can forward 7.5 billion packets per second. The minimum packet size at which they can do linerate forwarding is thus \~160 bytes (around \~150 bytes of L2 payload due to FCS and inter-frame gap).

The attendee making the comment was thus technically correct: Arista 7300-series switches cannot perform linerate forwarding of 40-byte TCP SYN packets.

#### Is this relevant?

You might have an environment in which thousands of servers have nothing better to do than saturate 10GE uplinks sending 64-byte VoIP packets or test each other's readiness by sending continuous streams of TCP SYN/RST packets.

The only environment I'm aware of that comes close to that are the test labs. If you have a real-life use case where something generates hundreds of 10GE streams full of packets with average packet size smaller than 150 bytes, I would love to hear from you.

For example, I recently spoke with someone who told me their caching servers (a typical example of an environment with small packet sizes) cannot saturate 10GE uplinks due to bottlenecks in Linux TCP stack.

{{<note update>}}Update 2021-02-15: It's perfectly possible to saturate 10GE or 40GE server uplinks in 2021, and some people got as far as using 100GE server uplinks. The question whether line-rate forwarding of small packets matters [remains a matter of opinion (and use case)](/2021/02/importance-switching-small-packets.html).{{</note>}}

#### Summary

It's nice to know the actual limitations of each platform you're considering. If you're dealing with unusual workload, make sure to check PPS as well as bandwidth figures (and anything else you might find relevant -- for example multicast forwarding performance or ARP table sizes).

Would this "discovery" stop me from recommending Arista 7300-series switches in average data center environments? Of course not.

#### Warning: rant ahead

... which brings me to the ranty part of this blog post. I understand the bitterness of a hot-shot vendor SE who just lost a big deal to a competitor, but please do yourself a favor and stop parroting the "facts" thrown at you by your competitive analysis team, particularly when those facts are totally irrelevant to real-life use cases. Such a behavior is (choose one):

A\) Childish

B\) Counterproductive

C\) Irrrelevant

D\) Irritating

E\) All-of-the-above

Also, please stop pretending you're a concerned citizen and disclose your affiliation and job position. I'm all for discussing technical details as long as we all understand individual perspectives and potential biases. On the other hand, it's pretty easy to spot a vendor rep bashing a competitor from a mile away, and you'll gain nothing by harassing everyone around you with your version of the truth.
