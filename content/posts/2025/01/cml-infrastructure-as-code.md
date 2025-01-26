---
title: "Cisco Modeling Labs and Infrastructure-as-Code"
date: 2025-01-29 07:18:00+0100
tags: [ worth reading ]
---
_Dalton Ortega, Cisco Modeling Labs Product Manager, sent me the following email as a response to my [Configuring IP Addresses Won&#39;t Make You an Expert](https://blog.ipspace.net/2025/01/common-labbing-misconceptions/) blog post:_

First, your statement on Autonetkit is indeed correct. We had removed that from the product due to lack of popularity. That being said, in our roadmap we are looking at methods to reintroduce on-the-fly configuration as well as enhancing our sample labs library to make getting started with CML easier.
 
Secondly, CML can be run in full IaC mode because of the API-first build. In fact, many of our customers are using CML as an automated test/validation bed for their CI/CD pipelines. Tools like Ansible and Terraform are available to facilitate this inside CML too. For more details, read:

* [Get Started With Terraform and Cisco Modeling Labs](https://blogs.cisco.com/learning/get-started-with-terraform-and-cisco-modeling-labs)
* [How to Use Ansible with CML](https://blogs.cisco.com/learning/how-to-use-ansible-with-cml)

{{<long-quote>}}
It seems it should be relatively easy to create a _cml_ [provider](https://netlab.tools/providers/) to generate a Terraform file from the _netlab_ topology and use it to start a lab in CML. Any volunteers?
{{</long-quote>}}