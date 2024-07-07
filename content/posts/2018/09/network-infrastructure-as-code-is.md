---
date: 2018-09-05 08:12:00+02:00
tags:
- automation
series: [ niac ]
niac_tag: principles
title: Network Infrastructure as Code Is Nothing New
url: /2018/09/network-infrastructure-as-code-is/
---
*Following "if you can't explain it, you don't understand it" mantra I decided to use blog posts to organize my ideas while preparing my Networking Infrastructure as Code presentation for the Autumn 2018 [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course. Constructive feedback is highly appreciated.*

Let's start with a simple terminology question: what exactly is *Infrastructure as Code* that everyone is raving about? Here's what Wikipedia has to say on the topic:
<!--more-->
> Infrastructure as code (IaC) is the process of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. \[...\] The definitions may be in a version control system. It can use either scripts or declarative definitions, rather than manual processes, but the term is more often used to promote declarative approaches.

You might wonder where all the other things are that the *Network Infrastructure as Code* (NIAC) evangelists are talking about like *automated testing, continuous integration,* and *continuous delivery.* Guess what: they're not even mentioned. I'm not saying they're not useful (they are -- and we [already covered them](https://my.ipspace.net/bin/list?id=NetAutSol&module=5) in the automation course), but they are not part of IaC concept.

Now let's go back to the definition. Does "*managing and provisioning infrastructure through machine-readable definition files*" sound familiar?

Are device configurations *definition files*? Of course -- they define what the devices we're applying them to should be doing. Are they *machine-readable*? Evidently. Does that mean that we had *network infrastructure as code* since the early days of Cisco software (even before it was called Cisco IOS)... or going even further, when we were still configuring IBM 3745 front-end processors? What do you think?

### A bit of historical trivia

IBM 3745 ran *Network Control Program* operating system, and the configuration file was really a set of assembler macros that were compiled and linked with the rest of the operating system to get a bootable image. Changing device configuration required a reload... not unlike the way you had to do *configuration replace* on Nexus OS until software release 8.1.

### Need More Information?

We talked about [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) and [continuous integration, delivery and deployment](https://my.ipspace.net/bin/list?id=AutConcepts#CICD) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
