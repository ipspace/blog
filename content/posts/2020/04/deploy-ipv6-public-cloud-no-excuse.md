---
title: Deploying IPv6 in Public Clouds is Easy
date: 2020-04-22 07:55:00
tags: [ cloud, IPv6 ]
---
One of the [hands-on exercises](https://my.ipspace.net/bin/list?id=PubCloud) in our [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course asks the attendees to deploy a full-blown virtual networking solution with a front-end (web) server in a public subnet, and back-end (database) server in a private subnet.

The next (optional) exercise asks them to add IPv6 to the mix for a full-blown dual-stack deployment.
<!--more-->
I knew that AWS had decent IPv6 (networking) support for quite a while, and Azure IPv6 is (maybe) in GA, but I didn't expect the exercise to be almost trivial. Dave Mack decided to go for it, and [solved both tasks at the same time](https://github.com/Dave-Mack/ipspace-public-cloud/tree/master/exercise-4-deploy-virtual-network) using Terraform to provision AWS VPC, subnets, security groups, Internet gateway, and IPv4 and IPv6 route tables. He even performed the connectivity tests over IPv4 and IPv6.

Want to know how he got it done? [Explore his GitHub repository](https://github.com/Dave-Mack/ipspace-public-cloud/tree/master/exercise-4-deploy-virtual-network).