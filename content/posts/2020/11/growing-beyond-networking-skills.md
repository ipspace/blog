---
title: "Growing Beyond Networking Skills"
date: 2020-11-25 07:09:00
tags: [ certifications, training ]
---
One of my subscribers trying to figure out how to improve his career choices sent me this question:

> I am Sr. Network Engineer with 12+ Years’ experience. I was quit happy with my networking skills but will all the recent changes I'm confused. I am not able to understand what are the key skills I should learn as a network engineer to keep myself demandable.

Before reading the rest of this blog post, please read _[Cloud and the Three IT Geographies](http://www.it20.info/2012/09/cloud-and-the-three-it-geographies-silicon-valley-us-and-rest-of-the-world/)_ by Massimo Re Ferre.
<!--more-->
Got the message? What I (or anyone else) am telling you might **not** apply to your environment. Also, you have to figure out whether you want to work for a vendor, a system integrator, a startup, or an end customer. They are looking for vastly different skillsets. For example, an end-customer might need someone to build a new data center fabric, while a startup might not be interested in anyone not fluent in Python and eBPF.

Finally, you might be making [short-term or long-term plans](/2008/11/sometimes-path-is-more-important-than/), and long-term plans might include migrating to a more forward-looking geography.

If you're looking for a short-term fix, the best thing you could do is look around: figure out what potential employers in your environment are looking for, and get those skills.

Long-term I see at least three interesting areas:

**Networking in public clouds**. While every slide deck promoting unicorn dust claims there's no need to understand networking to deploy stuff in public cloud (or you could use their canned unicorn farts to get it done), the reality is a bit different. 

Just because you're running in an [alternate universe on someone else's computer](/2020/05/aws-networking-101/), you're still using subnets, ACLs, routing tables, VPNs, BGP, NAT, load balancers, DNS, anycast... and [guess who knows how that stuff works](/2019/12/you-still-need-networking-engineer-for/) ;)

**Network automation**. Some end-customers might not be ready to deploy their core workloads in the clouds, but most everyone big enough should be interested in reducing errors in their operations and increasing speed of services deployment... or you REALLY don't want to work for them. 

Making network automation even more attractive (from career perspective) is our propensity for snowflake networks. As long as every network is different, there won't be a magic box you can use to automate them all (regardless of what stupidities vendors put into their slide decks)... at least not without heavy customization.

**Linux networking**. Software-based switching [won't ever replace ASICs](/2020/10/network-operating-systems-qa-part-2/), but a vast majority of network devices used software-based switching for as long as I know (hint: what do you think is powering your home router?), and it's reasonable to get way beyond gigabit speeds on x86 hardware these days.

Also, more and more network devices use Linux as the underlying operating system, and some vendors (Arista, NVIDIA, to a lesser extent Juniper and Cisco) allow you to install your own software directly on the network devices. Understanding how to do either of these things can't hurt, can it?

**Data centers and virtual networking** (like VMware NSX) skills will be highly marketable for a long time in some geographies (but so is COBOL programming knowledge). You might decide to start here if you want a [gradual change in what you're doing](/2015/01/should-i-go-for-ccde-or-vcix-nv/) as opposed to doing something a bit more radical like Linux networking.

However, you have to be careful how you approach the [next S-curve in your career](/2016/02/full-stacks-and-s-curves/). Here's what my subscriber sent me on his approach to mastering network automation:

> I have learned Python to gain network automation skill. Currently I am at beginner+  level in this skill.

NO. NO. NO... **** NO!

You do NOT gain network automation skills by learning Python. [You don't even have to have programming skills](/2016/12/you-dont-need-programming-skills-to/) to do some basic automation. What you do need is the [understanding of network automation fundamentals](/2017/09/start-your-network-automation-journey/) which have absolutely nothing to do with Python. After all, if you want to become a tax advisor after being an accountant for the last decade, learning Excel macros wouldn't be your first step on that journey.

Also, keep in mind that after investing more than a decade into learning somewhat rare and valuable skills, you want to put them to good use and [benefit from the magic of compound interest](/2015/08/how-did-you-learn-so-much-about/), not compete with kids fresh out of high school. There are dozens of Python coders for every VLAN-provisioning CLI jockey out there.

Start your network automation journey from "_I have a challenge I want to solve_" perspective. Figure out the workflow you're trying to automate, simplify it as much as possible, search for the simplest possible tools that could be used to implement the workflow (even though [I hate its limitations](/2019/09/beware-marketing-magic-of-gui-based/), Ansible might not be a bad idea), ideally [hand it off to a team of professionals (= software developers) once you get the proof-of-concept off the ground](/2016/09/how-do-i-persuade-my-management/), and find the next challenge to solve.

You could do all that on your own (there are tons of free resources scattered across the Internet), master fundamentals and get tool deep dives with [ipSpace.net automation webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars), or get a [mentored guided tour with our automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) that already helped hundreds of networking engineers [automate their networks](https://www.ipspace.net/NetAutSol/Solutions). The choice is yours -- you have to find your own time/money balance. 

You have the same set of choices if you decide to go for:

* Cloud networking: [webinars](https://www.ipspace.net/Cloud), [online course](https://www.ipspace.net/PubCloud/)
* Data center technologies: [webinars](https://www.ipspace.net/Roadmap/Data_center_webinars), [online course](https://www.ipspace.net/Building_Next-Generation_Data_Center)

We don't have a similar comprehensive set of materials covering Linux networking yet, but we're working on it ;)
