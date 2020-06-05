---
title: Network Reliability Engineering Should Be More than Software or Automation
##date: 2020-06-05 17:35:00
draft: true
tags: [ automation ]
---
A while ago Juniper started aggressively promoting [Network Reliability Engineering](https://www.juniper.net/uk/en/products-services/what-is/nre/) - the networking variant of concepts of software-driven operations derived from [GIFEE](https://github.com/GIFEE/GIFEE) SRE concept (because it must [make perfect sense to mimic whatever Google is doing](https://blog.ipspace.net/2016/03/you-want-your-network-to-be-like.html), right?).

There’s nothing wrong with promoting network automation, or [infrastructure-as-code concepts](https://blog.ipspace.net/2018/09/network-infrastructure-as-code-is.html), and Matt Oswalt and his team did an awesome job with [NRE Labs](https://blog.ipspace.net/2018/09/network-infrastructure-as-code-is.html) (huge “Thank you!” to whoever is financing them), but is that really all NRE should be?
<!--more-->
Just looking at the acronym it has three words in it:

* Network (ok, we know what this is)
* Reliability (tougher one, ask network practitioners how to calculate reliability of a complex system and watch them squirm)
* Engineering (you probably know my [opinion about this one](https://blog.ipspace.net/2018/01/how-to-become-better-networking-engineer.html)).

[Reliability Engineering](https://en.wikipedia.org/wiki/Reliability_engineering) is also a well-defined concept, and one would assume that Network Reliability Engineering applies that concept to computer networks. Really?

While I totally agree we need to replace repetitive (and error-prone) manual operations with repeatable automated processes, I also believe you should not automate existing mess, but start with a reliable minimalistic network design without one-off exceptions and gazillion of configuration drifts caused by late-night throwing-spaghetti-at-walls google-and-paste troubleshooting sessions.

Unfortunately (as I [pointed out in the podcast I did with Matt a long while ago](https://blog.ipspace.net/2019/01/network-reliability-engineering-on.html)) the [NRE blog](https://networkreliability.engineering/post/) as well as Juniper whitepapers and marketing collaterals keep mum about that aspect of network reliability and focus on workflows and automation  (no surprise there, Juniper is doing a [really good job there](https://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html)).

So, what do you think? Am I too radical, or should we start with a thorough cleanup (assuming you’re dealing with a brownfield environment) and reliable designs instead of rushing head-on into automating whatever we're doing?