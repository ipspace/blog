---
date: 2020-12-01 07:16:00+00:00
distributed-systems_tag: sdn
high-availability_tag: need
series:
- distributed-systems
series_weight: 800
tags:
- design
- high availability
title: Fifty Shades of High Availability
---
A while ago we had an interesting exchange of ideas around inserting high-availability network appliance into a public cloud environment (TL&DR: it was really hard until AWS introduced Gateway Load Balancing), and someone quickly pointed out we're solving the wrong challenge because...

> Azure Firewall [...] is a fully stateful firewall-as-a-service with built-in high-availability.

Somehow he wasn't too happy when I pointed out that there's more to high availability than vendor marketing ;)
<!--more-->
**WARNING**: Before reading the rest of this blog post, [try answering](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) this simple question:

> What do I really need, and what is good enough?

Still here? Are you sure your application is so important it needs special tricks to increase its availability?

OK, let's start with the oldest marketing trick: _high availability_ means [**restarting a VM when it fails**](https://blog.ipspace.net/2011/08/high-availability-fallacies.html) (aka VMware High Availability). While it's true that the service will be eventually restored, and it's better than running a single-instance server with no safeguards, keep these minor details in mind:

* The VM is restarted when some agent discovers it's time to restart it, which is perfectly fine for handling hardware failures, but not exactly stellar when dealing with software failures or degraded performance. Your service might be gone way before that agent gets nervous.
* A restarted VM will reboot. That takes time (more so if you're still using a Windows server).
* The disks might need file system check. That takes some more time.
* If you're running a service that uses an internal database, that database needs to be recovered. Add some more waiting time.

So yeah, after a while the service will be back. In the meantime, the unhappy customers will be twiddling their thumbs.

Regardless of how unimportant my application is, I would always use this approach when available. After all, it can't hurt to have your service restarted after a failure... but please don't call a single VM instance that is rebooted when it fails a high availability solution. It's 2020, and what you're doing is nothing more than basic hygiene.

Moving forward with beloved virtualization solutions, I will not waste any time on crazy schemes involving [moving running server instances around the globe](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html). They work best in PowerPoint and [rarely in practice](https://blog.ipspace.net/2011/09/long-distance-vmotion-for-disaster.html) (unless you need an [audit tick-in-the-box](https://blog.ipspace.net/2019/09/disaster-recovery-test-faking-another.html)).

**High-availability server clusters** are just a tad better. Instead of an operating system restart, a service is restarted when the primary server or service fails. The clients won't have to wait for the OS reboot, but might still wait for service recovery.

OK, so we'll run multiple server instances, **put a load balancer in front of them, and restart failed instances as needed** (this is probably how Azure Firewall works). Much better, but still far from perfect:

* All sessions going to the failed server will be lost on server failure. Not a big deal in a typical web application (although in most cases the end-user will get a garbled page and will reload in frustration), but it might be a significant annoyance when a 10GB upload fails after 15 minutes.

{{<note info>}}Web browsers typically don't retry requests that fail, so it's up to the end-user to get annoyed and press the RELOAD button.{{</note>}}

* If your application team asks you to implement any sort of session stickiness, it's usually an indication that the application stores the client session state within individual server instances (as opposed to back-end database or key-value store). Not only will clients get garbled web pages on server failure, they will also lose session state, which might include the contents of their shopping cart. Awesome.

But wait, there's something much much better (or so they claim): **clusters sharing session state across all nodes**. It looks [picture-perfect in PowerPoint](https://blog.ipspace.net/2015/11/stretched-firewalls-across-layer-3-dci.html) -- whatever happens, someone will be able to keep going without losing anything (including client TCP sessions) -- until you realize that [tight coupling of devices that should provide failure resiliency](https://blog.ipspace.net/2016/11/reliability-of-clustered-solutions.html) probably isn't the greatest idea out there. After all, if one node goes totally bonkers, it might bring down all other nodes (just ask anyone who had to deal with switch stack challenges).

There's also the minor detail of nodes wasting increasingly more time synchronizing session state if you want to grow the cluster size to deal with increased load.

It's obviously much better if you can **implement high availability in the application code** instead of relying on generic infrastructure high availability. 

Example: When using active/standby database instances, the database clients can be made to switch from active to standby instance on failure, giving you much better results than any generic load balancing concoction:

* There is no data loss if you use 2-phase commit (but then you tightly coupled the database instances into a single failure domain);
* You might lose some data with _log shipping_ but the database instances are decoupled, which means that the primary instance keeps working even if the standby instance fails.
* Failover to standby instance is almost instantaneous as opposed to load balancer health probes. When a database client detects connection error, it automatically switches over to the backup instance.
* You could even use the standby instance for read-only database access, increasing the performance of applications that mostly read data like most e-commerce applications; in some environment 99% of the transactions are read-only queries.

Finally, keep in mind that modern application stack contain more than one service, and that a single rotten apple anywhere in the stack can bring down the performance of the whole stack (see [How Not to Measure Latency](https://blog.ipspace.net/2020/08/measuring-latency.html)). The only way to work around this problem is to have **independent copies of the application stack** (*swimlanes*) to keep the performance challenges within a single lane which can then be shut down if needed.

{{<figure src="HA_Swimlanes.png" caption="Sample swimlane design">}}

However, even within a perfectly designed system with multiple swimlanes you might get a total system failure if you're using synchronous data exchange between database instances (example: 2-phase commit). The only way to make swimlanes completely independent from one another is to have _eventual consistency_ between data stores... which means that the application code has to be able to deal with that.

### More to Explore

* [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) and [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online courses include *High-availability architectures* modules;
* [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar describes numerous high-availability solutions including swimlanes;
* I covered swimlanes and their implications for zone-aware Azure services in load balancing part of [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar;
* If you want to understand the networking impacts of VMware's high availability watch [vSphere 6 Networking Deep Dive](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive) webinar.
