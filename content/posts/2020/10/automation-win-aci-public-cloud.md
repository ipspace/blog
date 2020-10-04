---
title: "Automation Win: Recreating Cisco ACI Tenants in Public Cloud"
date: 2020-10-15 06:22:00
tags: [ automation, cloud ]
---
*This blog post was initially sent to the subscribers of our SDN and Network Automation mailing list. [Subscribe here](http://www.ipspace.net/Subscribe/Five_SDN_Tips).*

Most automation projects are gradual improvements of existing manual processes, but every now and then the stars align and you get a perfect storm, like what Adrian Giacommetti encountered during one of his automation projects.

The customer had well-defined security policies implemented in Cisco ACI environment with tenants, endpoint groups, and contracts. They wanted to recreate those tenants in a public cloud, but it took way too long as the only migration tool they had was an engineer chasing GUI screens on both platforms.
<!--more-->
{{<note>}}The customer decided to use Oracle cloud, but the same principles could apply to AWS, Azure or GCP.{{</note>}}

Adrian was asked to automate the process, and figured out he might have stumbled on a motherlode.

Cisco ACI has rich REST API which allows you to extract all configuration (including everything Adrian needed) as well-formatted data structures. Forget screen scraping and crappy show commands... ACI speaks JSON to make your life easier.

Most public clouds are configurable through REST API, and most infrastructure-as-code tools like Terraform support those APIs.

The hard part of Adrian's job was mapping ACI constructs into public cloud constructs, everything after that was relatively simple programming:

* Extract data from Cisco ACI environment with REST API calls;
* Write a data munging module that transforms Cisco ACI configuration into data structures usable by public cloud API;
* Use public cloud REST API to recreate the environment, or use a templating tool to create a Terraform configuration file from the target data structure.

End result: the migration process took a few minutes instead of months of painstaking error-prone GUI hunting. For more details, [read Adrian's blog post](https://adriangiacometti.net/index.php/2020/09/25/aci-to-oci-with-terraform/), [explore the source code he published on GitHub](https://github.com/aegiacometti/cloud-automation), and [contact him](https://www.linkedin.com/in/adrian-giacometti/) if you have a similar project – he's an independent consultant, and I'm sure he would appreciate some extra work.

Have you encountered a challenge that could be automated as successfully as this one? Managed to make it work? Leave a comment!