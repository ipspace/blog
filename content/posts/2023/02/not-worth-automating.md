---
title: "Some Operations Are Not Worth Automating"
date: 2023-02-21 08:06:00
tags: [ automation ]
---
Ish [wrote an interesting comment](/2023/01/network-automation-expert-beginners/#1661) on my [Network Automation Expert Beginners](/2023/01/network-automation-expert-beginners/) blog post. He started with:

> [Our network has] about 40 sites, but we don't do total refresh cycles in bulk, just as needed. Everything we do is sporadic, and I'm trying to see the ROI on learning automation for things that are done once in a while that don't take much time to do manually anyway.

There are two aspects to this part of his comment:
<!--more-->
* Is it worth automating sporadic operations?
* Is it worth learning about network automation?

The latter is easier to answer: if you care about your career growth, you should learn the basics of network automation. Like public clouds, automation is becoming a must-be-aware-of tool, and not having a clue about it might severely limit your job-hunting opportunities. Do yourself a favor, figure out what it's all about, and make sure you won't stop at the Expert Beginner "_writing Ansible playbooks or Python scripts_" phase. Do I have to mention that you'll find plenty of relevant webinars and an [online course](https://www.ipspace.net/Building_Network_Automation_Solutions) on ipSpace.net?

Now for the more ambiguous part: automating sporadic operations. You should always ask yourself, "_how sporadic are they?_" For example: with 40 sites, I'd expect one refresh every month or so. Is that worth automating? Developing a full-blown solution that would roll out a new location on its own doesn't make sense, but having consistent configurations on all sites might be worthwhile. That brings us to another question: assuming device configurations change to fix omissions or introduce new functionality, how do you ensure consistent device configurations on all sites? Who enforces that, and how?

The next usual objection is *[time spent automating things](https://xkcd.com/1319/)*. Back to my reader:

> I can spend 40 hours trying to figure out how to automate something that will only take me 30 minutes and that I will only do ten times a year. Only for nobody to use that same automation method, or for it to become obsolete, or simply need to spend more hours maintaining and updating it.

Trying to evaluate the benefits of automating an operation based on time saved worked great for Henry Ford, but it's the wrong approach in most network automation environments. You should ask yourself:

-   How much will we gain from having consistent deployments?
-   Will we reduce troubleshooting efforts because we won't have bespoke configurations on every device in the network?
-   How much simpler will it be to troubleshoot the network at odd hours, knowing it's configured consistently?
-   Will we increase speed-of-deployment because we won't have to go through numerous "_this doesn't work (again), fix it_" cycles?

Also, stop focusing on configuration deployment. Network automation is much more than that, even though the preachers of the "*take a pinch of YAML, add a sprinkle of Jinja2, and shake well in Ansible shaker*" gospel usually fail to mention it. There must be some repetitive operation that drives you crazy. Automate that! Nothing along those lines? You must be incredibly fortunate, but here's another idea: do you have a repository of device configurations? Is it under version control? Can you figure out who made any particular change on a device you're troubleshooting and why? Do you think that having that information would make your life easier? [Oxidized](https://github.com/ytti/oxidized) might be just what you're looking for. For more ideas, browse the [sample network automation solutions](https://www.ipspace.net/NetAutSol/Solutions) created by the attendees of ipSpace.net [network automation online course](https://www.ipspace.net/Building_Network_Automation_Solutions).

Finally, it's perfectly fine if your network doesn't need automation. I just hope you came to that conclusion after realizing the full potential of network automation and making a well-informed decision. [400 automation-related blog posts](/tag/automation/), a [half-dozen webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars), and an [online course](https://www.ipspace.net/Building_Network_Automation_Solutions) might help you get the prerequisite knowledge.
