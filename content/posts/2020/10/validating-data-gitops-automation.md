---
cicd_tag: testing
date: 2020-10-13 06:31:00+00:00
series:
- cicd
tags:
- automation
title: Validating Data in GitOps-Based Automation
---
Anyone using [text files as a poor man's database](/2019/04/text-files-or-relational-database/) eventually stumbles upon the challenge left as a comment in [Automating Cisco ACI Environments](/2019/03/automating-cisco-aci-environment-with/) blog post:

> The biggest challenge we face is variable preparation and peer review process before committing variables to Git. I'd be particularly interested on how you overcome this challenge?

We spent hours describing potential solutions in _[Validation, Error Handling and Unit Tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5)_ part of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course, but if you never built a network automation solution using Ansible YAML files as source-of-truth the above sentence might sound a lot like Latin, so let's make it today's task to define the problem.
<!--more-->
### Beyond Simple Scripts

Most network engineers start their automation journey with easy wins: [simple scripts that collect information](https://www.ipspace.net/NetAutSol/Solutions#Simple_Reports) from a large set of network devices, or [make sure that all routers use the same set of NTP- or syslog servers](https://www.ipspace.net/NetAutSol/Solutions#Configuration_Consistency).

Once the initial excitement of having your first automation solution in production fades, the next logical step becomes [network- and services deployment](https://www.ipspace.net/NetAutSol/Solutions#Configuration_Consistency), and after a few failed attempts it becomes painfully obvious that you need a [_data model_ describing the whole network](/kb/DataModels/) (or a service) instead of individual boxes. At that point you could usually describe your automation system with this simple diagram[^SOT]:

{{<figure src="/2020/10/Network-Deployment-Diagram.jpg" caption="Typical Network Deployment Automation System">}}

Using templates to generate device configurations (or Terraform recipes or API calls) is well-understood; the next interesting challenge you have to overcome is _where do I store my data model_ (or more formally, what _data store_ do I use) and if you happen to use Ansible as the go-to tool, text files become the obvious choice. 

Sprinkle version control on top of that, add some branching and merging magic and you seem to be in the green meadows of Infrastructure-as-Code (because you're describing your network as a set of YAML files) and [GitOps](/2018/08/gitops-in-networking/) until you realize every data model suffers from GIGO problems.

A typical GitOps workflow (although [focused on managing device configurations not data model changes](https://my.ipspace.net/bin/list?id=NetAutSol&module=2#M2S2B)) is displayed on the following diagram:

{{<figure src="/2020/10/Manage-Configs-GitOps.jpg" caption="Managing Device Configurations with GitOps">}}

The above workflow is missing a crucial step: _are the changes made to the source code any good and should they be accepted?_ That challenge has been solved a gazillion times in software development using approaches like code review, automated testing, and continuous integration... but how do you implement them in a network automation solution?

In fact, you have more on your hands than simple software development project: you have to test _your code_ (templates, playbooks...) and _your data_; in this series of blog posts we'll focus on the latter.

There are tons of things you can do to validate changes to your data model before they get accepted into the production source-of-truth. Here are just a few examples (more in an upcoming blog post):

* Pre-commit hooks[^1] that do basic sanity checks like checking the syntax of YAML files with **yamllint**
* Pre-commit hooks or continuous integration (CI) pipelines[^2] that validate the basic sanity of your data model (for example: are IP addresses in the right format)
* CI pipeline that validates data model against a snapshot of an actual network (for example, checking device- and interface names);
* CI pipeline that builds a simulated version of the whole network, deploys the changes, and runs unit tests on the simulated network;
* Pre-deployment pipeline that collects and reports changes about to be made to device configurations for operator approval.

As I already mentioned, we covered most of these ideas in _[Validation, Error Handling and Unit Tests](https://my.ipspace.net/bin/list?id=NetAutSol&module=5)_ part of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course; I plan to cover at least a few of them in upcoming blog posts, but you know that it typically takes a while before I find time to do that, so if you're serious about implementing guardrails for your automation solution you might be better off [enrolling into the course](https://www.ipspace.net/Building_Network_Automation_Solutions#register).

[^SOT]: The diagram was created in 2015 before it became popular to talk about _single source-of-truth_. Today I would use that hip term instead of _network parameters database_.
[^1]: Programs executed before you're allowed to commit your changes to local copy of Git repository
[^2]: Programs executed every time someone pushes a branch to the central Git repository