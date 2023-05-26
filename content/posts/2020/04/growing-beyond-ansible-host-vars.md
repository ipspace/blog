---
title: Growing Beyond Ansible host_vars and group_vars
date: 2020-04-16 6:53:00
tags: [ Ansible, automation ]
series: [ ssot ]
ssot_tag: details
---
One of the attendees of my [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course quickly realized a limitation of Ansible (by far the most popular network automation tool): it stores all the information in random text files. Here’s what he wrote:

> I've been playing around with Ansible a lot, and I figure that keeping random YAML files lying around to store information about routers and switches is not very uh, scalable. What’s everyone's favorite way to store all the things?

He’s definitely right (and we spent a [whole session](https://my.ipspace.net/bin/list?id=NetAutSol&module=2#M2S3A) in the network automation course discussing that).
<!--more-->
However, you can get pretty far by using host- and group variable files. For example, [Mark Prior](https://www.ipspace.net/Author:Mark_Prior) (an automation expert with numerous deployments under his belt) still uses them in his projects as he explained in his [Network Infrastructure as Code](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#INFRA_AS_CODE) presentation.

Once you think you should do better, start by consolidating things into a [proper data model which is kept in a single file](/kb/DataModels/30-Generalize%20Network%20Model.html) (instead of having random thingies lying around in host\_vars and group\_vars files). You’ll find more details in the [Data Models](https://my.ipspace.net/bin/list?id=NetAutSol&module=3) part of our automation course (where you'll also find a [section on data stores](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S1)).

The only way to grow beyond data models in text files is by using a database (in which case you’ll have to develop your own UI), or an IPAM/CMDB system that matches your needs. Obviously, you’ll pay for that scalability with increased complexity. You have to export data from one of those systems before running Ansible playbooks, or write dynamic inventory scripts or your own inventory plugin. Anyway, that's the only way to grow if you insist on using Ansible. Maybe you should check out Nornir?

Assuming you did your homework and figured out what data model you need to describe your services or network infrastructure, you could start looking around for the best tool to store that data model in. Netbox is probably one of the best ones because it was designed by a [cool networking engineer with massive experience](https://www.ipspace.net/Author:Jeremy_Stretch)… and he even described his solution in [our automation course](https://my.ipspace.net/bin/list?id=NetAutSol&module=4#M4S3A).
