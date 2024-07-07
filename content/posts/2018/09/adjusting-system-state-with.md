---
date: 2018-09-12 07:42:00+02:00
tags:
- automation
title: Adjusting System State with Infrastructure as Code
series: [ niac ]
niac_tag: implement
url: /2018/09/adjusting-system-state-with/
---
*This is the second blog post in "thinking out loud while preparing Network Infrastructure as Code presentation for the* [*network automation course*](https://www.ipspace.net/Building_Network_Automation_Solutions?utm_source=blog)*" series. If you stumbled upon it, you might want to* [*start here*](/2018/09/network-infrastructure-as-code-is/)*.*

An anonymous commenter to my [previous blog post on the topic](/2018/09/network-infrastructure-as-code-is/) hit the crux of the infrastructure-as-code challenge when [he wrote](/2018/09/network-infrastructure-as-code-is/#c4016391268971561558): "*It\'s hard to do a declarative approach with Ansible and the nice network vendor APIs.*" Let's see what he was trying to tell us.
<!--more-->
The goal of infrastructure-as-code approach is to have a system in a state that's defined by machine-readable (and hopefully human-readable) definition files. The \$1M question is "*How do we get the system in that state?*"

**Building from scratch.** This is the easiest possible approach assuming you can use it. It's been used forever by simple installation scripts; Docker aficionados do it every time they build a container image. It also works quite well in environments that don't patch the servers but rebuild them from scratch. Assuming you're willing to adjust your architecture and processes, you can even make it work for application deployment in fully-virtualized environments like public IaaS clouds.

You can use almost any scripting tool to build a system from scratch -- all you need is something with minimal error detection and looping and branching capabilities (to make your scripts adjustable and/or readable). Bash and Ansible are perfect tools for the job.

**Restarting the system**. Most Linux services use a configuration file that specifies how that service should behave. The configuration file is effectively build-from-scratch script written in domain-specific language (DSL).

Implementing *infrastructure-as-code* for those services is trivial (like I wrote in the original blog post that so upset the above-mentioned commenter: these concepts are old)... but unfortunately, you can't always restart a system.

However, you can get an amazing number of crazy things done if you did your design right: an ISP used this approach to automate their core network in early 2000s.

**Adjusting the system state**. This is the hardest approach to implementing infrastructure-as-code: given a running system, and a definition file specifying the desired state of the system, execute actions that will bring the system into the desired state.

There are tons of tools out there that solve this problem, from environment-specific tools like Docker Compose or Amazon CloudFormation to generic frameworks like Terraform, Chef or Puppet.

Many modern Linux services can adjust their state on their own -- all you have to do is to change the configuration and tell the service to adjust what it's doing based on the new configuration file.

Some network devices can do the same trick. The crudest form of system state adjustment is **configure replace**; Junos, IOS XR and Arista EOS offer a more granular approach using *candidate configuration*.

Assuming you have a networking device that implements configuration replacement at some reasonably good-enough level, there's no need to reinvent the *adjusting system state* wheel on your own with tools like vendor API and Ansible. (or as I wrote in the past: [don't get obsessed with REST API](/2018/04/dont-get-obsessed-with-rest-api/)). The problem has been solved; all you have to do is to:

-   Understand what problem you're trying to solve;
-   Select the best tools for the job;
-   Solve the problem with minimum effort.

### More Information

* We talked about [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
* [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions?utm_source=blog) online course is also focused on these concepts.
