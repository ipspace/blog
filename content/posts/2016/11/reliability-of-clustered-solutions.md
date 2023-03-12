---
date: 2016-11-14 08:56:00+01:00
high-availability_tag: ignore
ha-cluster_tag: overview
series:
- ha-cluster
tags:
- design
- security
- data center
- high availability
title: 'Reliability of Clustered Solutions: Another Data Point'
url: /2016/11/reliability-of-clustered-solutions.html
---
A while ago [I wrote](https://blog.ipspace.net/2016/10/do-i-need-redundant-firewalls.html):

> I haven't seen any hard data, but intuition suggests that apart from hardware failures a standalone firewall might be more stable than a state-sharing firewall cluster.

Guillaume Sachot (working for a web hosting company) sent me his first-hand experience on this topic:
<!--more-->
> I don\'t have statistics to prove it, but as a hoster, I can confirm that I\'ve seen high availability appliances fail more often than non-clustered ones. And it\'s not limited to firewalls that crash together due to a bug in session sharing, I have noticed it for almost anything that does HA: DRBD instances, Pacemaker, shared filesystems\...
>
> It fails, fails and fails. There are bugs, but also configuration issues/bad sync, network flapping that breaks replication and puts all instances in standby/secondary mode\...
>
> Same for VMWare clusters that cannot handle partial storage loss or performance issues without losing it completely, disconnecting from vCenter because their daemon indefinitely blocks on refreshing storage status.
>
> In the end, a non-redundant VM on a non-clustered host seems to be the service that lasts the longest.
>
> The good compromise for most people that do not require very low recovery time seems to be non-redundant VM(s) running on a cluster to cover host failure (hardware or software), and maybe \"passive\" VM(s) on another cluster that is triggered manually.
>
> And if customers need very high availability, they should/must design their app to take it into account and host it on multiple locations/independent providers.

Not that many people would want to listen to anything along these lines. Believing in Santa Claus and magical [High Availability solutions](https://blog.ipspace.net/2011/08/high-availability-fallacies.html) is more comforting.
