---
date: 2018-09-26 08:56:00+02:00
tags:
- automation
- AWS
title: Infrastructure-as-Code Tools
url: /2018/09/infrastructure-as-code-tools.html
series: [ niac ]
niac_tag: implement
---
*This is the fourth blog post in "thinking out loud while preparing Network Infrastructure as Code presentation for the [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions?utm_source=blog)" series. Previous posts: [Network-Infrastructure-as-Code Is Nothing New](/2018/09/network-infrastructure-as-code-is.html), [Adjusting System State](/2018/09/adjusting-system-state-with.html) and [NETCONF versus REST API](/2018/09/infrastructure-as-code-netconf-and-rest.html).*

[Dmitri Kalintsev](https://telecomoccasionally.wordpress.com/about/) sent me a nice description on how some popular Infrastructure-as-Code (IaC) tools solve the challenges I described in *The CRUD Hell* section of [Infrastructure-as-Code, NETCONF and REST API](/2018/09/infrastructure-as-code-netconf-and-rest.html) blog post:
<!--more-->
> The CRUD hell you\'re describing only applies to the configuration management tools that were bent out of shape to pretend being an infrastructure-as-code tool.

Even worse, there's a tool that (by default) performs **show running** every time it's asked to change anything in a network device configuration instead of caching the device configuration (system state), resulting in ridiculously slow progress that I described in [*Configuring Network Devices: Lessons Learned*](https://my.ipspace.net/bin/list?id=NetAutSol&module=4#M4S2A) part of [network automation online course](https://www.ipspace.net/Building_Network_Automation_Solutions). Hint: its name starts with A ;)

> The tools I can speak confidently about - Terraform and CloudFormation - come with their own state DB that stores the complete state of the objects that a template instance \"owns\". In Terraform\'s case, \"refresh\" at apply/destroy is completely optional, and computation of \"what\'s to be done\" can be performed entirely based on the state DB\'s contents.

While that sounds great, do remember the two biggest challenges of computer science:

-   Naming things (irrelevant in this context)
-   Cache coherence
-   Off-by-one errors

When using [UDP clouds](http://www.it20.info/2011/04/tcp-clouds-udp-clouds-design-for-fail-and-aws/), it might be a bit risky to rely on the cached state database when adjusting system state, but then I guess we're always trading performance for reliability and consistence (see also: [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)).

> These tool would only do the REST calls that are strictly necessary, rather than make them over and over, followed by the state read and re-computation in an attempt to \"converge\" the config to the desired state.

That's what any reasonable software engineer would do:

-   Collect the system state (or trust a cached state);
-   Compute the difference between current and desired state;
-   Execute the commands (or API calls) that bring the current state closer to desired state... in just the right order to make them work;
-   Save the desired state in your cache as the new system state.

The tools that repeatedly read system state just prove that heaping layers of abstraction of top of one another rarely results in a high-performance system (see also: [software disenchantment](http://tonsky.me/blog/disenchantment/)).

Obviously some tools know how to do things right. As Dmitri explained in a follow-up email exchange:

> In case of Terraform, if you choose to not do automatic refresh at the \"terraform apply\" time, you have an option to refresh the state of managed objects \"on demand\" - by running \"terraform refresh\". You could do this periodically during quiet hours to make sure your state is fresh, if the out-of-sync state is of a real concern. You can even can tell Terraform which specific resource(s) to refresh.

Anyway, if your infrastructure-as-code problem happens to be pretty common (example: deploy LAMP or MEAN stack in AWS), there are plenty of tools you can use -- forget all the nitty-gritty details, choose one that's good enough for your needs and move on.

The real problem starts when you want to apply infrastructure-as-code principles to niche environments like physical networking. The only decent NIaC tool I'm aware of is Cisco NSO (with a reassuringly expensive price tag). Anything else? Please write a comment!

The other way forward is to build the minimum viable tool you can use to solve your problem (because you really don't want to reinvent the whole wheel). We covered [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar, and you'll find tons of ideas, guidelines and how-tos in [Building Network Automation Solutions online course](https://www.ipspace.net/Building_Network_Automation_Solutions).
