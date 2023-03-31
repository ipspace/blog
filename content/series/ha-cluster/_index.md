---
title: High Availability Service Clusters
layout: custom
minimal_sidebar: true
sidebar_box: HA
---
Clusters of servers offering the same service in active/standby or active/active setup are a common high availability solution. They work very well as long as:

* The clustering software can reliably detect partitions -- there should always be an odd number of cluster members, or extra witness nodes
* The cluster is not stretched across unreliable infrastructure.

You should also understand how these solutions work:

* Node or service failure in an active/standby setup might cause significant downtime while the service is restarted on another cluster member.
* No clustering solution will protect you against operator mistakes.

Once you grasp these fundamentals, it's perfectly possible to design and deploy well-functioning clusters including network services clusters:

{{<series-listing tag="design">}}

Not surprisingly, solutions created by networking vendors (including [multi-chassis link aggregation](/series/mlag.html) clusters) ignore all of the above. This is what I had to say about the sad state of affairs:

{{<series-listing tag="overview">}}

SDN controllers are no exception:

{{<series-listing tag="sdn">}}

One of the worst examples of the services clusters are firewall clusters. They are almost always implemented with two nodes without a witness, and often stretched across multiple data centers.

{{<series-listing tag="firewall">}}

For even more information, watch:

* [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar
* [BGP Routing with an Edge Firewall](https://my.ipspace.net/bin/list?id=Design#2023_03) from the March 2023 [ipSpace.net Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic)
