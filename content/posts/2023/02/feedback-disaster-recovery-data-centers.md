---
title: "Feedback: Designing Active/Active and Disaster Recovery Data Centers"
date: 2023-02-16 06:53:00
tags: [ design ]
---
In the _[Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)_ I tried to give networking engineers a high-level overview of challenges one might face when designing a highly-available application stack, and used that information to show why the common "solutions" like stretched VLANs make little sense if one cares about application availability (as opposed to auditor report). Some (customer) engineers [like that approach](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers#Happy_Campers); here's the feedback I received not long ago:

> As ever, Ivan cuts to the quick and provides not just the logical basis for a given design, but a wealth of advice, pointers, gotchas stemming from his extensive real-world experience. What is most valuable to me are those "gotchas" and what NOT to do, again, logically explained. You won't find better material IMHO.

Please note that I'm talking about generic multi-site scenarios. From the high-level connectivity and application architecture perspective there's not much difference between a multi-site on-premises (or collocation) deployment, a hybrid cloud, or a multicloud deployment.