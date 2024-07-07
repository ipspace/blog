---
date: 2011-08-08 07:07:00.002000+02:00
high-availability_tag: fail
series_weight: 520
tags:
- data center
- vMotion
- virtualization
- high availability
title: High Availability Fallacies
url: /2011/08/high-availability-fallacies/
---
I've already written about the [stupidities of risking the stability of two data centers to enable live migration of "mission critical" VMs between them](/2011/02/what-exactly-makes-something-mission/). Now let's take the discussion a step further -- after hearing how critical the VM the server or application team wants to migrate is, you might be tempted to ask "and how do you ensure its high availability the rest of the time?" The response will likely be along the lines of "We're using VMware High Availability" or even prouder "We're using VMware Fault Tolerance to ensure even a hardware failure can't bring it down."
<!--more-->
I have some bad news for the true believers in virtualization-supported high availability -- quite a few of them probably don't understand how it works. Let’s see what HA products can do ... and keep in mind that hardware causes just a few percents of the failures; most of them are caused by software failures or operator errors.

**VMware High Availability** (or any equivalent product) is a great solution, but the best it can do is to restart a VM after it crashes or after the hypervisor host fails. Assuming you can reliably detect a VM OS or application service (for example, database software) failure, the VM still needs to be *restarted*. VM-level high availability is thus dangerous, as it gives application developers and server administrators false hopes -- they start to believe a magical product can bring high availability to any hodgepodge of enterprise spaghetti code. In reality, the VM has to go through full power-up process and all the services the VM runs have to perform whatever recovery procedures they need to run before the VM (and its services) are fully operational.

**VMware Fault Tolerance** is an even more interesting case. It runs two parallel copies of the same VM (and [ensures they\'re continuously synchronized](http://lonesysadmin.net/2011/04/19/vmware-fault-tolerance-determinism-and-smp/)) -- a perfect solution if you're running a very lengthy procedure and don't want a hardware failure to interrupt it. Unfortunately, software failures happen more often than hardware ones \... and if the VM crashes, both copies (running in sync) will crash simultaneously. Likewise, if the application service running in the VM crashes (or hangs), it will do so in both copies of the VM.

{{<note>}}As expected, an interesting Twitter discussion followed this blog post. Among other interesting remarks, Duncan Epping (of the Yellow Bricks fame) rightfully pointed out that the VMware HA/FT products function exactly as described. That's absolutely true -- VMware's documentation is extremely precise in describing how HA and FT work. It's just that VMware marketing tends to oversell stuff.{{</note>}}

**High-availability clusters** like [Windows Server Failover Clustering](http://www.microsoft.com/windowsserver2008/en/us/failover-clustering-multisite.aspx) restart a failed service (for example, the SQL server) on the same or on another server. The restart can take from a few seconds to a few minutes (or sometimes even longer if the database has to do extensive recovery). A nine lost.

**Bridging between data centers** (the typical design recommended by VMware-focused consultants) might cause long-distance forwarding loops, or you might see the flood of traffic caused by a forwarding loop spilled over the WAN link into the other data center, killing all other inter-DC traffic (including cluster heartbeats if you’re brave enough to use [long-distance clusters](/2011/06/stretched-clusters-almost-as-good-as/), and storage replication). 

Want a data point: we experienced a forwarding loop caused by an intra-site STP failure. Recovery time: close to 30 minutes *with NMS noticing the problem immediately and operator being available on site*. Admittedly some of that time has been spent collecting evidence for post-mortem analysis.

Are you really willing to risk your whole IT infrastructure to support an application that was never designed to run on more than one instance? After all, one would hope your server admins do patch the servers ... and patches do require an occasional restart, don’t they?

**Moral of the story**: the “magic” products give you false sense of security; good application architecture and use of truly highly-available products (like MySQL database cluster) combined with load balancing technologies are the only robust solution to the high availability challenge.

### Even More Information

You'll find in-depth discussions of high-availability architectures in the [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.

Want to dive deep into the underlying infrastructure technologies? Watch [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers), [Data Center Interconnects](https://www.ipspace.net/DCI) and [VSphere 6 Networking Deep Dive](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive) webinars.

### Revision History

2023-03-03
: Rewrote a few paragraphs to make them easier to understand.
