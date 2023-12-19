---
date: 2009-04-25 09:11:00+02:00
ospf_tag: details
tags:
- OSPF
title: OSPF Router ID Selection Trivia
url: /2009/04/ospf-router-id-selection-trivia.html
---
**True or false**: If you have an (enabled) loopback interface configured on the router, its IP address will always be used as the OSPF router ID.
<!--more-->
**Answer: False**. Each OSPF process running on the router needs a unique Router ID. If you have a single loopback interface and two OSPF processes, the second OSPF process is forced to select another interface address as its router ID.

Here is a sample router printout:

``` code
Test#show running | inc ^interface|^ ip address
interface Loopback0
 ip address 10.0.0.1 255.255.255.255
interface FastEthernet0/0
 ip address 10.1.0.1 255.255.255.0
Test#show ip ospf | inc Routing Process
 Routing Process "ospf 2" with ID 10.1.0.1
 Routing Process "ospf 1" with ID 10.0.0.1
```
