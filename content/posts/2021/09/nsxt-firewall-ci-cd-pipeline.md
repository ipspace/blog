---
cicd_tag: solution
date: 2021-09-13 06:20:00+00:00
series:
- cicd
- niac
niac_tag: solution
tags:
- automation
- firewall
- NSX
title: Configuring NSX-T Firewall with a CI/CD Pipeline
---
Initial implementation of [Noël Boulene](https://www.linkedin.com/in/noyelb/)'s [automated provisioning of NSX-T distributed firewall rules](/2021/09/automating-nsxt-firewall-configuration/) changed NSX-T firewall configuration based on Terraform configuration files. To make the deployment fully automated he went a step further and added a [full-blown CI/CD pipeline using GitHub Actions and Terraform Cloud](https://netmemo.github.io/post/tf-gha-nsxt-cicd/).

Not everyone is as lucky as Noël -- developers in his organization already use GitHub and Terraform Cloud, making his choices totally frictionless.
<!--more-->
{{<note info>}}A tip from Noël: don't fight the tool selection if at all possible. Use whatever everyone else is using.{{</note>}}

Apart from storing on-premises security rules in a third-party cloud (assuming you're running NSX-T on-premises and not in AWS), there's another slight glitch in Noël's solution: Terraform instance running within GitHub infrastructure (that's where the CI/CD pipeline is run) must be able to contact on-premises NSX-T Manager. I know a few people that would get shivers when faced with that idea.

If you happen to be at the opposite end of the spectrum from Noël and have to use on-premises solutions you could get the same job done with:

* On-premises GitLab deployment, or GitLab CI/CD runners deployed on a host within your organization. Pete Lumbis [described the idea](https://my.ipspace.net/bin/list?id=NetAutSol&module=5#M5S3A) in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course, and I'm using it for most of my CI/CD pipelines.
* On-premises [Terraform backend](https://www.terraform.io/docs/language/settings/backends/) using Consul, etcd, Kubernetes, Postgres (relational database), or Swift (OpenStack object storage).
