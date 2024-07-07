---
cli_tag: real
date: 2018-05-10 08:03:00+02:00
intent-based-networking_tag: drawback
series:
- cli
tags:
- automation
- intent-based networking
title: Layers of Single-Pane-of-Glass Abstractions Won’t Solve Your Problems
url: /2018/05/layers-of-single-pane-of-glass/
---
*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. [Subscribe here](http://www.ipspace.net/Subscribe/Five_SDN_Tips).*

We've been told for years how we're over-complicating networking, and how the software-defined or intent-based whatever will remove all that complexity and remove the need for networking engineers.

What never ceases to amaze me is how all these software-defined systems are demonstrated: each one has a fancy GUI that looks great in PowerPoint and might even work in practice assuming you're doing exactly what they demonstrated... trying to be creative could result in interesting disasters.
<!--more-->
But is a GUI on top of an abstraction layer really what we need? I always thought that the problem we were trying to solve was to deliver services faster through self-service portals, or to deploy applications faster and more consistently.

Now take a closer look at the GUI layer offered by the SDN platforms like Cisco ACI or VMware NSX, or most intent-based systems. Is it really aimed at the end-users provisioning their own service, or is it suited for network administrators configuring the network with mouse instead of keyboard? If so, what have we gained?

{{<note>}}Please note I'm talking about service provisioning. Having a GUI-based service-focused monitoring and troubleshooting system instead of today's device-focused single pane of glass is a major step in the right direction, and some vendors are getting there.{{</note>}}

How about faster and more consistent application provisioning? Will we really provision them more consistently if we handcraft environment for individual applications using mouse instead of keyboard? What we really need is an automated deployment process that takes a deployment recipe and executes a series of API calls to consistently provision the exact same environment every time it's executed.

**Long story short**: whenever you're evaluating new technologies or architectures, try to figure out what business (not technology) problem you're really trying to solve, and whether the new shiny thing solves it or introduces another distracting layer of abstraction.

Unfortunately the networking engineers often don't think in these terms -- that's why I included [Collecting the Requirements](http://nextgendc.ipspace.net/Public:1-Collecting_the_Requirements) section in [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course and [Putting It All Together](http://automation.ipspace.net/Public:6-Putting_It_All_Together) section in [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course.
