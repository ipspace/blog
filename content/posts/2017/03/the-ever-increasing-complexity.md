---
date: 2017-03-07 09:39:00+01:00
tags:
- data center
- SD-WAN
title: The Ever-Increasing Complexity
url: /2017/03/the-ever-increasing-complexity.html
sd-wan_tag: rant
---
Eyvonne Sharp wrote a [great blog post describing Cisco's love of complexity](http://www.esharp.net/ciscos-identity-crisis-complexity-pride-and-sd-wan/) and how SD-WAN vendors proved things don't have to be that complex.

I know Cisco (and every other vendor) loves making [ever-more-complex solutions](/2013/09/sooner-or-later-someone-will-pay-for.html) that [lock you into their morass](/2015/01/lock-in-is-inevitable-get-used-to-it.html) for the rest of your life ([long-distance vMotion](/2015/02/before-talking-about-vmotion-across.html) anyone?).
<!--more-->
I'm also positive a lot of the complexity we're facing is the result of customer requests. You know, those people that never bothered to understand how technology really works (because vendors promised them it's easy), designed their network based on whitepapers (written by those same vendors), faced scaling challenges, and started yelling at the vendor to implement a [dozen nerd knobs](/2017/03/nerd-knobs-save-day-nssa-saga-continues.html) (while sometimes breaking the standards) to make their network work ([stretched clusters](/2011/06/stretched-clusters-almost-as-good-as.html) anyone?). It's amazing what a large PO can bring you ;)

{{<note>}}The latest installment in that soap opera: [OSPF Topology-Transparent Zone (RFC 8099)](https://tools.ietf.org/html/rfc8099) because it\'s easier to add another layer of indirection than fixing a broken network design. OTOH, fixing a broken design rarely sells more boxes and software upgrades.{{</note>}}

Another source of complexity: clueless CYA customers that have no idea what they need because they never invested into a proper network design. When such customers create an RFP it often requires every technology ever published as an Internet draft "because we might need it in the future". I've personally seen RFPs that were a laundry list of acronyms compiled from 3+ different vendor specs. Needless to say, nobody fulfilled all the requirements

{{<note>}}HT to \@Anonymous for reminding me of this one-- I've been away from system integration business for too long.{{</note>}}

Of course it's not just the customers. Have you ever heard the "doing more with less" and "leveraging the existing investment" mantras (aka LISP-in-Campus)?

The real difference between Cisco and SD-WAN vendors is the length of their history. Cisco has been evolving their software for 30+ years (and has to support most of the \*\*\*\* they were forced to implement to get a particular PO indefinitely) while SD-WAN solutions started with a clean slate. Let's see how complex SD-WAN solutions will get after being faced with incompatible impossible-to-turn-down opportunities for a decade or two.

It's also easier to start from scratch and implement a clean bare-bones solution (quite often after learning the hard lessons while working for an "overly complex" \$vendor) than trying to retrofit a new idea into the old framework (I still remember IBM mainframes having virtual [punched cards](https://en.wikipedia.org/wiki/Punched_card) and 132-column [line printer](https://en.wikipedia.org/wiki/Line_printer) printouts deep in the bowels of their operating systems).

Is it fair to make fun of the complexity-ridden legacy vendors? Well, it definitely makes for fun reading, but maybe we should just respect old age while at the same time telling the dinosaurs it's time to change by voting with our wallet.

### Can You Get away from the Complexity?

You do know you don't have to use all the complexity the vendors are throwing at you, right? It's possible to design simple and robust large-scale networks if you understand how technology works, and select the best tools for each job at hand.

I [ranted about the never-ending complexity](https://my.ipspace.net/bin/list?id=NetBiz#LL) in the [Business Aspects of Networking Technologies](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies) webinar, and we large-scale data center network designs in the [Building Next-Generation Data Center course](http://www.ipspace.net/Building_Next-Generation_Data_Center).