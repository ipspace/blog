---
date: 2011-10-14 06:14:00+02:00
dr_tag: avoid
high-availability_tag: dr
series:
- dr
tags:
- data center
- vMotion
- high availability
title: Follow-the-Sun Workload Mobility? Get Lost!
url: /2011/10/follow-sun-workload-mobility-get-lost.html
---
Based on what I wrote about the [latency and bandwidth challenges of long-distance vMotion](https://blog.ipspace.net/2011/09/long-distance-vmotion-for-disaster.html) and why it rarely makes sense to use it in disaster avoidance scenarios, I was asked to write an article to tackle the idea that is an order of magnitude more ridiculous: using vMotion to migrate virtual machines around the world to bring them close to the users.

That article has disappeared a long time ago in the haze of mergers, acquisitions and SEO optimizations, so I'm reposting it here:
<!--more-->
---

After I made a particularly snarky comment about an article that touted inter-data center (DC) virtual machine (VM) mobility as the ultimate tool to reach the 100% availability heavens ([this is why that argument is totally invalid](https://blog.ipspace.net/2011/08/high-availability-fallacies.html)), someone asked me whether I don’t believe in workload mobility, disaster avoidance and follow-the-sun data centers. I am positive that some businesses have needs for all three above-mentioned functionalities, but I also know that live VM migration is not the right tool for the job.

Let’s focus on the most bizarre of the three ideas: using VM mobility to implement *follow-the-sun datacenters*. The underlying business requirements are sound and simple – moving the servers closer to the end-users reduces latency and long-distance bandwidth requirements. Reduced latency also improves response times and throughput (see also [bandwidth-delay product](http://en.wikipedia.org/wiki/Bandwidth-delay_product)). However, you cannot reach this goal by moving the virtual machines around the data centers; you simply can’t move a running virtual machine over long-enough distances.

The maximum round-trip latency supported by vSphere 4.0 is 5 msec. While the timing requirements have been relaxed a bit in vSphere 5.0, the maximum round-trip latency is still 10 msec – way too low to implement the *follow-the-sun* model (you need more than 100 msec to get from Central Europe to Ireland, let alone across the Atlantic or Pacific).

Even if you were able to move a running VM between continents, you’d still face a number of other challenges. Bridging (the traditional mechanism used to support long-distance VM mobility) over such distances is out of question; most layer-2 protocols (like ARP) would time out when faced with round-trip delays measured in hundreds of seconds. You might be able to support the VM mobility with LISP, but even that approach has a number of drawbacks until someone implements LISP within the hypervisors’ soft switches.

So, is it impossible to implement follow-the-sun datacenters? Of course not, Googles of the world have solved the problem more than a decade ago using DNS-based load balancing (or anycast) between data centers and local load balancing within the data center. You can also use AWS and create elastic resources based on geographic load distribution. Both approaches do have one thing in common: they rely on properly architected scale-out applications.

In short, if would be nice if some of the high-level consultants took some time to check product data sheets and laws of physics (like the speed of light) before selling totally impractical marketectures, but I don’t expect it to happen any time soon.

---

As described in the [Data Center Interconnects](https://www.ipspace.net/Data_Center_Interconnects) and [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinars, and the [Scalability Rules](http://www.amazon.com/gp/product/0321753887/ref=as_li_tf_tl) book, the only solution that really works is a scale-out application architecture combined with load balancers.
