---
date: 2020-01-30 10:57:00+01:00
ha-cloud_tag: intro
high-availability_tag: cloud
series:
- ha-cloud
tags:
- design
- cloud
- high availability
title: You're Responsible for Resiliency of Your Public Cloud Deployment
url: /2020/01/youre-responsible-for-resiliency-of.html
---
Enterprise environments usually implement "mission-critical" applications by pushing [high-availability requirements down the stack](/2013/04/this-is-what-makes-networking-so-complex.html) until they hit networking... and then blame the networking team when the [whole house of cards collapses](/2019/10/disaster-recovery-faking-take-two.html).

Most public cloud providers are not willing to play the same stupid blame-shifting game - they live or die by their reputation, and maintaining a stable service is their highest priority. They will do their best to implement a robust and resilient infrastructure, but will not do anything that could impact its stability or scalability... including the snake oil the [virtualization](/2015/02/before-talking-about-vmotion-across.html) and [networking](/2019/11/stretched-vlans-and-failing-firewall.html) vendors love to sell to their gullible customers. When you deploy your application workloads into a public cloud, you become responsible for the resiliency of your own application, and there's no magic button that could allow you to push the problems down the stack.
<!--more-->
Public cloud providers give you plenty of tools to help you build a highly resilient application, from availability zones and regions to multi-level load balancing, storage replication and managed cloud services... but you have to use them the right way. Application teams that invested into learning how to do that would feel right at home, those relying on vendor magic will be totally lost.

Our [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course will [help you master this topic](https://my.ipspace.net/bin/list?id=PubCloud&module=8). We'll start with requirements and definitions, inspect sample application architectures, revisit lessons learned operating a traditional well-designed mission-critical environment, and [hear from Justin Warren](https://www.ipspace.net/PubCloud/#JW20) how they apply to public cloud deployments.
