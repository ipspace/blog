---
date: 2013-11-04 07:43:00+01:00
ha-cloud_tag: intro
high-availability_tag: cloud
series:
- ha-cloud
tags:
- firewall
- cloud
- load balancing
- high availability
title: Are Your Applications Cloud-Friendly?
url: /2013/11/are-your-applications-cloud-friendly/
---
A while ago I had a discussion with someone who wanted to be able to move whole application stacks between different private cloud solutions (VMware, Hyper-V, OpenStack, Cloud Stack) and a variety of public clouds.

Not surprisingly, there are plenty of startups working on the problem -- if you're interested in what they're doing, I'd strongly recommend you add [CloudCast.net](http://www.thecloudcast.net/) to your list of favorite podcasts -- but the only correct way to solve the problem is to design the applications in a cloud-friendly way.
<!--more-->
Here's a short list of network-related requirements an application designer/developer should consider to ensure the application stack is easy to migrate between different environments (short summary: don't depend on any particular environment- or network behavior).

If you have a similar list for compute/storage components, or if you feel I've missed a requirement or two, please write a comment.

{{<note>}}Keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, and others (when capitalized) are used in accordance with guidelines provided in RFC 2119 and RFC 6919.{{</note>}}

### Client-to-Application Interface

-   An application's external entry point MUST be defined by a static IP address and a static TCP/UDP port number(s).
-   Applications MUST support IPv4 and IPv6 client access. IPv4 client access MAY be implemented with help of stateless NAT46.
-   Application clients MUST identify an application solely by its DNS Fully-Qualified Domain Name (FQDN) and well-known port number or DNS SRV record.
-   Applications spanning multiple data centers for load balancing reasons MUST rely on DNS-based load balancing or other equivalent global load balancing mechanisms.
-   Applications deployed in multiple data centers for redundancy reasons MUST use DNS for failover purposes.
-   Application clients MUST NOT use dynamic TCP/UDP ports to access the application.

### Addressing Within the Application Stack

-   Applications SHALL NOT rely on fixed addresses being assigned to individual virtual machines or server instances within the application stack.
-   Clients within the application stack (example: database client running on a web server) SHALL use DNS services or equivalent solution (example: Zookeeper) to find the current IP address of the desired server.

### High Availability Requirements

-   HA applications SHOULD use scale-out architecture.
-   Applications MUST NOT rely on underlying cloud/hypervisor services to meet high-availability requirements. Failure resilience MUST be built into the application.
-   HA applications SHOULD use multi-instance databases, running either as a scale-out cluster or as a primary database with one or more backup instances.

### Load Balancing for Scale-Out Applications

-   Scale-out applications SHOULD use application-level load balancing mechanisms if at all possible.
-   External load balancing functionality (client-to-application load balancing) MAY use cloud-provided load balancing services.
-   Internal load balancing between application components MUST use application-level solutions or virtual appliances that can be migrated with the rest of the application stack.
-   Applications SHOULD NOT store session state on individual servers, but in a shared cache, key-value store or database.

### Firewalling and Security

-   Security design of an application MUST NOT change when the application stack moves between different cloud solutions.
-   Distributed VM NIC firewalls SHOULD be used wherever possible.
-   Traditional (inter-subnet) firewalls MAY be used between security zones in the application stack.
-   Inter-subnet firewalls MUST be implemented with virtual appliances to make them easy to migrate.

### How realistic are these requirements?

It's obviously impossible to fix an existing application to adhere to all the above requirements, but do try to use them when starting new projects. Also, share them with your application developers -- the more they adhere to them, the easier everyone's life will be in the long term (it's really not THAT hard to use a DNS name instead of an IP address in a high-level language like Java, ASP.NET, P\*, R\*...).

### Anything else?

I'm positive I missed a few things (I always do, and getting your comments telling me what I overlooked is the best part of my blogging experience) -- please list them in your comments.

Also, you OUGHT TO want to watch the [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) and you REALLY SHOULD read the excellent [Scalability Rules](https://www.amazon.com/Scalability-Rules-Principles-Scaling-Sites/dp/0321753887) book.
