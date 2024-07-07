---
cicd_tag: tools
date: 2021-03-09 06:23:00+00:00
series:
- cicd
tags:
- automation
title: 'Interesting Tool: Schema Enforcer'
---
It looks like JSON Schema is the new black. Last week I wrote about a [new Ansible module](/2021/03/ansible-validation/) using JSON Schema to validate data structures passed to it; a few weeks ago NetworkToCode released [Schema Enforcer](https://blog.networktocode.com/post/introducing_schema_enforcer/), a similar CLI tool (which means it's easy to use it in any CI/CD pipeline).

{{<note info>}}Wondering why schema validation matters? [Start here](/kb/DataModels/70-Validation/). See also: [GIGO](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out).{{</note>}}

Here are just a few things Schema Enforcer can do:
<!--more-->
* Validate any YAML file against a JSON schema just by including a comment at the top of the YAML file (much better than my crazy pipeline including **yq** and a temporary file).
* Read JSON schema in YAML format. A beautiful addition for everyone who got squinty eyes from looking at too many curly braces.
* Validate Ansible inventory using schema(s) specified in additional Ansible variables or even based on variable names used in Ansible inventory.

Interested? It's on [GitHub](https://github.com/networktocode/schema-enforcer/) -- download it and make it work for you.