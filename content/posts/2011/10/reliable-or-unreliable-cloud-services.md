---
date: 2011-10-03 07:47:00.002000+02:00
high-availability_tag: cloud
tags:
- cloud
- high availability
title: Reliable or Unreliable Cloud Services?
url: /2011/10/reliable-or-unreliable-cloud-services.html
---
The question of high-availability cloud services (let's agree *reliable* in this context really means *highly available*) pops up every time I discuss cloud networking requirements with enterprise-focused experts. While it's obvious the software- and platform services must be highly available (as their users have few mechanisms to increase their availability), Infrastructure-as-a-Service (IaaS) remains a grey area.

However, once you look at the question from the business perspective, it seems Amazon probably made a pretty good choice: offer reasonably-available service at a low price. Here's what I wrote on this topic for a web site that disappeared in the haze of URL restructuring in the meantime.
<!--more-->
---
Following the [well-publicized Amazon EC2 failure](https://www.theregister.com/2011/04/21/amazon_web_services_outages_spans_zones/)[^ECF], Massimo Re Ferre (VMware’s vCloud architect at that time) wrote an interesting post arguing that [infrastructure cloud providers should offer reliable (TCP-like) services rather than UDP-like services](https://it20.info/2011/04/tcp-clouds-udp-clouds-design-for-fail-and-aws/).

[^ECF]: The whole thing happened in 2011. Amazon EC2 failures are nothing new or unusual ;)

In his opinion, the cloud infrastructure should have high-availability and disaster recovery mechanisms similar to the current VMware offerings. I agree that some application and platform cloud services must be highly available, but trying to meet very high availability requirements (4-5 nines) with the infrastructure cloud offerings will just make them more complex and thus more expensive.

{{<note>}}Avoiding the pitfalls of trying to define what *reliable* means for infrastructure cloud services, we’ll focus on high-availability requirements; when people talk about *reliable* infrastructure, they usually think about *highly available* infrastructure.{{</note>}}

Looking at the bigger picture, some cloud services do have to be highly available; let’s look at various categories of cloud services going from application toward infrastructure services:

* **Application services** (Software as a Service or SaaS) must obviously be at least as reliable as their more traditional counterparts. SaaS users can’t add an additional layer that would allow them to increase their reliability. For example: if you use Google Mail and it happens to be down, there’s nothing you can do to get access to your e-mail. Database services are similar. After all, if you're working primarily on the the network layer, databases look just like specialized applications.
* **Platform services** (Platform as a Service or PaaS) like Google AppEngine or AWS Lambda also have to offer some inherent resilience and high availability[^AZ]. If you deploy your web-based application as a bunch of modules on a cloud platform, you can’t control where those modules will be executed, how the platform will handle the increased load (apart from tweaking a few parameters from the control panel), or how it will handle global load distribution.
* **Infrastructure services** (Infrastructure as a Service) are quite different. Making them highly available would solve some problems for people who don’t know how to design and deploy properly scaled-out application architecture[^UP], but that wouldn’t greatly increase application availability. After all, software crashes or configuration errors are far more common than infrastructure failures like the one Amazon experienced[^AFC]; the servers running as virtual machines in IaaS cloud services also need to be patched or upgraded. Investing in high availability on the VM level (ensuring the VM is always up and running) with mechanisms like VMware’s Fault Tolerance would thus lead only to marginal improvement in application uptime.

[^AZ]: Skipping for the moment the availability zone/region considerations.

[^UP]: They should really use PaaS or SaaS services because at least some of those services address some high-availability requirements

[^AFC]: Clearly, an IaaS provider experiencing frequent or prolonged outages won’t stay in the business long enough to matter.

Furthermore, using scaled-out application architecture where every tier (web servers, application servers, database servers) runs on multiple parallel server instances, it’s easier to achieve geographically distributed processing and adaptive load balancing. If you want to deploy a robust application in an IaaS environment, the use of comprehensive load balancing mechanisms is a must. Incidentally, those same mechanisms make your *application* highly available even when the underlying *servers* (or infrastructure) fail, more so if you balance the load between different data centers.

I am sure that every engineer designing a cloud solution would love to build a highly available IaaS infrastructure, where every single component would be redundant and the failover mechanisms would ensure five nines or better availability, but the cost and complexity realities usually stop us from doing that. A highly available infrastructure would definitely not be cost-competitive compared to just-good-enough cloud platforms, and we all know that IaaS buyers look primarily at the costs.

From the service provider perspective, reliable IaaS service is a lose-lose proposition. If customers are experienced enough to understand the realities of unreliable infrastructure (and application designs they can use to deploy highly reliable applications), they won’t pay extra for reliability they don’t need. If they’re new to the cloud world and assume that cloud services can never fail (or their applications aren’t mission-critical), they won’t pay the premium price because they won’t understand the need for extra infrastructure complexity and the resulting higher costs.

The optimum IaaS route is probably the one Amazon took: Build a cost-optimized (but still highly reliable) infrastructure, offer the services necessary to build reliable scaled-out applications, like elastic load balancing, and try to [educate customers](https://docs.aws.amazon.com/whitepapers/latest/web-application-hosting-best-practices/an-aws-cloud-architecture-for-web-hosting.html) about how to use those services to increase the reliability of their applications.
