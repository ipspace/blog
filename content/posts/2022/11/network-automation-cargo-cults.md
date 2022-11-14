---
title: "Network Automation Cargo Cults"
date: 2022-11-24 07:33:00
tags: [ automation ]
draft: True
---
Some network automation skeptics came to that place the hard way: they got burned by half-baked semi-tested systems. This is what one of my good friends had to say in a LinkedIn comment:

> I am suspicious of automation, as I've unfortunately seen too many outages caused by either human error or faulty automation. Every time it required human CLI/GUI intervention to correct it. The problem is that the more automation we push, the fewer people know how to use the "old school" way to administer stuff.

Network automation is not the only IT discipline that could cause hard-to-correct errors requiring manual intervention. I'm positive everyone knows at least one horror story resulting in the manual tweaking of the Windows registry or a sequence of arcane SQL commands.
<!--more-->
However, one would expect that catastrophic outages would be rare and a one-off event -- after all, we've been developing software for decades, and we should have learned a few lessons along the way. For serious software development organizations, concepts like version control, transactions, and thorough testing are considered table stakes. Unfortunately, that's not how the pundits were selling network automation benefits to the networking engineers eager to get out of the manual configuration quagmire.

As every software engineer or architect worth their salary knows, one should start with (at least) the following:

* **Requirements:** what should the solution do? What services do we plan to automate? Who are the expected end-users? What can we expect from them?
* **Data structures:** how will we describe the services we're planning to automate? What are the relations between objects in our data model? What integrity rules should we keep in mind?
* **Overall architecture:** Where will we store the data? How will the user interface look? How will we interact with the network devices? How will we recover from inevitable failures?

I've seen organizations that approached network automation like any other software development project, combining networking engineers (the expert users) with software developers. Some of these projects had astonishing results, but you rarely hear about them -- people working on those projects have better things to do than to deliver unpaid presentations at conferences[^RD].

[^RD]: Unless they work for a major technology vendor that uses technical conferences as recruitment drives.

Instead, we got a deluge of blog posts, podcasts, and conference talks explaining how easy it is to automate your network if only you embrace the "_we all have to become Python programmers_" mantra or master Ansible. Instead of an in-depth discussion of architectures, data structures, software development methodologies, and challenges of modifying the state of a distributed system, we got a veritable cargo cult focused on low-level tools. Unsurprisingly, a quick "_Ansible is so easy to use_" talk followed by a glitzy demo is always sexier than "_these are the five mandatory steps you should take before you can start automating your network._"

The situation is getting a bit better. Network-to-Code occasionally publishes a blog post focused on the concepts[^NSD], and every now and then, someone describes how to use NetBox (or a similar tool) in an automation solution to create the source of truth. However, it's still common to see YAML files or Excel spreadsheets used together with Ansible playbooks in "production-grade" automation solutions.

[^NSD]: No surprise there -- they run a consulting practice and have to set the expectations if they want their projects to be successful.

Don't get me wrong. If you have to build a proof-of-concept to persuade your management that it makes sense to automate service deployment, don't waste your time on integration with a transactional data store. YAML files are good enough for the minimum viable demo, but when you get the approval to build a production solution, you must start using better tools. Using Ansible Tower as the GUI sitting in front of Ansible playbooks controlled with external variables will quickly get you to the point where you'll start blaming your users for entering incorrect data. In reality, you should blame yourself for not validating the data in the first place.

**Long story short**: don't blame network automation if a script that someone hacked over a weekend for personal use got adopted as a company-wide "automation solution." Even AWS got burned when [someone failed to implement input sanity checks in one of their automation playbooks](https://aws.amazon.com/message/41926/).
