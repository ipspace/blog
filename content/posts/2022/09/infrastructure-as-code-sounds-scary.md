---
date: 2022-09-13 06:53:00+00:00
niac_tag: principles
series:
- niac
tags:
- automation
title: Infrastructure-as-Code Sounds Scary
---
One of my readers preparing for public cloud deployment sent me an interesting observation:

> I pushed to use infrastructure-as-code as we move to Azure, but I'm receiving a lot of pushback due to most of the involved parties not having any experience with code. Management is scared to use any kind of "homegrown" tools that only a few would understand. I feel like I'm stuck deploying and managing the environment manually.

It looks like a bad case of suboptimal terminology for this particular audience. For whatever reason, some infrastructure engineers prefer to stay as far away from programming as possible[^NP], and infrastructure-as-code sounds like programming to them.
<!--more-->
[^NP]: Don't get me started on the "_do we all have to become programmers_" stupidity. I hope we're beyond that.

In reality, [infrastructure-as-code](/series/niac/) means _using the same methodology to handle your infrastructure configuration as you would use for your source code_:

* It has to be in a text file (so it's possible to diff the changes)
* It has to be machine-readable and human-readable (goodbye, XML and JSON 😜)
* It better be managed with a version control system.

We [already have most of that in networking](/2018/09/network-infrastructure-as-code-is/); it's called _device configurations_. A similar concept is completely absent in most server virtualization products (including vSphere and Hyper-V), network virtualization products, including VMware NSX and (to a large extent) Cisco ACI[^ACI], and all private and public clouds I'm aware of.

[^ACI]: Cisco ACI can spew out the system configuration but could not generate tenant configuration in text format the last time I checked.

Instead of saying "_we should use infrastructure-as-code,_" try persuading your peers with "_wouldn't it be great if we would have a configuration file documenting how our cloud networking is configured instead of chasing parameters across GUI screens?_" Bonus points if you manage to add version control on top of that.

As for the "homegrown" tools: there are numerous well-known [intent-based tools](/2018/09/infrastructure-as-code-tools/) that deal with the [CRUD API hell](/2018/09/infrastructure-as-code-netconf-and-rest/). Some of them are provided by the public cloud providers (CloudFormation for AWS or Resource Manager for Azure); the best-known third-party tool with enterprise-grade is probably Terraform. There is absolutely no need to develop new tools to have a well-managed public cloud deployment. All you need are popular tools you can get as free or commercially supported variants, a bit of planning, and a well-defined workflow (for a longer answer [watch this video](https://my.ipspace.net/bin/get/Design/22.06.05%20-%20Tools%20for%20Enterprise%20Public%20Cloud%20Deployments.mp4?doccode=Design) from the [June 2022 Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic)). 

You can also use the examples in the [ipSpace.net Public Cloud GitHub repository](https://github.com/ipspace/pubcloud) to help you get started, and a bunch of ipSpace.net webinars to learn more about public cloud networking:

* [Cloud 101](https://www.ipspace.net/Introduction_to_Cloud_Computing) webinar to get the initial orientation
* [Azure](https://www.ipspace.net/Microsoft_Azure_Networking) and [AWS](https://www.ipspace.net/Amazon_Web_Services_Networking) webinars if you're looking for a deep dive into provider-specific technologies
* [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course if you're interested in design- and architecture aspects.
