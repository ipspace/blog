---
cli_tag: real
date: 2018-02-22 13:26:00+01:00
series:
- cli
tags:
- automation
title: Big Red Button for Network Automation
url: /2018/02/big-red-button-for-network-automation.html
---
A while ago I was enjoying a few beers with a longtime friend of mine who happens to be running the networking team for one of the rare companies that understands how infrastructure should be built and operated.

Of course, I had to ask him what he thinks about the imminent death of CLI and all-encompassing automatic provisioning from some central orchestration system. Here's the gist of his response:
<!--more-->
> Here's the funny thing: when you have a network-down situation, you need to figure out what's going on and fix it as soon as possible. It doesn't matter whether it's a vendor bug or an orchestration system bug, you do whatever needs to be done to get the network running... and in many cases the only way to do it fast enough is via CLI.

Obviously once you figure out what the problem was and what workaround you could use (assuming there's one), you have to stop the automation system from continuously resetting your configuration to known state (which you know by now results in a network meltdown).

There are two ways to do it:

-   You have a mechanism to [automate exceptions](https://blog.ipspace.net/2016/07/automate-exceptions.html) -- per tenant, interface, box, site, network... ideally all of the above;
-   You have a big red button that stops the automation and keeps the network running in its current state until the programmers adjust their code or templates to deal with the new reality.

It doesn't matter which approach you take -- as long as you don't count on [crying "*Wilma!!!*"](https://youtu.be/GJu8RreAGnM?t=33s) after locking yourself out of your network.

### Want to Know More?

We'll have fun discussing these topics (and things like [*intent-based whatever*](https://blog.ipspace.net/2017/09/intent-based-hype.html)) in [Building Network Automation Solutions online course](http://www.ipspace.net/Building_Network_Automation_Solutions).

### Speaking of Red Buttons

This is the first big red button I've seen in my life when I was punching cards during my high-school years. It was sitting on an IBM/360 with 48K of core memory and fridge-size 5MB disk drives. The urge to pull it was almost irresistible.

{{<figure src="https://i1.wp.com/www.retroist.com/wp-content/uploads/2016/03/emergency-pull.jpg?fit=750%2C422&ssl=1">}}

### Before You Tell Me...

As is often the case, I'm simplifying things.

There are platforms where you can do (almost) anything you can configure on individual boxes with the centralized GUI. vCenter comes to mind, but even there you need ESXi CLI to configure the nerd knobs.

In those cases, you might think you don't need the big red button... until you change ESXi virtual switch parameters in a way that breaks connectivity between vCenter and ESXi host (more about that in [vSphere Networking Deep Dive webinar](http://www.ipspace.net/VSphere_6_Networking_Deep_Dive)). Anyone who's been configuring ACLs on any networking device without **commit** capabilities should be very familiar with this concept... and the big red button is usually called **reload in 5.**

However, those are the trivial cases. In any system that provides any meaningful level of abstraction you won't be able to control the exact settings on the controlled devices (or there would be no level of abstraction), making the big red button even more important.

*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. [Subscribe here](http://www.ipspace.net/Subscribe/Five_SDN_Tips).*
