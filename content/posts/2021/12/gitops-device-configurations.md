---
title: "Checking Network Device Configurations in a GitOps CI Pipeline"
date: 2021-12-14 07:54:00
tags: [ automation ]
series: [ cicd ]
cicd_tag: testing
---
Here's a fun fact network automation pundits don't want to hear: if you're working with [replaceable device configurations](/2016/10/network-automation-rfp-requirements/) (as we did for the past 20 years, at least those fortunate enough to buy Junos), you already meet the [Infrastructure-as-Code](https://en.wikipedia.org/wiki/Infrastructure_as_code) requirements. [Storing device configurations in a version control system](/2018/08/gitops-in-networking/) and using reviews and merge requests to change them (aka GitOps) is just a cherry on the cake.

When I [made a claim along these same lines](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) a few weeks ago during the _[Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts)_ webinar, [Vladimir Troitskiy](https://www.linkedin.com/in/vldmtr/) sent me an interesting question:
<!--more-->
> I see some kind of a problem with the 'GitOps and config replace' approach. Let's assume you have a network device that is able to replace its configuration only all at once. Obviously, at the early automation stages, you don't have a full-blown data model to generate the full config of the device from scratch. So the best you can do in GitOps-style is to fork this text file, edit it with a text editor and merge it back. As you don't have a built-in CLI help and your input isn't validated, you can only hope the result is a valid config and the device won't choke with it during the replacement.

There are a few tricks you can use in that case (for more details, follow the links in [this blog post](/2018/08/gitops-in-networking/), I created tons of materials on the topic a few years ago):

**Limit the changes an operator can make**. Compare the changes made in a commit to a valid list of commands this operator can use and reject anything that is not allowed. For example, a server administrator can only add **switchport trunk allowed vlan** commands to server-facing ports on data center switches.

**Check the command syntax**. Suppose you limit the changes an operator can make. In that case, it's easy to write a simple validation script that will check the syntax and the parameters of the few allowed commands (including _do we have **add** keyword in that **switchport** command?_).

**Do sanity checks**. For example, is the configuration using ACLs that are never defined? Are there services that should not be enabled (like HTTP server)? [netlint](https://netlint.readthedocs.io/en/latest/) by [Leo Kirchner](https://blog.kirchne.red/) is a sample tool that you could use to get started; if you know a better tool please write a comment. 

**Require manual approvals** for all changes beyond the pre-approved list of commands.

**Use a static configuration analysis tool** like *Batfish*. It can't go beyond the usual SNAFUs if you haven't done your homework (written "expected network behavior" tests), but every little bit helps.

**Use actual devices in pre-deployment tests**. Numerous networking devices have configuration difference tools. Some of them (Junos, EOS) have *candidate configuration* -- an excellent way to push the proposed changes *to the actual device* and ask it whether it feels comfortable with them.

Bonus points if you add the **config diff** command output as a comment to the merge/pull request.

**Use automated post-deployment tests**. They are a chore to write but could be a life-saver, particularly if you could run them before confirming the configuration change (making sure an automated rollback kicks in if you managed to brick your network).

**Don't expect to make perfect complex configuration changes**. I hope you're not trying to implement complex configuration changes by typing random commands into your network devices today. You'd usually plan the exact sequence of commands in advance, schedule a maintenance window, and carefully execute them. What's stopping you from doing the same with Git?

What if you have to adjust the configuration change based on how much your plan deviates from reality? No problem:

* Fix the problem when rolling out the change. It makes no sense to go through a Git repository -- the network is broken anyway, and you can always roll back to a working configuration.
* Commit the final configurations back into your Git repository;
* Write a long commit message explaining what went wrong;
* Submit them as another merge/pull request.

The workflow is explained in  *‌[Manage Network Device Configurations with Git](https://my.ipspace.net/bin/list?id=NetAutSol&module=2#M2S2B)* part of _[Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions)_ online course).

Bonus point: you have a history of changes, so it's easy to roll back from a botched change even if the problems pop up a week later.

Anything else? Please write a comment.
