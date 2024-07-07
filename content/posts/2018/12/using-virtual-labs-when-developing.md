---
date: 2018-12-07 08:57:00+01:00
tags:
- automation
- labs
title: Using Virtual Labs When Developing Network Automation Solutions
url: /2018/12/using-virtual-labs-when-developing/
series: [ cicd ]
cicd_tag: principles
series_weight: 300
---
One of the fundamentals I always emphasize in [introductory parts](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S1) of my network automation [workshops](https://www.ipspace.net/Workshops) and [online courses](https://www.ipspace.net/Building_Network_Automation_Solutions) is the fact that we're about to develop software that will control the most-mission-critical part of IT infrastructure, and should therefore use software development methodologies like version control, testing...

However, there's a "small" glitch. While it's perfectly possible to test most software in some virtual environment you can spin up on-the-fly using Vagrant, Docker, Jenkins, Travis, or some other CI/CD tool, testing a network automation solution requires access to network devices.
<!--more-->
Using virtual labs seems like the only viable approach in most cases, and while we covered all sorts of [error handling, data validation, testing and CI/CD topics](https://my.ipspace.net/bin/list?id=NetAutSol&module=5) in the network automation course, we never focused on virtual labs.

We'll fix that in Spring 2019 course in which two guest speakers ([Matt Oswalt](https://www.ipspace.net/Building_Network_Automation_Solutions#MO19) and [Kristian Larsson](https://www.ipspace.net/Building_Network_Automation_Solutions#KL19)) will focus on using virtual labs. This is what Matt had to say about the topic in an interview with [Christoph Jaggi](http://uebermeister.com/about.html):

> What is the main purpose of building a virtual lab instead of a physical one?

Physical labs require a lot of power, space, and cooling. They're difficult and time‐consuming to change and are usually quite costly to initially acquire as well as maintain long‐term. Virtual labs can take advantage of the consolidation brought about by server virtualization by running network devices as virtual machines, connected with virtual "wires". If you're not trying to validate actual hardware, running a virtual lab can be a more flexible, less costly alternative.

> Would you use a virtual lab for learning, or can it also be used for testing or validation?

Learning is definitely the biggest use case for a virtual lab ‐either learning the platforms themselves, or as a target for learning automation tools on top.

In terms of validation or testing, this largely depends on what you're trying to test or validate. If you're making configuration changes, or writing a script to gather data from all your network devices, this usually only involves the management plane. In this case, a virtual lab is perfectly appropriate for testing, because the differences between a physical and virtual lab with respect to management functionality is usually minimal or nothing.

However, if you're trying to validate anything to do with the data plane, such as trying to replicate a hardware bug, or make certain performance benchmarks, you're likely to run into significant differences that make this testing less valuable. In this case, it might be worth considering a physical lab, if exact real‐world testing is what you're after.

> Virtualization in combination with virtual appliances makes it possible to run complex setups with different elements on a single machine. Can such a virtualized environment provide the same functionality and the same results as an environment that uses dedicated hardware appliances?

Again, in many ways, yes, but it still depends on what you're using the lab for. There are some use cases that just simply can't be faithfully replicated with virtualized hardware. Other use cases don't really depend on hardware features or performance, so for those use cases, virtualized is just fine.

> Does a virtual lab also support the addition of a packet analyzer for real‐time network analysis at line‐rate?

Absolutely, and any other tools you might think of. The benefit of standing things up virtually is that you're not limited to just using network devices; you can absolutely add tools like packet analysis to get used to how they integrate together. Again, the performance characteristics shouldn't be expected to be consistent between a virtualized and a physical topology, but building out a proof‐of‐concept in a virtual lab first will go a long way towards making sure that a physical PoC goes well.

Want to know more? Watch the [Continuous Integration, Delivery and Deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) part of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar and explore the 2019 [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
