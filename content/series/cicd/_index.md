---
title: CI/CD in Networking
layout: custom
minimal_sidebar: true
sidebar_box: NetOps
---
{{<quote source="ChatGPT explaining CI/CD in networking">}}CI/CD in networking is a process that helps ensure networking configurations are continuously integrated and deployed in a safe and efficient manner. This involves using automated tools to check the networking configurations for errors and misconfigurations before deploying them to the network infrastructure. If issues are found, developers are alerted to make the necessary fixes. This process helps to prevent network downtime, improve network reliability, and ensure that users have a seamless experience.{{</quote>}}

### {{<plushy confused>}}What Exactly Is CI/CD?

Interested? Let's start with the fundamentals:

{{<series-listing tag="principles" weight="yes">}}

You might also want to explore [network-infrastructure-as-code](/series/niac.html) concepts.

### {{<plushy master>}}Testing, Validation, and Tools

If you want to automate source code integration and deployment, you have to ensure that the changes you're making to your existing codebase won't break it. Testing and validation are thus the crucial elements of CI/CD pipelines:

{{<series-listing tag="testing">}}

Here are a few tools you might find useful:

{{<series-listing tag="tools">}}

### {{<plushy magic>}}Sample Solutions

Several attendees of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course used CI/CD pipelines in [their automation solutions](https://www.ipspace.net/NetAutSol/Solutions). Some of those solutions are published on GitHub, giving you a glimpse into working code:

* Daniel Teycheney [created a CI pipeline](https://github.com/writememe/BlgNetAutoSol/tree/master/5_Logging_Testing_Validation) that validates Ansible playbooks before they're merged with the *master* branch.
* Donald Johnson [checks data models before committing them into a Git-based repository](https://github.com/johnsondnz/ipspace-validation-example/blob/master/README.md)

I also blogged about these CI/CD solutions:

{{<series-listing tag="solution">}}


### {{<plushy happy>}}More Information

Watch the [Continuous Integration, Delivery and Deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) part of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar and listen to these podcasts:

{{<series-listing tag="podcast">}}

We covered the CI/CD pipeline- and network testing details in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course:

* [Thomas Wacker](https://www.ipspace.net/Author:Thomas_Wacker) described how [UBS AG embraced automation and automated testing for their data center network rebuild](https://my.ipspace.net/bin/list?id=xNetAut173#UBS).
* [Kristian Larsson](https://www.ipspace.net/Author:Kristian_Larsson) explained the [basics of network testing and the use of virtual routers in CI/CD testing](https://my.ipspace.net/bin/list?id=xNetAut191#SYSTEST).
* [Gabriele Gerbino](https://www.ipspace.net/Author:Gabriele_Gerbino) presented some practical examples on how to build a [simple CI/CD testing pipeline](https://my.ipspace.net/bin/list?id=xNetAut183#PIPELINE).
* [David Barroso](https://www.ipspace.net/Author:David_Barroso) explained how you can [use NAPALM to validate whether the actual state of a network device meets its desired state](https://my.ipspace.net/bin/list?id=AnsibleOC#NAPALM-VALIDATE).
* [Pete Lumbis](https://www.ipspace.net/Author:Pete_Lumbis) explained the [basics of Continuous Integration and Continuous Delivery (CI/CD)](https://my.ipspace.net/bin/list?id=xNetAut171#CICD) and dived deep into [Continuous Integration with GitLab](https://my.ipspace.net/bin/list?id=xNetAut173#GITLAB_CI).