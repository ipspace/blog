---
date: 2021-06-15 08:22:00+00:00
lastmod: 2021-07-12 17:46:00
ospf_tag: details
tags:
- OSPF
title: OSPF Inter-Process Route Selection
---
The traditional wisdom claimed that a Cisco IOS router cannot compare routes between different OSPF routing processes. The only parameter to consider when comparing routes coming from different routing processes is the admin distance, and unless you change the default admin distance for one of the processes, the results will be random.

Following [Vladislav's comment to a decade-old blog post](https://blog.ipspace.net/2008/01/e1-and-e2-routes-in-ospf.html#639), I decided to do a quick test, and found out that code changes tend to invalidate traditional wisdom. OSPF inter-process route selection is no exception. That's why it's so stupid to rely on undefined behavior in your network design, memorize such trivia, test the memorization capabilities in certification labs, or read decades-old blog posts describing arcane behavior.
<!--more-->

Before we move on:

* In case you haven't got the message: **do not** use anything described in this blog post outside of a CCIE lab. Good network designs do not depend on under-documented features.
* The only reason I wrote this blog post was to document that the old wisdom is no longer true.
* Have I told you not to use multiple OSPF processes with the same admin distance? Oh, I did. Keep that in mind, will you?

## Creating the Lab

I decided to use a simple triangle topology with one of the links having a static IP prefix:

{{<figure src="/2021/06/OSPF-Inter-Process.png" caption="Lab topology">}}

This is how I [described it in a YAML file](https://github.com/ipspace/netlab-examples/tree/master/OSPF/multi-process):

```
---
defaults:
  device: csr

module: [ ospf ]

nodes: [ e1, e2, rtr ]

links:
- e1-rtr
- e2-rtr
- e1:
  e2:
  prefix: 10.42.42.0/24
  role: stub
```

With *[netlab](https://netlab.tools/)*, I had a lab up, running, and configured in three minutes. All it took was a single command:

```
$ netlab up
```

Baseline check: *rtr* should have two equal-cost paths to the target prefix:

```
rtr#sh ip route 10.42.42.0
Routing entry for 10.42.42.0/24
  Known via "ospf 1", distance 110, metric 2, type intra area
  Last update from 10.1.0.5 on GigabitEthernet3, 00:01:22 ago
  Routing Descriptor Blocks:
    10.1.0.5, from 10.0.0.2, 00:01:22 ago, via GigabitEthernet3
      Route metric is 2, traffic share count is 1
  * 10.1.0.1, from 10.0.0.1, 00:01:22 ago, via GigabitEthernet2
      Route metric is 2, traffic share count is 1
```

✅ -- no surprise there

Next baseline check: changing the OSPF cost on one interface should result in having a single path to the target prefix:

```
rtr(config)#int gig 2
rtr(config-if)#ip ospf cost 1000
rtr(config-if)#^Z
rtr#sh ip route 10.42.42.0
Routing entry for 10.42.42.0/24
  Known via "ospf 1", distance 110, metric 2, type intra area
  Last update from 10.1.0.5 on GigabitEthernet3, 00:01:51 ago
  Routing Descriptor Blocks:
  * 10.1.0.5, from 10.0.0.2, 00:01:51 ago, via GigabitEthernet3
      Route metric is 2, traffic share count is 1
```

✅ -- as expected. IOS XE 16.6.1 works the way I remember IOS to work.

Next: create a new OSPF process and move the link *rtr-e2* into the new process. 

```
router ospf 3
! 
interface GigabitEthernet3
 description rtr -> e2
 ip address 10.1.0.6 255.255.255.252
 ip ospf network point-to-point
 ip ospf 3 area 0
```

The network now looks like this (from the perspective of *rtr*):

{{<figure src="/2021/06/OSPF-Multi-Process.png" caption="Multi-process OSPF deployment on *rtr*">}}

*rtr* has two paths to 10.42.42.0/24, but learned from two different processes, with admin distance supposedly being the only tie-breaker. In these cases, the router would usually retain the older information to increase network stability.

```
rtr#show ip route 10.42.42.0
Routing entry for 10.42.42.0/24
  Known via "ospf 3", distance 110, metric 2, type intra area
  Last update from 10.1.0.5 on GigabitEthernet3, 00:00:34 ago
  Routing Descriptor Blocks:
  * 10.1.0.5, from 10.0.0.2, 00:00:34 ago, via GigabitEthernet3
      Route metric is 2, traffic share count is 1
```

❌ This is definitely weird. The new entry replaced the old one.

I tried to get the entry from OSPF process 1 in place by clearing OSPF processes, shutting down links... and failed. Time to do some debugging

```
rtr#clear ip route 10.42.42.0
rtr#
RT: del 10.42.42.0 via 10.1.0.5, ospf metric [110/2]
RT: delete subnet route to 10.42.42.0/24
RT: updating ospf 10.42.42.0/24 (0x0) [local lbl/ctx:1048577/0x0]  :
    via 10.1.0.1 Gi2  0 1048578 1048577
RT: add 10.42.42.0/24 via 10.1.0.1, ospf metric [110/1001]
RT: updating ospf 10.42.42.0/24 (0x0) [local lbl/ctx:1048577/0x0]  :
    via 10.1.0.5 Gi3  0 1048578 1048577
RT: closer admin distance for 10.42.42.0, flushing 1 routes
RT: add 10.42.42.0/24 via 10.1.0.5, ospf metric [110/2]
```

The debugging printout claims the second route has *closer admin distance*, but the admin distances are definitely the same. So maybe it's the process number, or the sequence of route insertion that matters. Let's try what happens if we change the OSPF cost in process 3.

```
rtr#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
rtr(config)#int gig 3
rtr(config-if)#ip ospf cost 2000
...
RT: updating ospf 10.42.42.0/24 (0x0) [local lbl/ctx:1048577/0x0]  :
    via 10.1.0.5 Gi3  0 1048578 1048577
RT: closer admin distance for 10.42.42.0, flushing 1 routes
RT: add 10.42.42.0/24 via 10.1.0.5, ospf metric [110/2001]
RT: updating ospf 10.42.42.0/24 (0x0) [local lbl/ctx:1048577/0x0]  :
    via 10.1.0.1 Gi2  0 1048578 1048577
RT: closer admin distance for 10.42.42.0, flushing 1 routes
RT: add 10.42.42.0/24 via 10.1.0.1, ospf metric [110/1001]
```

Now the router claims the prefix coming from OSPF process 1 has *closer admin distance*, whereas in reality it has *lower OSPF cost*. It looks like Cisco IOS uses intra-protocol metrics even when comparing routes coming from different routing protocols *with the same admin distance*.

Just for the giggles, I removed the **ip ospf cost** interface configuration commands, making the paths through *e1* and *e2* equal cost. Whatever I did, *rtr* consistently chose the path through *e1*, so it looks like the inter-process route selection goes even further than the OSPF cost.

Finally, what about the old blog posts I mentioned? Don't expect anyone to fix them, and be careful about the information you glean off the Internet. Hands-on lab results always beat google-and-paste.

### Revision History

2021-07-12
: Updated the blog post to use the new **netlab** CLI.

2021-06-18
: Added _you really really really should not be doing this_ section. Unfortunately I don't expect it to ever dissuade an insistent networking engineer trying to save a broken design with a horrible kludge.