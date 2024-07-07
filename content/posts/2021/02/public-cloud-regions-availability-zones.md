---
date: 2021-02-16 07:14:00+00:00
ha-cloud_tag: design
high-availability_tag: cloud
series:
- cloud-subnets
- ha-cloud
tags:
- cloud
- high availability
title: Availability Zones and Regions in AWS, Azure and GCP
---
My friend Daniel Dib sent me this interesting question:

> As I understand it, subnets in Azure span availability zones. Do you see any drawback to this? Does subnet matter if your VMs are in different AZs?

I'm positive I don't have to tell you what networks, subnets, and VRFs are, but you might not have worked with public cloud availability zones before. Before going into the details of Daniel's question (and it will take us three blog posts to get to the end), let's introduce *regions* and *availability zones*  (you'll find more details in [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) and [Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinars).
<!--more-->
### Regions and Availability Zones

All three big public cloud providers use *regions* and *availability zones*. Definitions vary a bit, but they're fundamentally the same thing:

* *Region* is a location around which they cluster multiple data centers. Latency and bandwidth within a region are usually guaranteed.
* Each region has multiple *availability zones*. AWS guarantees that the availability zones within a region are geographically separate (different data centers), while Azure has some regions that have a single availability zone.
* All cloud providers claim that the availability zones are independent failure domains -- a problem within one availability zone should not impact other availability zones.

While the last statement is mostly true, you still need connectivity between availability zones which means that there's still some coupling between them, and the potential for undesired spillover effects (similar to [inter-AS BGP quirks](/2015/04/on-sdn-controllers-interconnectedness/)). All three providers also use a single orchestration system per region, and at least AWS already found out the hard way it's a bad idea to run the orchestration system in a single region. Their experiment made headlines, while it seems like nobody bothers when Azure orchestration system decides to *eventually* deliver services.

Regions should be completely independent from one another, but at least Azure uses a single orchestration system API endpoint across all regions. When an AWS region has problems you can still connect to other regions (because they are managed through different API endpoints -- FQDN/IP address), while you're pretty much stuck if your local Azure orchestration system endpoint decides it's time for a lunch break. Obviously I might be totally off track in which case I'd appreciate a quick correction in the comments.

### Impact of Regions and Availability Zones on Application Architecture

AWS, Azure, and GCP solemnly promise that they build their services in a way that makes availability zones independent failure domains. We don't know how true that is, but it's not a bad start.

You should therefore deploy instances of an application with high availability requirements in multiple availability zones, ideally in independent [swimlanes](https://akfpartners.com/growth-blog/fault-isolation-swim-lane) (more about that in a later blog post), but if you really care about availability you SHOULD use multiple regions. All public cloud providers offer local load balancing (TCP/UDP load balancing and HTTP proxy), DNS-based global load balancing, and at least AWS offers anycast load balancing. Azure cross-region load balancer is in preview as of February 2021, and I you know [I won't waste too much time reading GCP documentation](/2020/08/selecting-public-cloud/) (because the service I'm interested in might be [deprecated tomorrow](https://medium.com/@steve.yegge/dear-google-cloud-your-deprecation-policy-is-killing-you-ee7525dc05dc)).

And yes, I'm totally aware we didn't get anywhere close to what Daniel was asking, but you have to start somewhere, and we ran out of time for today... See you next week ;)

### More to Explore

You're probably used to the list of webinars where you can find 10x more information than in the blog posts:

* [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking)
* [Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking)
* [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)
