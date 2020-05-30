---
title: "Enabling IPv6 in AWS Deployments"
date: 2020-06-03 17:27:00
tags: [ IPv6, cloud, AWS ]
---
IPv6 is old enough to buy its own beer (in US, not just in Europe), but there are still tons of naysayers explaining how hard it is to deploy. That's probably true if you're forced to work with decades-old boxes, or if you handcrafted your environment with a gazillion clicks in a fancy GUI, but if you used Terraform to deploy your application in AWS, it's as hard as adding a few extra lines in your configuration files.

[Nadeem Lughmani](https://www.linkedin.com/in/nadeem-lughmani-38b4251/) did a [great job documenting the exact changes needed to get IPv6 working in AWS VPC](https://github.com/nadeemnet/NetworkingInPubClouds/tree/master/networkv6), including adjusting the IPv6 routing tables, and security groups. Enjoy ;)

{{<note info>}}[Deploying IPv6](https://my.ipspace.net/bin/list?id=PubCloud&module=5#HOMEWORK) is just one of many hands-on exercises you have to solve in our [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.{{</note>}}