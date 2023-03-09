---
date: 2016-05-05 09:28:00+02:00
dr_tag: intro
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- high availability
title: Unexpected Recovery Might Kill Your Data Center
url: /2016/05/unexpected-recovery-might-kill-your.html
---
Here's an interesting story I got from one of my friends:

-   A large organization used a disaster recovery strategy based on [stretched IP subnets](http://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) and restarting workloads with unchanged IP addresses in a secondary data center;
-   Once they experienced a WAN connectivity failure in the primary data center and their disaster recovery plan kicked in.

However, while they were busy restarting the workloads in the secondary data center, and managed to get most of them up and running, the DCI link unexpectedly came back to life.
<!--more-->
That wouldn't be a problem if they would have re-addressed the servers, or at least done proper shutdown in the primary data center, but they were so busy recovering from the failure that they forgot to turn off the servers and storage in the primary data center.

**End result**: tons of duplicate IP addresses, cluster failures and data corruption (because the data on replicated disks diverged in the meantime).

**Moral of the story**: disaster recovery starts with a proper shutdown of the failed data center. The extra half an hour you need to do that is much better than being offline for days while restoring data from tape backups... and if your Recovery Time Objective (RTO) is less than a few hours you probably need an application-level active/active solution anyway.

Or as my friend Boštjan Šuštar wrote in a recent email:

> Disaster Recovery Procedure: Don't panic and always carry a towel.

Don't think such a disaster could ever happen in real life? Then you definitely don't need my [Building Next-Generation Data Center online course](http://www.ipspace.net/Building_Next-Generation_Data_Center).
