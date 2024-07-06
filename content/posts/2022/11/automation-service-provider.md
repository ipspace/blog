---
title: "Network Automation: a Service Provider Perspective"
date: 2022-11-22 07:59:00
tags: [ automation ]
---
_[Antti Ristimäki left an interesting comment](/2022/10/network-automation-considered-harmful.html#1458) on [Network Automation Considered Harmful](/2022/10/network-automation-considered-harmful.html) blog post detailing why it's suboptimal to run manually-configured modern service provider network._

---

I really don't see how a network any larger and more complex than a small and simple enterprise or campus network can be developed and engineered in a consistent manner without full automation. At least routing intensive networks might have very complex configurations related to e.g. routing policies and it would be next to impossible to configure them manually, at least without errors and in a consistent way.
<!--more-->
With automation even the most complex configurations can be presented with a simple abstraction and should one need to implement any architectural change in the network, one can build the logics only once and let the automation multiply it into the running configs. We have a lot of examples of such, for example policy frameworks for BGP SOO filtering, BGP large community based selective route filtering, prefix segment injection with correct SIDs, RPKI ROA validation configurations etc. Without automation it would be also very difficult to enforce the desired configurations and would result in an opportunistic network where certain configurations are only applied if an engineer has remembered to, or cared to, configure them.

By the way, I think that "automation" is not actually the best word to describe this whole thing and I'd rather talk about programmatic approach to network configuration. Ironically, I think that Software Defined Networking would be a perfect term, if only SDN hadn't gain such a bad reputation during recent years when it was used exclusively for just about anything. Maybe "network configuration as a code" would describe pretty well what is usually referred to as "automation".

---

Not surprisingly, what he wrote matches what I've been explaining in [automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) and [online course](https://www.ipspace.net/Building_Network_Automation_Solutions) for years:

* Figure out what you want to do
* Define the services the network has to offer
* Create a high-level data model describing the services
* (Optional) Transform services data model into devices data model to make your device configuration templates more palatable
* Create device configuration templates that transform your high-level data model into device configurations
* Set up a workflow that deploys device configurations, either in a maintenance window or on every change
* (Optional) Refactor the high-level data model into [4NF](https://en.wikipedia.org/wiki/Fourth_normal_form)/[5NF](https://en.wikipedia.org/wiki/Fifth_normal_form) and store services data in a transactional database instead of a bunch of YAML files in a shared folder
* (Optional) Create a user interface friendlier than YAML/vi to modify the high-level data model
* (Optional) Call your high-level data model _intent_ and create a buzzword-bingo-winning white paper or a self-congratulating conference talk

You might have noticed that I haven't mentioned a popular 7-letter tool or a must-learn 6-letter programming language -- low level tools don't matter nearly as much as processes, workflows and architectures.
