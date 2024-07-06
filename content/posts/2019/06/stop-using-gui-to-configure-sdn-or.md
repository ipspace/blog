---
cli_tag: real
date: 2019-06-06 08:18:00+02:00
intent-based-networking_tag: drawback
series:
- cli
tags:
- automation
- intent-based networking
- SDN
title: Stop Using GUI to Configure SDN or Intent-Based Products
url: /2019/06/stop-using-gui-to-configure-sdn-or.html
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

At the end of my [vNIC 2018 keynote speech](/2018/10/making-sense-of-software-defined-world.html) I made a statement along these lines:

> The moment you start using GUI with an SDN product you're back to square one.

That claim confused a few people -- Mark left [this comment](/2018/10/making-sense-of-software-defined-world.html?showComment=1539476892425#c8729491570071533210) on my blog:
<!--more-->
> My question is what is the alternative to a GUI which I interpret in an SDN world as a central authority that has oversight and controls all aspects of 10's, 100's or potentially 1000's of devices/sites?

Before I dive into the details, let's put some context around my statement (because I know that not everyone will go and [watch the presentation](https://my.ipspace.net/bin/list?id=SDDC101#vNIC2018) to understand it): it was made in an SDDC presentation assuming the users of a particular SDDC product (NSX) plan to deploy more than one application stack in their data center.

Ready? Let's go.

Someone could decide to use an orchestration system, or an SDN controller, or an intent-based product (keep in mind these things do [pretty much the same thing](/2017/09/intent-based-hype.html) but use different names because \$marketing) for a variety of reasons, including:

-   You want to get rid of those [pesky networking engineers](/2016/07/why-is-every-sdn-vendor-bashing.html);
-   You want to do things that nobody in their right mind should be doing, and the \$vendor promised they are really easy to do with their recently-launched [machine-learning-based unicorn dust](/2018/10/worth-watching-machine-learning-in.html);
-   Your \$vendor told you it makes sense to deploy things that nobody knows how to configure correctly (a bunch of [four-letter-acronyms](/2017/09/why-is-cisco-pushing-lisp-in-enterprise.html) comes to mind), and their SDN product supposedly does that (good luck figuring out [what it did when it breaks](/2018/02/how-self-sufficient-do-you-want-to-be.html));
-   You want to give people who don't understand how stuff works tools to [get stuff done](/2018/02/single-image-systems-or-automated.html).

These are all valid reasons and there's nothing wrong with them... but if you answered **YES** to any of the above, please consider outsourcing your infrastructure by moving into a public cloud (see also: [three paths of enterprise IT](/2017/11/the-three-paths-of-enterprise-it.html)).

Still here? How about:

-   You want to increase speed of deployment;
-   You want consistent deployments;
-   You want to make deployments reliable and repeatable.

If you want to reach any of these goals, you should remove the human element from the deployment process. An operator clicking on an SDN GUI will be no more reliable than an operator typing **reload** in the wrong SSH session. The only exception might be an orchestration system that is abstracted enough to take only a few input parameters (example: edge ports and service type) from the operator. SDN products like Cisco ACI are lightyears away from that simplicity (see also: [why do we need an Ansible playbook to collect ACI configuration parameters](/2018/06/automation-win-document-cisco-aci.html)).

Furthermore, if you want to make complex deployments repeatable, you have to use [infrastructure-as-code principles](https://my.ipspace.net/bin/list?id=NetAutSol&module=7) and rely on machine-readable deployment recipes. Expecting a human to consistently follow pages of instructions is insanity.

**To recap**: Even though an SDN product can control 1000s of devices, using a GUI to configure those devices (or services on them) is plain wrong as soon as the operator has to enter more than a few tightly-controlled and validated parameters to deploy the service, and will not give you any substantial benefits... or as I'm always saying: [technology is not a solution, it's just an enabler that allows you to optimize your processes](/2017/10/are-you-solving-right-problem.html).

**Corollary**: If you're running an SDN or next-generation-whatever proof-of-concept without asking the \$vendor engineer demoing the product to [configure everything through an API](/2018/02/anti-automation-from-antimatter-universe.html) you're doing it wrong... and if you don't know which automation or infrastructure-as-code tool you'll use to deploy services on top of that platform, you haven't done your homework.

### If You Need More Information

-   With [Standard ipSpace.net subscription](https://www.ipspace.net/Subscription/Individual) you get access to more than a dozen SDN and network automation webinars;
-   [Expert subscription](https://www.ipspace.net/Subscription/Individual) gives you access to all those webinars plus an [online course](https://www.ipspace.net/Courses) -- choose [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) course to go with your expert subscription.
