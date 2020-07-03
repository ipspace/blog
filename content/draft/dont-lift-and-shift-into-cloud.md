---
title: "Don't Lift-and-Shift Your Enterprise Spaghetti into a Public Cloud"
# date: 2020-07-03 09:48:00
tags: [ cloud ]
draft: True
---
[Jon Kadis](https://www.linkedin.com/in/jon-kadis-006962/) spent most of his life working on enterprise networks, and sadly found out that even changing jobs and moving into a public cloud environment can't save you from people trying to [lift-and-shift](https://twitter.com/cloud_opinion/status/1271643349628280832) enterprise IT kludges into a greenfield environment.

Here's what he sent me:
<!--more-->
- - -
Should you talk to people who are moving to the cloud, remind them not to “drag their data center into the cloud”. Don’t try to duplicate device for device what’s in your data center. Look toward cloud native options, particularly around security that, yes, require you to change the way you think about securing your network, but allow it to be deployed and managed in an automated fashion.

Recently I’m seeing people come into the cloud and want to bring virtual instances of their existing firewall, load balancer,  proxy, and WAF and put them in the middle of a cleanly deployed Infrastructure-as-Code network. Yes, it’s the gear they’re comfortable with and trust. However, for any change in the environment, instead of being a pull-request and a Terraform Plan/Apply they’re back in the GUI making un-source-controlled changes to a (now virtual) box.  Much of the value of IaC gets lost when they start working that way.
- - -
Not surprisingly, that's exactly what Matthias Luft and myself have been explaining in [Cloud Security](https://www.ipspace.net/Cloud_Security) webinar and [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course. The online course even includes a dedicated [Deploying Networking Virtual Appliances](https://my.ipspace.net/bin/list?id=PubCloud&module=7#M9S20) section which could be summarized into "_Don't... and here are a half-dozen reasons why it's a bad idea._"