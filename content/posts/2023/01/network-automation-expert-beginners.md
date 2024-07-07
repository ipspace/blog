---
title: "Network Automation Expert Beginners"
date: 2023-01-17 07:33:00
tags: [ automation ]
---
Some network automation skeptics came to that place the hard way: they got burned by half-baked semi-tested systems. This is what one of my good friends had to say in a LinkedIn comment:

> I am suspicious of automation, as I've unfortunately seen too many outages caused by either human error or faulty automation. Every time it required human CLI/GUI intervention to correct it. The problem is that the more automation we push, the fewer people know how to use the "old school" way to administer stuff.

Network automation is not the only IT discipline that could cause hard-to-correct errors requiring manual intervention. I'm positive everyone knows at least one horror story resulting in manual tweaking of the Windows registry, or a sequence of arcane SQL commands[^DT].
<!--more-->
[^DT]: Or hours of downtime anxiously waiting for the database to be restored from backup tapes.

However, one would expect that catastrophic outages would be rare and one-off events -- after all, we've been developing software for decades, and we should have learned a few lessons along the way. Concepts like version control, transactions, thorough testing, and input validation are considered table stakes for serious software development organizations. Unfortunately, that's not how the pundits were selling network automation benefits to the networking engineers eager to get out of the manual configuration quagmire.

As every software engineer or architect worth their salary knows, one should start with (at least) the following:

* **Requirements:** what should the solution do? What services do we plan to automate? Who are the expected end-users? What can we expect from them?
* **Data structures:** how will we describe the services we're planning to automate? What are the relations between objects in our data model? What integrity rules should we keep in mind?
* **Overall architecture:** Where will we store the data? How will the user interface look? How will we interact with the network devices? How will we recover from inevitable failures?
* **Business logic:** What needs to be done? How will we get from the current state of the network to the desired final state?
* **Testing plan:** How will we test our solution? How will we make sure the tests are relevant? How will we minimize the deployment risks? 

Also, nobody in their right mind would not validate inputs to a mission-critical application[^NAC] or deploy new code in production without thorough testing. Some application would go as far as checking the status of executed actions and [roll back on errors](/2019/04/recovering-from-network-automation/)[^BA] -- something that is sorely missing in way too many home-grown network automation solutions.

[^NAC]: Considering the role of networking in modern IT infrastructure, one might argue that any read/write network automation is by default a mission-critical application.

[^BA]: You wouldn't want to have money taken out of your bank account and disappear because the target account of your payment request does not exist, would you?

I've seen organizations that approached network automation like any other software development project, combining networking engineers (the expert users) with software developers. Some of these projects had astonishing results, but you rarely hear about them -- people working on those projects have better things to do than to deliver unpaid presentations at conferences[^RD].

[^RD]: Unless they work for a major technology vendor that uses technical conferences as recruitment drives.

Instead, we got a deluge of blog posts, podcasts, and conference talks explaining how easy it is to automate your network if only you embrace the "_we all have to become Python programmers_" mantra or master Ansible. Instead of an in-depth discussion of architectures, data structures, software development methodologies, and challenges of modifying the state of a distributed system, those motivational talks often resulted in a cargo cult of [expert beginners](/2013/05/expert-beginners/) focused on low-level tools. Unsurprisingly, a quick "_Ansible is so easy to use_" talk followed by a glitzy demo is always sexier than "_these are the five mandatory steps you should take before you can start automating your network._"

The situation is getting a bit better since the days I started talking about these concepts in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course. Network-to-Code occasionally publishes a [blog post focused on automation concepts or architectures](https://blog.networktocode.com/post/network-automation-architecture-part-03/)[^NSD], Anton Karneliuk seems to have a [sound curriculum](https://karneliuk.com/2022/12/tips-for-network-engineers-willing-to-transit-to-network-automation/), and every now and then someone describes how to use NetBox (or a similar tool) in an automation solution to create the source of truth. However, it's still common to see YAML files or Excel spreadsheets used together with Ansible playbooks in "production-grade" automation solutions.

[^NSD]: No surprise there -- they run a consulting practice and have to set the expectations if they want their projects to be successful.

Don't get me wrong, I'm not saying you cannot start automating network operations until you built a full-blown system with CLI, API and GUI on top of a relational database. If you need a quick solution that will grab some data from the network devices and create a report or a graph, go for it. If you need a tool that will help you troubleshoot the network, write it. You can't do too much harm if you're executing read-only commands from an account that has no device configuration privileges[^CRS].

[^CRS]: Hoping that the days of shoddy software that would crash when faced with rapid SNMP polling or a barrage of **show** commands are long gone.

Also, if you have to build a proof-of-concept to persuade your management that it makes sense to automate service deployment, don't waste your time on integration with a transactional data store. YAML files are good enough for the minimum viable demo. It's also OK to continue using that approach in a small team, assuming you use version control to track the changes to the data model, and thoroughly review all the changes before they're promoted into production. Some people found that they [don't need more than GitOps](/2018/08/gitops-in-networking/), and that's perfectly fine as long as you know what you're doing and what the risks and limitations of that approach are.

However, once you get the approval to build a production solution that will be used by non-experts (including members of other IT teams), you must start using better tools. Using Ansible Tower as the GUI sitting in front of Ansible playbooks controlled with external variables will quickly get you to the point where you'll start blaming your users for entering incorrect data. In reality, you should blame yourself for choosing suboptimal tools and not validating the input data in the first place.

**Long story short**: don't blame network automation if a script that someone hacked over a weekend for personal use got adopted as a company-wide "automation solution." Even AWS got burned when [someone failed to implement input sanity checks in one of their automation playbooks](https://aws.amazon.com/message/41926/).

### Revision History

2023-01-11
: David Gee and Cristian Sirbu provided extensive feedback that made this blog post much better than the original draft (all the errors and the snark are still mine 😉) Thanks a million!
