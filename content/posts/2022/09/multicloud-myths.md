---
date: 2022-09-15 07:44:00+00:00
ha-cloud_tag: stretch
series_weight: 700
series:
- ha-cloud
tags:
- cloud
title: 'Multi-Cloud: Myths and Reality'
---
I keep hearing numerous variations of the following argument from people believing in the unlimited powers of [multi-cloud](https://en.wikipedia.org/wiki/Multicloud)[^WBS] (deploying your workloads in multiple public cloud providers):

> We don't install all our servers in the same DC. But would you trust one Cloud Server Provider with all your applications? That's why you should use multi-cloud.

I've been hearing similar arguments for at least 30 years, including:
<!--more-->
[^WBS]: Wikipedia link included to illustrate how some of its articles could be full of bovine byproducts.

* Would you trust a single firewall vendor? You should have two firewalls from different vendors in sequence in case one of them has a critical bug.
* Would you trust a data center switching vendor? You could reduce the costs by buying switches from multiple vendors.

Guess what: while there might be a few instances where the above arguments were valid, they usually resulted in an expensive, bloated blob of complexity.

While you shouldn't place infinite trust in the Cloud Service Providers, deploying an application workload across multiple cloud service providers makes as much sense as:

* Building one data center with Cisco gear and another data center with Arista gear (yet again, I know people doing that)
* Running Ubuntu servers in one data center and RedHat servers in another data center *for the same application*
* Using Oracle database in one data center and PostgreSQL database in another data center *for the same application*

In a word: No. If you care about resiliency and availability, deploy parallel application stacks across multiple availability zones or regions *of the same cloud provider*.

{{<note info>}}Trying to do that if your application stack relies on a single database instance or a distributed database using a 2-phase commit is a waste of time. The proof is left as an exercise for the reader; you might find some hints in the _[Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)_ webinar.{{</note>}}

Does that mean that the multi-cloud makes no sense? Sadly, no. Going back to the more traditional examples:

* Are there organizations that would run Cisco gear in one location and Arista gear in another one? Sure. Mergers and acquisitions usually result in a hodgepodge of hard-to-manage equipment.
* Are there environments that have applications written in a half-dozen programming languages? Of course. Giving development teams too much freedom will always result in a bazaar[^RPE]
* Is anyone using multiple transactional databases (Oracle, SQL Server, PostgreSQL) simultaneously? I'm sure the answer is YES. Sometimes it might be due to mergers, too much freedom, or simply because a third-party product requires a specific database.

It's the same with multi-cloud:

* You'll often end up using multiple public cloud providers after a merger or acquisition.
* Some applications (for example, Office 365) are tied to a specific public cloud.
* Runaway development teams with a spare credit card can generate as much technical debt as you allow them to.

Is it worth considering a product that can connect these disparate islands? Sure, but please don't try to tell me you're going to deploy applications in multiple public clouds to _increase availability_[^MCV].

Looking for even more grumpiness? Listen to the Day Two Cloud *[The State of Multi-Cloud Networking](https://packetpushers.net/podcast/day-two-cloud-070-the-state-of-multi-cloud-networking)* and *[Cloud Economics Are Ridiculous](https://daytwocloud.io/podcast/day-two-cloud-078-cloud-economics-are-ridiculous/)* podcasts or follow [Corey Quinn](https://twitter.com/QuinnyPig).

Interested in real-life solutions? I covered multi-region connectivity in [AWS](https://www.ipspace.net/Amazon_Web_Services_Networking) and [Azure](https://www.ipspace.net/Microsoft_Azure_Networking) webinars, and hinted at potential multi-cloud solutions in _[Networking in Private and Public Clouds](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds)_ webinar.

[^RPE]: ... even without the resume-padding activities

[^MCV]: ... regardless of how much the vendors selling multi-cloud networking would love you to do just that.
