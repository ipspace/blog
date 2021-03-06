---
title: "Using YAML Instead of Excel in Network Automation Solutions"
date: 2021-03-16 07:45:00
tags: [ automation ]
---
One of the attendees of our network automation course asked a question along these lines:

> In a previous Ansible-based project I used Excel sheet to contain all relevant customer data. I converted this spreadsheet using python (xls_to_fact) and pushed the configurations to network devices accordingly. I know some people use YAML to define the variables in Git. What would be the advantages of doing that over Excel/xsl_to_fact?

Whenever you're choosing a data store for your network automation solution you have to consider a number of aspects including:
<!--more-->
* What will the user interface be?
* Do I need transactional consistency?
* Do I need to track changes to the data?
* How will I validate changes?
* Do I need to know who made the changes and when?

Considering just these five aspects (there are probably many more), what are the options?

* Excel provides a nice user interface, but nothing else.
* YAML files combined with Git provide change tracking and logging, but UI sucks (cue **vi** versus **emacs** saga). Data validation usually happens in Git/CI/CD pipelines, starting from Git pre-commit hooks. Data is *eventually-consistent*; merge conflicts have to be resolved manually.
* Relational databases provide transactional consistency but little else. Most notably, you have to create your own UI. They do provide baseline data checking (is a value in a field expecting a number really a number) and referential integrity, but you might still need further checks implemented in the UI component (example: is IP address valid) or deployment pipeline (example: is interface name valid).
* IPAM/CMDB tools provide nice UI, data validation, and transactional consistency (because they're running on top of a relational database), but usually no change tracking or logging.

Assuming you want to keep things simple, I'd prefer YAML over Excel:

* Excel has simple row/column data structure. In YAML you could have richer (structured) data types.
* You could track changes to YAML files with Git. Doing that in Excel is... interesting.
* Don't get me started on the beauties of having a shared Excel spreadsheet in a Dropbox folder.

Finally:

* Using YAML files (or Excel spreadsheets) will get you started, but you'll need something better in the long run.
* Some people use Excel as a query tool. No problem with that -- after deploying the services (based on YAML files), collect the new configuration/operational state and present it in a read-only Excel spreadsheet.

### More details

* I wrote about *transactional* and *eventual* consistency in [State Consistency in Distributed SDN Controller Clusters](https://blog.ipspace.net/2021/02/state-consistency-distributed-controllers.html)
* We [discussed data stores](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S1) in [Data Models](https://my.ipspace.net/bin/list?id=NetAutSol&module=3) module of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
* We'll also talk about data stores in one of the future sessions of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.

You might also want to read:

* [Text Files or Relational Database?](https://blog.ipspace.net/2019/04/text-files-or-relational-database.html)
* [Growing Beyond Ansible host_vars and group_vars](https://blog.ipspace.net/2020/04/growing-beyond-ansible-host-vars.html)
* [Validating Data in GitOps-Based Automation](https://blog.ipspace.net/2020/10/validating-data-gitops-automation.html)
* [Automation Solution: Testing Data Models](https://blog.ipspace.net/2020/01/automation-solution-testing-data-models.html)
* [Validate Ansible YAML Data with JSON Schema](https://blog.ipspace.net/2020/10/validate-yaml-jsonschema.html)
