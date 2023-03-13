---
date: 2019-03-07 09:28:00+01:00
tags:
- automation
- data models
title: Building Network Automation Source-of-Truth (Part 2)
url: /2019/03/building-network-automation-source-of.html
series: [ ssot ]
ssot_tag: build
---
In the first blog post of this series I described how you could [start building the prerequisite for any network automation solution: the device inventory](https://blog.ipspace.net/2019/02/building-network-automation-source-of.html).

Having done that, you should know *what* is in your network, but you still don't know *how* your network is supposed to work and *what services* it is supposed to provide. Welcome to the morass known as *building your source-of-truth*.
<!--more-->
### There Can Be Only One

Before going into the details: source-of-truth (an accurate description of how your network is supposed to behave) is the most important bit of information you're dealing with... and there can be only one (or many sources of conflicting partial truths, also known as lies).

Having said that, don't aim for a humongous database describing everything there is to know about your network. It doesn't matter (for today's discussion) if you store all the information in the same database, or if you have to store bits of it in IPAM, some other bits in an orchestration system, and some extraneous information in text files... as long as (A) there's no data duplication, (B) you know where the information you need is and (C) the process to modify any bit of information is well-defined.

### In the Ideal World

This is how you should build and use a source-of-truth in an ideal world:

-   Define a service;
-   Define an abstract data model describing the service;
-   Figure out the best data store to use and a process to modify the data model (anything from Notepad to web UI)
-   Create data transformations that create device-specific data structures from the abstract data model (anything from YANG data models to traditional device configurations);
-   Combine device-specific information from all services that should be provided by a device and deploy the desired state of the device.

Not surprisingly, this is how most well-designed orchestration, network automation, or intent-based products work (the difference between the three categories is usually the need to get venture capital or sell something supposedly new). The real question is: "*how well does this idea work in the brownfield environments of the real world?*" Short answer: "*as always, there's a huge gap between theory and practice*"

### Meanwhile on Planet Earth

The best you can hope for in most environments that [don't run networks as their core business](https://blog.ipspace.net/2017/11/the-three-paths-of-enterprise-it.html) (some Service Providers got their act together and managed to move pretty close to the ideal world) is an Excel spreadsheet listing VLANs, another Excel spreadsheet with semi-accurate subnet assignments, and tribal knowledge. The only source-of-truth (description of how the network works and what services it provides) you'll find in these environments is the device configuration.

There are few things you can do when faced with reality:

-   **Give up** and [invent a gazillion excuses](https://blog.ipspace.net/2016/11/finding-excuses-to-avoid-network.html) why you can't possibly automate your network. Based on some comments I'm regularly getting this seems to be a very popular choice;
-   **Hope you'll be able to automate new deployments**. This should work in theory, but you'll most likely fail miserably due to lack of automation mindset and discipline. It's hard to keep a deployment consistent if everyone thinks they can get custom-tailored network service to [support whatever mistakes they made in application design](https://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html), or if network technicians believe the right way to fix problems is to log into devices and start throwing random configuration commands at problems until the problems become scared enough to disappear (temporarily and for no good reason);

{{<note>}}
A very large organization decided to automate the deployment of new data centers covering everything from initial software upgrades to connectivity and services testing and validation, and managed to deploy a brand new data center every month with a tiny team. Unfortunately, the moment the deployment team walked away, the local ops team immediately reverted to **configure terminal**, totally destroying the value created in the deployment process.
{{</note>}}

-   **Get your hands dirty** and start the tedious process of getting rid of the current mess.

There's only one good advice you can give someone who's faced with an enormous task like eating an elephant: don't give up and do it one bite at a time. Here are some ideas you might be able to use when gradually building your source-of-truth:

-   Identify small bits of annoying inconsistencies. The usual culprits would be NTP, SYSLOG, and DNS configuration;
-   Create simple data models that describe the desired state of these services. It could be a simple as a list of servers in a YAML file;
-   Create templates to produce configuration snippets from your simple data model;
-   Create a process that integrates the configuration snippets with existing device configuration.

{{<note info>}}
Several attendees of our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) decided to do exactly this as one of the hands-on assignments, [usually across numerous platforms from a half-dozen vendors](https://blog.ipspace.net/2018/01/synchronize-network-management.html).
{{</note>}}

You might be lucky enough to have equipment from a vendor that can spell *data models* or *candidate device configuration* (hint: [focus on these requirements](https://blog.ipspace.net/2016/10/network-automation-rfp-requirements.html) instead of PowerPoint-based unicorn poop the next time you're buying networking gear) in which case the integration process is reasonably simple. If you're not so lucky, explore the [brownfield automation solution](https://www.ipspace.net/kb/ConfigRegex/) described by Josef Fuchs.

Lather, Rinse, Repeat. Slowly expand the scope of services (or configuration snippets) described by your data models. Make sure all new services are born in the ideal world. You'll still have an enormous amount of legacy to deal with, but at least you'll be moving forward and demonstrating the value automation brings to the table (consistency, repeatability, better processes, change management...).

When you cleaned up a significant part of network services, start enforcing the automation data models as the primary source of truth - whenever an actual device configuration doesn't match the configuration generated through your templates it should be fixed. The cleanup process will be long and tedious, but you'll have to do it eventually... and you might find some great ideas in Mat Wood's talk describing [how they solved this challenge in Facebook enterprise network](https://my.ipspace.net/bin/list?id=NetAutSol&module=6#M6S2).

Makes sense? Disagree? Please write a comment... and if you decide to go down this path, follow [hundreds of fellow networking engineers](https://www.linkedin.com/school/ipspace-building-network-automation-solution-course/) who found [our network automation online course](https://www.ipspace.net/Building_Network_Automation_Solutions) highly useful.
