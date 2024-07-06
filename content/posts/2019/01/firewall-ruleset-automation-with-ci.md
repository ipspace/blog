---
cicd_tag: solution
date: 2019-01-11 08:38:00+01:00
series:
- cicd
tags:
- automation
- firewall
title: Firewall Ruleset Automation with CI Pipeline
url: /2019/01/firewall-ruleset-automation-with-ci.html
---
One of my readers sent me a description of their automation system that manages firewall rulesets on Fortigate firewalls [using NAPALM to manage device configurations](https://my.ipspace.net/bin/list?id=Ansible#NAPALM).

In his own words:

> We are now managing thousands of address objects, services and firewall policies using David Barroso's FortiOS Napalm module. This works very well and with a few caveats (such as finding a way to enforce the ordering of firewall policies) we are able to manage all the configuration of our firewalls from a single Ansible playbook.

The did the right thing and implemented an abstracted data model using [GitOps](/2018/08/gitops-in-networking.html) to manage it:
<!--more-->
> We manage our Ansible code in git using an on-premises git repository system. We have YAML documents that describe firewall objects (addresses, subnets, groups), services, and policies We transform these data structures into firewall configurations using Jinja2 templates.

Does that mean that everyone has to learn git? Not really...

> When a network engineer wants to make a change to a firewall's policy, she edits the corresponding YAML file that describes the configuration. No knowledge of git is required, because the engineer can just edit the file from the web UI in our git repository.

So far so good. Now for the really cool part: the CI pipeline:

---

Once the changes are saved, the tooling around our git repository system automatically puts them in a new branch and generates a pull request.

At this point, a git hook will execute a custom script that validates the YAML configuration. The beauty of having our firewalls' configuration in YAML format is that this is very easy to manage with Python or PowerShell scripts. For example, our validation script analyses the firewall rules and identifies "dangerous" policies, such as those that allow access to unsecure services on the Internet, or raises an alert for Internet-facing services that have no logging and no IPS enabled.

The validation script produces a report in text format which flags all the issues identified in the YAML configuration. The report is added as a comment to the pull request.

After this step, an email is sent automatically to the pull request reviewers. The reviewers can look at the "diff" of the pull request in the same web UI, and read the report produced by the validation script. If the change is approved, a git hook will execute a job in Ansible Tower, which will pull the new configuration from the git repo and run an Ansible playbook to apply the change to the firewall devices.

---
Here's a diagram of the whole process provided by my reader:

{{<figure src="/2019/01/s1600-Firewall+Configuration+Change+Management+Process.png" caption="Firewall configuration change management process">}}

Want to learn how to do something similar? You'll find tons of relevant details in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.
