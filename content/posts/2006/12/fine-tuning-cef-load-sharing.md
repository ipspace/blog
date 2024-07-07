---
date: 2006-12-12 12:30:00+01:00
tags:
- CEF
- load balancing
title: Fine-Tuning CEF Load Balancing
url: /2006/12/fine-tuning-cef-load-sharing/
---
In environments with a low number of IP hosts you have to fine-tune the CEF load-sharing algorithm to ensure that the traffic is spread between all parallel paths. A typical scenario is a primary-backup data center setup with pairs of replicating servers, as shown in the figure below.

{{<figure src="/2006/12/LoadSharing_1.jpg">}}

In these cases, you have to try different values of *seed* parameter of the [CEF universal algorithm.](/2006/10/cef-per-destination-load-sharing/)
<!--more-->
For example, if you have two equal-cost paths between networks 10.0.0.0/24 and 192.168.0.0/24...

``` {.code}
a1#show ip cef 192.168.0.0 detail
192.168.0.0/24, version 33, epoch 0, per-destination sharing
0 packets, 0 bytes
 via 172.16.1.6, Serial0/0/0.200, 0 dependencies
   traffic share 1
   next hop 172.16.1.6, Serial0/0/0.200
   valid adjacency
 via 172.16.1.2, Serial0/0/0.100, 0 dependencies
   traffic share 1
   next hop 172.16.1.2, Serial0/0/0.100
   valid adjacency
```

\... you might want the traffic between 10.0.0.1 and 192.168.0.1 to flow over a different link than the traffic between 10.0.0.2 and 192.168.0.2. The command that will help you is the **show ip cef exact-route *source destination***. In our example, both traffic flows would go over the same serial link:

```
a1#show ip cef exact-route 10.0.0.1 192.168.0.1
10.0.0.1 -> 192.168.0.1 : Serial0/0/0.100 (next hop 172.16.1.2)
a1#show ip cef exact-route 10.0.0.2 192.168.0.2
10.0.0.2 -> 192.168.0.2 : Serial0/0/0.100 (next hop 172.16.1.2)
```

However, by changing the *seed* parameter of the **ip cef load-sharing algorithm universal** command, you can influence the [CEF hashing function](/2006/10/cef-load-sharing-details/), eventually reaching a state where the traffic flows are spread between both WAN links:

```
a1(config)#ip cef load-sharing algorithm universal 1
a1(config)#^Z
a1#show ip cef exact-route 10.0.0.1 192.168.0.1
10.0.0.1 -> 192.168.0.1 : Serial0/0/0.100 (next hop 172.16.1.2)
a1#show ip cef exact-route 10.0.0.2 192.168.0.2
10.0.0.1 -> 192.168.0.2 : Serial0/0/0.200 (next hop 172.16.1.6)
```
