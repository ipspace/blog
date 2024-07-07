---
date: 2017-04-24 11:51:00+02:00
high-availability_tag: need
series_weight: 770
tags:
- design
- data center
- high availability
title: Figure Out What the Customer Really Needs
url: /2017/04/figure-out-what-customer-really-needs/
---
One of the toughest challenges you can face as a networking engineer is trying to understand what the customer really needs (as opposed to what they think they're telling you they want).

For example, the server team comes to you saying "*we need 5 VLANs between these 3 data centers*". What do you do?
<!--more-->
The correct approach is to figure out what problem they're trying to solve, work with them to understand the limitations (from application architecture, database setup, storage replication...) and finally propose a solution that's close enough to what they think they need but doesn't compromise the network stability.

To do that, you have to understand a bit about the application architectures, and that's what I've tried to explain in the [*Designing Active-Active and Disaster Recovery Data Centers*](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar and [numerous other webinars](http://www.ipspace.net/Webinars), as well as in the [university course I've been teaching](http://content.ipspace.net/get/Scalable).

I can't tell you how delighted I was when I received this email from one of the engineers watching my webinar:

> We have a customer and he wanted to migrate his application from active-DR(manual) into active-active or active-active-active and introduce cross-DC load balancing and VLANs everywhere.
>
> So I used the information and guidance based on your webinar to stop this approach (for now, waiting for answer to my feedback) and hopefully it will be changed to proper swimlanes in each DC and DB replication based on their requirements.
>
> So the webinar was very useful, full of ideas and recommendation, and I am satisfied and happy because it helped me in real life. But fight is not finished yet...

I can only wish him luck ;)

#### More information

Want to be like that engineer? Here's one potential path to take:

-   [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) to get you started;
-   [Introduction to Virtualized Networking](http://www.ipspace.net/Introduction_to_Virtualized_Networking) to understand how a physical network interacts with the virtual components;
-   [vSphere 6 Networking Deep Dive](http://www.ipspace.net/VSphere_6_Networking_Deep_Dive) if you want to figure out the best way to connect VMware hosts to a data center network;
-   [Leaf-and-Spine Fabrics](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) to master the intricacies of modern data center network designs;

You get access to all these webinars (and over 60 more) with the [ipSpace.net subscription](http://www.ipspace.net/Subscription).

Finally, when you're ready for the big challenge, take the [Building Next-Generation Data Center online course](http://www.ipspace.net/Building_Next-Generation_Data_Center).
