---
title: "Network Automation Products for Brownfield Deployments"
date: 2020-10-08 06:44:00
tags: [ automation, intent-based networking ]
intent-based-networking_tag: drawback
---
Got this question from one of my long-time readers:

> I am looking for commercial SDN solutions that can be deployed on top of brownfield networks built with traditional technologies (VPC/MLAG, STP, HSRP) on lower-cost networking gear, where a single API call could create a network-wide VLAN, or apply that VLAN to a set of ports. Gluware is one product aimed at this market. Are there others?

The two other solutions that come to mind are Apstra AOS and Cisco NSO. However, you probably won’t find a simple solution that would do what you want to do without heavy customization as every network tends to be a unique snowflake. 
<!--more-->
The best analogy to deploying a network automation solution in a brownfield environment is a new Enterprise Resource Planning (ERP) system deployment (example: SAP, Microsoft Dynamics, Oracle ERP...).

As every company creates invoices in a slightly different way (because they are so very special) and calculates salaries in slightly peculiar way (yet again, because they’re special), it’s usually impossible to take an off-the-shelf ERP system and deploy it without heavy customization… and after going through endless rounds of customizations, it’s really hard to get rid of the army of consultants tweaking the system on a daily basis to implement all the other bright ideas the business comes up with in the meantime.

Being a grumpy skeptic who has seen too much, I see only three major ways forward for my reader:

* Replace the existing infrastructure with an automated black-box solution (like Cisco ACI or Cisco SD-Access), and [enjoy the show once it breaks](/2018/02/how-self-sufficient-do-you-want-to-be.html);
* Buy a generic automation framework and have someone (internal or external) tweak it to meet your requirements. I’ve seen various vendors building and/or acquiring automation frameworks along these lines since mid 1990s, and they always remained a niche market due to heavy investment required to make it work.
* Slowly build your own system, focusing on major pain points where the automation could result in maximum business/operations impact. Or, in the immortal words of Andrew Lerner, invest in premium people instead of in premium vendors.

And just in case you might be interested in the last option, do check out our [automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) and [online course](https://www.ipspace.net/Building_Network_Automation_Solutions). Numerous networking engineers [built great solutions after attending it](https://www.ipspace.net/NetAutSol/Solutions).
