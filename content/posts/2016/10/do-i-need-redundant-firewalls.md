---
date: 2016-10-12 10:44:00+02:00
ha-cluster_tag: firewall
high-availability_tag: ignore
series:
- ha-cluster
tags:
- design
- firewall
- data center
- high availability
title: Do I Need Redundant Firewalls?
url: /2016/10/do-i-need-redundant-firewalls/
---
One of my readers sent me this question:

> I often see designs involving several more than 2 DCs spread over different locations. I was actually wondering if that makes sense to bring high availability inside the DC while there\'s redundancy in place between the DCs. For example, is there a good reason to put a cluster of firewalls in a DC, when it is possible to quickly fail over to another available DC, as a redundant cluster increases costs, licenses and complexity.

Rule#1 of good engineering: Know Your Problem ;) In this particular case:
<!--more-->
-   What's acceptable loss of service?
-   What's your RTO (Recovery Time Objective)?
-   What's your acceptable unit of loss?
-   What's your fallback/recovery approach?

Decades ago when we used carrier pigeons to transport data between terminals and mainframes (not really, but 2400 bps modems weren't much faster), losing a terminal session involved loss of data, cussing, yelling, and plenty of wasted time.

Today, losing an HTTP(S) session results in minor annoyance. Also, your mobile users will lose signal orders of magnitude more often than you'll lose a firewall (at least I hope so), so why bother with a state-sharing cluster. Maybe a fast failover to a secondary unit is good enough.

{{<note>}}I haven't seen any hard data, but intuition suggests that apart from hardware failures a standalone firewall might be more stable than a state-sharing firewall cluster. If you have a pointer to something more tangible, please write a comment!{{</note>}}

However, what does matter to the spoiled users of today is the recovery time. If they want to buy something from your web site and cannot do it **NOW**, they'll walk away and complain loudly on Twitter and Facebook. From this perspective, it makes sense to have an approach that would bring your application back to life ASAP (for whatever value of ASAP). Maybe it's good enough to have a cluster that shares the public IP address but no session state, resulting in session loss and recovery within a few seconds.

If you think you can survive a longer outage every now and then, maybe it's good enough to run a firewall as a VM and have it restarted after the crash.

Finally, does it make sense to declare a data center offline just because its firewall crashed? No, not even to Amazon or Google. You could bypass the failed firewall with routing tricks on DCI link, but it would be way cheaper and less complex to have some firewall redundancy in place within the data center.

Last but definitely not least, there's the divide-and-conquer approach. Don't put all your eggs in one basket (or protect all your application with a single firewall instance).

### Want to Know More?

-   You MUST read [Scalability Rules: Principles for Scaling Web Sites](https://www.amazon.com/gp/product/013443160X/ref=as_li_tl)
-   I haven't read the whole [Site Reliability Engineering: How Google Runs Production Systems](https://www.amazon.com/gp/product/149192912X/ref=as_li_tl) book yet, but even the first chapters are good.
-   I've discussed networking aspects of multi-data-center designs in [Designing Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.
-   The same topic is also [one of the sections](http://nextgendc.ipspace.net/Public:Description) of my [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
