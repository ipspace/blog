---
title: "Container-Based Services in Docker"
# date: 2020-07-04 15:25:00
tags: [ Docker ]
draft: True
---
## Basics

* Any container can offer any service
* Containers are attached to internal networks ==> no external access

Solutions:

* Attach containers to external network (macvlan, ipvlan)
* Make internal Docker networks reachable from the outside (routing)
* Make container-based services reachable on external IP addresses.

## Exposed and Published ports

* What is what
* Do you need exposed ports
* Can you publish non-exposed ports

## Behind the Scenes

* NAT tables
* Multi-network setup

## Accessing Container Services over IPv6

* 6-to-4 proxy
