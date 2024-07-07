---
date: 2011-06-10 06:27:00.004000+02:00
high-availability_tag: ignore
ha-cluster_tag: overview
series:
- ha-cluster
tags:
- data center
- high availability
title: 'Stretched Clusters: Almost as Good as Heptagonal Wheels'
url: /2011/06/stretched-clusters-almost-as-good-as/
---
Some people are changing round wheels to heptagonal format because they will roll better. Some other people are building *stretched* [*high-availability clusters*](http://en.wikipedia.org/wiki/Computer_cluster) -- clusters of servers stretched over multiple data centers. Unfortunately only one of these claims is false.

Similar to the [stretched firewalls](/2011/04/distributed-firewalls-how-badly-do-you/) design, stretched tightly coupled HA clusters are vulnerable -- you lose the inter-DC link for long enough time (depending on how the cluster heartbeat is configured, a few seconds could be enough) and you have a total disaster on your hands.
<!--more-->
**Best case -- partitioned cluster**. Most HA clustering solutions available today (including [Microsoft's WSFC](http://en.wikipedia.org/wiki/Microsoft_Cluster_Server)) handle cluster partitioning (some members get isolated from the rest) the same way: the isolated minority is shut down and the services they offered are restarted on the remaining nodes. The methods used to figure out which part constitutes the minority differ, but they all use variants of voting mechanisms and quorums (with disks or file systems thrown in sometimes to make the total number of votes odd).

Did I mention the services were *restarted*? That's a lengthy outage right there without even taking in consideration the excessive load those services place on the remaining members of the cluster (in a balanced two-DC design, a DCI link outage would probably take down approximately half of the cluster nodes).

**Worst case -- split brain**. If you manage to misconfigure the quorum algorithm (or shared storage used as a missing vote), both parts of partitioned cluster would think they are the remaining majority. Both parts would *restart all services that were running on the "lost" half*, so you'll get *two copies of each service*, each copy writing to its own local copy of the storage, completely ruining your data in the process. Recovering from a split brain event takes hours (at least), starting with a complete shutdown and data restore (you do have backups, don't you?).

**Hoping it won't happen doesn't help**. Think twice before writing "*if we lose our DCI link, the split brain will be the least of our problems*" in the comments. Do you really want to bet your whole IT infrastructure on a WAN link?

**What can I do to stop it?** Sometimes not much, because everyone else crazed by the flat-earth nirvana stories won't listen. In this case make sure you document your objections and predictions -- at least you'll have an "*I told you so*" document.

Sometimes it might help to ask the stretched cluster designers what happens if the DCI link does goes down and the cluster partitions. They just might pause and reconsider.

Best case, you're working in an organization where apps, server and networking people actually talk to each other and work together to solve the business problems (stretched clusters are not solving business problems, they are kludges around bad application architecture). That's the perfect place to start the scale-out application architecture discussion and the role load balancers (I can't make myself say [*Application Delivery Controller*](http://packetpushers.net/show-47-load-balancers-good-thing-we-step-in-it/)) play in it. If you want to learn more about that, you'll find plenty of information in my [Data Center Interconnects](https://www.ipspace.net/DCI) and [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinars.
