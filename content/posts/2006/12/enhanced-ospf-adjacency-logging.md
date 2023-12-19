---
date: 2007-01-09 22:12:00+01:00
ospf_tag: config
tags:
- syslog
- OSPF
- logging
title: Enhanced OSPF Adjacency Logging
pre_scroll: True
url: /2006/12/enhanced-ospf-adjacency-logging.html
---
The **log-adjacency-changes** OSPF configuration command was improved with the **detail** command that logs every step of OSPF adjacency establishment (sample printout below), making it a great troubleshooting tool.

```
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from DOWN to INIT, Received Hello
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from INIT to 2WAY, 2-Way Received
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from 2WAY to EXSTART, AdjOK?
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from EXSTART to EXCHANGE, Negotiation Done
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from EXCHANGE to LOADING, Exchange Done
%OSPF-5-ADJCHG: Process 1, Nbr 172.16.0.21 on Serial0/0/0.100 from LOADING to FULL, Loading Done
```
