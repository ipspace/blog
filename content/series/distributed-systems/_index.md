---
title: Distributed Systems
layout: custom
sidebar_box: HA
---
Regardless of what anyone is telling you, reliable distributed systems aren't simple. I would strongly recommend you take time and read at least some of these documents first:

* [Fallacies of Distributed Computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)
* [Fallacies of Distributed Computing Explained](http://www.rgoarchitects.com/Files/fallacies.pdf)
* [Notes on Distributed Systems for Young Bloods](https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/)
* [CAP Theorem](https://codahale.com/you-cant-sacrifice-partition-tolerance/)
* [Byzantine Fault Tolerance](https://en.wikipedia.org/wiki/Byzantine_fault)
* [Scaling Distributed Systems is Hard](https://queue.acm.org/detail.cfm?ref=rss&id=2693195)
* [Consensus is Harder Than It Looks](http://brooker.co.za/blog/2020/10/05/consensus.html)
* [Modules, Monoliths, and Microservices](https://tailscale.com/blog/modules-monoliths-and-microservices/)

### Fallacies of Distributed Computing

We covered the fallacies of distributed computing in [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar:

* [Fallacies of Distributed Computing](https://my.ipspace.net/bin/get/Net101/F1%20-%20Fallacies%20of%20Distributed%20Computing.mp4?doccode=Net101)  
* [Network Is (Not) Reliable](https://my.ipspace.net/bin/get/Net101/F2.1%20-%20Network%20Is%20%28Not%29%20Reliable.mp4?doccode=Net101)  
* [Latency Is (Not) Zero](https://my.ipspace.net/bin/get/Net101/F2.2%20-%20Latency%20Is%20%28Not%29%20Zero.mp4?doccode=Net101)  
* [Bandwidth Is (Not) Infinite and Free](https://my.ipspace.net/bin/get/Net101/F2.3%20-%20Bandwidth%20Is%20%28Not%29%20Infinite%20and%20Free.mp4?doccode=Net101)  
* [Networks Are (Not) Secure](https://my.ipspace.net/bin/get/Net101/F2.4%20-%20Networks%20Are%20%28Not%29%20Secure.mp4?doccode=Net101)  
* [Internet Has More than One Administrator](https://my.ipspace.net/bin/get/Net101/F2.5%20-%20Internet%20Has%20More%20than%20One%20Administrator.mp4?doccode=Net101)  
* [Networks Are (Not) Homogenous](https://my.ipspace.net/bin/get/Net101/F2.6%20-%20Networks%20Are%20%28Not%29%20Homogenous.mp4?doccode=Net101)

### Distributed Systems in Software-Defined Networking

Wonder how these concepts apply to [Software-Defined Networking](https://www.ipspace.net/SDN)? Any network is a distributed system, and when you add an SDN controller, it becomes a tightly-coupled distributed system. I explained the implications in a few blog post:

{{<series-listing tag="sdn" year="sure" weight="yes">}}

### Distributed Systems in Network Devices

You might also encounter distributed systems in high-end network devices. I described a few implementation gotchas in these blog posts:

{{<series-listing tag="device" year="sure" weight="yes">}}

### OpenFlow Controllers

Here are some older blog posts focusing on (now mostly obsolete) OpenFlow and OpenFlow-based SDN controllers. I'm including them here because I firmly believe we SHOULD learn from past mistakes:

{{<series-listing tag="openflow" year="sure" weight="yes">}}

### More Details

Need even more details? You'll find them in these webinars (available with [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription)):

* [SDN Architectures and Deployment Considerations](https://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations)
* [SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases)

