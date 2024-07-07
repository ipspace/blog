---
cli_tag: fail
date: 2018-10-15 08:37:00+02:00
series:
- cli
series_weight: 1000
tags:
- automation
title: Why Is Network Automation such a Hot Topic?
url: /2018/10/why-is-network-automation-such-hot-topic/
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

One of my readers asked a very valid question when reading the [*Why Is Network Automation So Hard*](/2018/05/why-is-network-automation-so-hard/) blog post:

> Why was network automation \'invented\' now? I have been working in the system development engineering for 13+ years and we have always used automation because we wanted to save time & effort for repeatable tasks.

He's absolutely right. We had [fully-automated ISP service in early 1990's](/2013/11/we-had-sdn-in-1993-and-didnt-know-it/), and numerous service providers [used network automation for decades](https://www.nanog.org/meetings/nanog54/presentations/Tuesday/Morris.pdf).
<!--more-->
As always (as [Russ White would say](/2017/11/the-three-paths-of-enterprise-it/)) it comes down to whether you run your network because it's bringing you money -- in which case you might do whatever it takes to make it bring in more money -- or because you have to -- in which case you'll cut the costs as much as possible. That explains why most enterprises never considered automation. Service providers should have fared better, but many of them evolved from traditional voice operators running static services that barely needed automating.

There were further challenges explained in more details in [Network Automation 101](http://www.ipspace.net/Network_Automation_101) webinar and in introductory part of the [Network Automation workshop](http://www.ipspace.net/Hands-On_Network_Automation) and [online course](http://www.ipspace.net/Building_Network_Automation_Solutions):

-   Networks became mission-critical, and the management didn't trust us to get automation right;
-   We built unique snowflakes that were impossible to automate without heavy customization;
-   Core network devices have humongous [blast radius](/2015/04/on-sdn-controllers-interconnectedness/);
-   We lacked programming skills, proper software development processes and procedures, and affordable test environment;
-   Finally, it was hard to work with network device CLI (more about that at some later time).

What has changed in the last few years?

-   The [SDN brouhaha](/2014/01/control-and-data-plane-separation-three/) forced vendors to give an appearance of becoming "software defined", so most of them came up with something resembling a REST API (there were notable exceptions like Junos that had a good API from day one).
-   Engineers who figured out that SDN means [Still Does Nothing](/2016/02/so-what-exactly-is-sdn/) started thinking about network automation as SDN Lite thingy that could actually make their lives better;
-   A lot of us started evangelizing the need for automation, which might have shifted the mindset a bit;
-   Cloud happened for real -- and once an organization starts deploying their workload in the cloud, you can either get your \*\*\*\* together and deliver services in reasonable time, or become obsolete.

Agree? Disagree? Please write a comment.
