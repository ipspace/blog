---
title: "Worth Reading: ACI Terraform Scalability"
date: 2022-05-29 07:15:00
tags: [ automation ]
---
Using Terraform to deploy networking elements with an SDN controller that cannot replace the current state of a tenant with the desired state specified in a text file (because nobody ever wants to do that, right) sounds like a great idea... until you try to do it at scale.

Noël Boulene hit interesting scalability limits when trying to [provision VLANs on Cisco ACI with Terraform](https://netmemo.github.io/post/aci-terraform-scale/). If you're thinking about doing something similar, you REALLY SHOULD read his article.
