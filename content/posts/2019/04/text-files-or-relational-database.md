---
date: 2019-04-23 08:28:00+02:00
tags:
- automation
- Ansible
title: Text Files or Relational Database?
url: /2019/04/text-files-or-relational-database/
series: [ ssot ]
ssot_tag: details
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

One of the common questions I get once the networking engineers progress from Ansible 101 to large-scale deployments (example: generating configurations for 1000 devices) is "Can Ansible use a relational database? Text files don't scale..."

**TL&DR** **answer**: Not directly, but there are tons of database Ansible plugins or custom Jinja2 filters out there.
<!--more-->
### A Quick Detour

Before going into Ansible and relational databases, let me point out that Microsoft managed to put the [whole Windows codebase into a single Git repository](https://blogs.msdn.microsoft.com/bharry/2017/05/24/the-largest-git-repo-on-the-planet/) (admittedly after writing a [Git-specific layer on top of the file system](https://github.com/Microsoft/GVFS)), so I would consider scalability of text files a solved problem. They might not be the best tool for the job, but that's a different story.

### Ansible and Relational Databases

While there's no relational database support built into Ansible, you can always [extend it in multiple directions](https://my.ipspace.net/bin/list?id=AnsibleOC#EXTEND). You could use dynamic inventory scripts or Python modules to solve the particular problem of storing Ansible inventory or host variables in a relational database, and there are plenty of them lying around GitHub, for example [dynamic Ansible inventory for MySQL](https://github.com/avinash6784/ansible-dynamic-inventory-mysql).

However, before rushing out and writing a Python module or adapting the above-mentioned dynamic inventory script, you have to ask yourself:

-   What problem am I trying to solve?
-   What is the best tool for the job?

{{<note info>}}The following section is a very quick summary of the [Data Models and Data Stores](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S1) section from the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course. [Register here](https://www.ipspace.net/Building_Network_Automation_Solutions#register).{{</note>}}

### Text Files or Relational Databases?

Regardless of what technology you use for the data store, your solution has to provide this functionality:

-   Create/Read/Update/Delete (CRUD) functionality
-   Reasonably easy-to-use user interface that provides search, adds, updates and deletes.
-   Data validation and referential integrity (either built-in or through data validation)
-   Change logging and audits (optional)
-   Transactional consistency (optional)

Text files (using text editor + Git) provide all of the above apart from transactional consistency and data validation. Data validation including referential integrity checks is relatively easy to implement with either commit scripts or CI pipeline.

Relational databases provide CRUD functionality, data validation and referential integrity. If you want to have a user interface, change logging, reviews, or audit, you have to add a front-end application (often custom-written).

If you already have a service provisioning system with relational database back-end and good UI, go for it. If you'd have to write it from scratch, text files might be good enough for the first few days.

Is there a middle ground? Sure. You might want to check out IPAM/CMDB platforms like NSoT and NetBox... and speaking of NetBox, [Jeremy Stretch](https://www.ipspace.net/Author:Jeremy_Stretch) talked about it during his [guest speaker presentation](https://automation.ipspace.net/Public:Speakers#Changing_Network_Configurations_or_State) in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
