---
title: "Example: Fully-Automated AWS Network Infrastructure Deployment"
date: 2020-06-11 06:45:00
tags: [ cloud, AWS ]
---
Regular readers of my blog probably remember the detailed explanations [Erik Auerswald](https://www.unix-ag.uni-kl.de/~auerswal/) creates while solving hands-on exercises from our [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course (previous ones: [create a virtual network](/2020/03/cloud-automation-create-virtual-network.html), [deploy a web server](/2020/05/example-deploy-web-server-aws.html)).

This time he documented the [process he went through to develop a Terraform configuration file that deploys full-blown AWS networking infrastructure](https://github.com/auerswal/pubcloud2020/tree/master/ex4-infra) (VPC, subnets, Internet gateway, route tables, security groups) and multiple servers include an SSH bastion host. You'll also see what he found out when he used Elastic Network Interfaces (spoiler: routing on multi-interface hosts is tough).

{{<jump>}}[Keep reading](https://github.com/auerswal/pubcloud2020/tree/master/ex4-infra){{</jump>}}