---
date: 2016-04-05 10:35:00+02:00
high-availability_tag: need
series_weight: 650
tags:
- high availability
title: 'High Availability Planning: Identify the Weakest Link'
url: /2016/04/high-availability-planning-identify.html
---
Everyone loves to talk about business critical applications that require extremely high availability, but it's rare to see someone analyze the whole application stack and identify the weakest link.

{{<note info>}}For more details, watch the [Designing Active/Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar{{</note>}}

If you start mapping out the major components of an application stack, you'll probably arrive at this list (bottom-to-top):
<!--more-->
-   Network links and devices;
-   Network services;
-   Servers and storage;
-   Virtualization platforms and operating systems;
-   Databases, message queues...;
-   Applications.

Each one of these components can fail due to hardware failure, software error, or human mistake (operator error).

Next, identify the likelihood of individual failures. Hardware failures (apart from link failures) are less common than software failures or operator errors these days, and in most cases infrastructure failures tend to be less common than application problems.

Finally, figure out how to increase the resilience of each of the components -- redundant links and network devices, network services clusters, dual-homed servers, hypervisor-based high-availability solutions, database replicas, and finally scale-out application architecture.

Now you're ready to start the discussion:

-   Which parts of the whole stack are currently resilient to failures and which ones represent a single point of failure?
-   Which parts could be made more resilient?
-   How will your organization handle the remaining SPOFs?
-   What is the downtime caused by a failure of a non-redundant component?
-   How often can you expect to see those failures?

Getting answers to those questions (good luck ;) might make it easier to persuade the CIO that you company doesn't need a [L2 DCI for disaster recovery](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) (which might happen every 10 years) when the non-redundant applications need a restart every month or remain unpatched for years because nobody wants to touch them... and if everything else fails, you can still [quote Gartner](http://blog.ipspace.net/2015/09/blessed-by-gartner-stretched-vlans-make.html).
