---
title: "Automating NSX-T Firewall Configuration"
date: 2021-09-02 07:14:00
tags: [ automation, NSX, firewall ]
---
[Noël Boulene](https://www.linkedin.com/in/noyelb/) decided to [automate provisioning of NSX-T distributed firewall rules](https://netmemo.github.io/post/nsxt-tf-firewall/) as part of his [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) hands-on work.

What makes his solution even more interesting is the choice of automation tool: instead of using the *universal automation hammer* (aka Ansible) he used Terraform, a much better choice if you want to automate service provisioning, and you happen to be using vendors that invested time into writing Terraform provisioners.

{{<jump>}}[More details](https://netmemo.github.io/post/nsxt-tf-firewall/){{</jump>}}