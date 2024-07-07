---
title: Network Reliability Engineering Should Be More than Software or Automation
date: 2020-06-15 06:35:00
tags: [ automation ]
series: [ niac ]
niac_tag: rant
---
*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. [Subscribe here](http://www.ipspace.net/Subscribe/Five_SDN_Tips).*

In late 2018 Juniper started aggressively promoting [Network Reliability Engineering](https://www.juniper.net/uk/en/products-services/what-is/nre/) - the networking variant of concepts of software-driven operations derived from [GIFEE](https://github.com/GIFEE/GIFEE) SRE concept (because it must [make perfect sense to mimic whatever Google is doing](/2016/03/you-want-your-network-to-be-like/), right?).

There’s nothing wrong with promoting network automation, or [infrastructure-as-code concepts](/2018/09/network-infrastructure-as-code-is/), and Matt Oswalt and his team did an awesome job with [NRE Labs](https://nrelabs.io/) (now defunct, huge “Thank you!” to whoever was financing them), but is that really all NRE should be?
<!--more-->
Just looking at the acronym it has three words in it:

* Network (ok, we know what this is)
* Reliability (tougher one, ask network practitioners how to calculate reliability of a complex system and watch them squirm)
* Engineering (you probably know my [opinion about this one](/2018/01/how-to-become-better-networking-engineer/)).

[Reliability Engineering](https://en.wikipedia.org/wiki/Reliability_engineering) is also a well-defined concept, and one would assume that Network Reliability Engineering applies that concept to computer networks. Really?

While I totally agree we need to replace repetitive (and error-prone) manual operations with repeatable automated processes, I also believe you should not automate existing mess, but start with a reliable minimalistic network design without one-off exceptions and gazillion of configuration drifts caused by late-night throwing-spaghetti-at-walls google-and-paste troubleshooting sessions.

Unfortunately (as I [pointed out in the podcast I did with Matt a long while ago](/2019/01/network-reliability-engineering-on/)) the [NRE blog](https://networkreliability.engineering/post/) as well as Juniper whitepapers and marketing collaterals keep mum about that aspect of network reliability and focus on workflows and automation  (no surprise there, Juniper is doing a [really good job there](/2016/10/network-automation-rfp-requirements/)).

So, what do you think? Am I too radical, or should we start with a thorough cleanup (assuming you’re dealing with a brownfield environment) and reliable designs instead of rushing head-on into automating whatever we're doing?

It seems [Russ White might be thinking along the same lines](https://blog.apnic.net/2019/10/02/opinion-autonomic-automated-and-reality/) ([here's another article he wrote](https://rule11.tech/is-it-planning-or-just-plain-engineering/))...
but maybe we're just a bunch of grumpy oldtimers.

Finally, have to mention that we cover what might be a more reasoned approach in the [*getting started*](https://my.ipspace.net/bin/list?id=NetAutSol&module=1) module of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course ;)