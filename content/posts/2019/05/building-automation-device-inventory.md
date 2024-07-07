---
date: 2019-05-07 08:33:00+02:00
tags:
- automation
title: Building Automation Device Inventory with Open Source Tools
url: /2019/05/building-automation-device-inventory/
series: [ ssot ]
ssot_tag: solution
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

One of the common questions we get in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course is "*how do I create device inventory if I don't know (exactly) what devices are in my network?*"... prompting one of the guest speakers to reply "*could it really be that bad?*" (yes, sometimes it is).

Some of the students tried to solve the challenge with Ansible. While that *might* eventually work (given enough effort), Ansible definitely isn't the right tool for the job.

What you need to get the job done is a proper toolchain:
<!--more-->
-   A tool that is good in doing device discovery -- network management tools usually pretty do a decent job;
-   A data store (or tool) that will act as your authoritative source-of-truth. Based on the complexity of your network and the desired editing method (text editor versus API/GUI) you could go with text files, a database, or an IPAM tool;
-   A script that will export the information from the source-of-truth into a format usable by your automation tool (example: dynamic inventory script for Ansible).

Next steps:

-   Selecting the tools;
-   Building the toolchain.

Gian Paolo Boarina [documented an interesting toolchain he built](https://www.ifconfig.it/hugo/post/monitoringmvp/):

-   Device discovery with LibreNMS;
-   Inventory and source-of-truth in NetBox;
-   Export of NetBox inventory into Icinga.

All you have to if you want to use the same toolchain with Ansible is to build a dynamic inventory script to export NetBox information into a JSON/YAML blob that Ansible can use.. oh wait, [here's one](https://pypi.org/project/ansible-netbox-inventory/) ;)

Happy toolchaining... and if you want to learn more about network automation watch our [network automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) or register for the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
