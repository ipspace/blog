---
title: "Arista EOS Configuration Automation"
date: 2022-12-08 07:42:00
tags: [ automation ]
---
I keep getting questions along the lines of "_is network automation practical/a reality?_" with arguments like:

> Many do not see a value and are OK with just a configuration manager such as Arista CVP (CloudVision Portal) and Cisco DNA. 

[Configuration consistently is a huge win](/2018/04/configuration-templating-could-be-huge.html) regardless of how you implement it (it's perfectly fine if the tools your vendor providers work for you). It prevents _opportunistic consistency_, as Antti Ristimäki [succinctly explained](/2022/11/automation-service-provider.html):
<!--more-->
> Without automation it would be also very difficult to enforce the desired configurations and would result in an opportunistic network where certain configurations are only applied if an engineer has remembered to, or cared to, configure them.

Having your network described as a set of well-defined parameters (aka [Source of Truth](https://my.ipspace.net/bin/list?id=AutConcepts#SSOT)) instead of [device configurations scattered all over the globe](/2019/03/creating-automation-source-of-truth.html) is another huge win, so it's no surprise that a lot of engineers include these concepts in their new projects. Here's what [Gaël Garcin](https://www.linkedin.com/in/ga%C3%ABl-garcin-39abbb12/) recently sent me:

---

In my last project I implemented a new leaf and spine 100G Arista fabric with BGP-EVPN for our core network. After having learned how it works, I have also found [Arista's Ansible libraries](https://avd.sh) to do a very clean job.

The result now is a 100% infrastructure-as-code core network, all starting from inventory files which generate all the fabric links and tenant configuration. The full router configurations are generated at each run and then pushed to Arista CVP which then does the change management, in particular with a “diff” print so we can see exactly what will be added or removed when we apply the change in production. It is a complete new way of working but so interesting! And I really don’t see a better time to do this change: it allows you to start slowly and migrate the production step by step while you get used to this new environment.

---

In a nutshell:

* Create a machine-readable high-level description of your network. It doesn't matter (initially) if you use [text files](/2021/11/worth-reading-git-source-truth.html) or [something more complex](/2019/04/text-files-or-relational-database.html);
* Create consistent device configuration templates, and use them as the sole means of creating device configuration (don't forget to consider how to implement the [Big Red Button](/2018/02/big-red-button-for-network-automation.html))
* Use whatever workflow works for you to deploy the configurations
* Squeeze the most out of the vendor-supplied tools, but don't be limited by their functionality.

Want to know more? Start exploring the [automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars).