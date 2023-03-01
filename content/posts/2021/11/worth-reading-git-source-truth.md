---
title: "Git as a Source of Truth for Network Automation"
date: 2021-11-28 07:28:00
tags: [ automation, worth reading ]
series: [ ssot ]
ssot_tag: solution
---
In [Git as a source of truth for network automation](https://vincent.bernat.ch/en/blog/2021-source-of-truth-network), Vincent Bernat explained why they decided to use Git-managed YAML files as the source of truth in their network automation project instead of relying on a database-backed GUI/API product like NetBox.

Their decision process was pretty close to what I explained in *[Data Stores](https://my.ipspace.net/bin/list?id=AutConcepts#DATASTORE)* and *[Source of Truth](https://my.ipspace.net/bin/list?id=AutConcepts#SSOT)* parts of _[Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts)_ webinar: you need change logging, auditing, reviews, and all-or-nothing transactions, and most IPAM/CMDB products have none of those. 

On a more positive side, NetBox (and its fork, [Nautobot](https://blog.networktocode.com/post/why-did-network-to-code-fork-netbox/)) has change logging (HT: [Leo Kirchner](https://blog.kirchne.red/)) and things are getting much better with [Nautobot Version Control plugin](https://www.dolthub.com/blog/2021-09-24-announcing-nautobot-on-dolt/). Stay tuned ;)
