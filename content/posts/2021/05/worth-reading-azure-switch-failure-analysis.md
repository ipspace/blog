---
title: "Worth Reading: Azure Datacenter Switch Failures"
date: 2021-05-30 08:12:00
tags: [ data center, switching ]
---
Microsoft engineers published an analysis of switch failures in 130 Azure regions ([review of the article](http://www.racheesingh.com/papers/sigcomm-ccr-final465-with-open-review.pdf), [The Next Platform summary](https://www.nextplatform.com/2021/05/12/microsoft-does-the-math-on-azure-datacenter-switch-failures/)):

* A data center switch has a 2% chance of failing in 3 months (= less than 10% per year);
* ~60% of the failures are caused by hardware faults or power failures, another 17% are software bugs;
* 50% of failures lasted less than 6 minutes (obviously crashes or power glitches followed by a reboot).
* Switches running SONiC had lower failure rate than switches running vendor NOS on the same hardware. Looks like bloatware results in more bugs, and taking months to fix bugs results in more crashes. Who would have thought...
