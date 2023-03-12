---
date: 2017-09-05 09:08:00+02:00
tags:
- automation
- intent-based networking
- SDN
title: Intent-Based Hype
url: /2017/09/intent-based-hype.html
intent-based-networking_tag: drawback
---
It all started with a realistic response I got to my [*automation and orchestration*](https://blog.ipspace.net/2017/07/automation-or-orchestration.html) blog post (here's a [unicorn-driving-a-DeLorean](http://blog.ipspace.net/2017/07/promises-gone-wild.html) one in case you missed it):

> Maybe you could also add the "intent-based network" which is also not so far from orchestration?

It got me thinking. The way I understand *intent-based* whatever, it's an approach where I tell a system what I want it to do, not how to do it.
<!--more-->
### A Bit of History

Before I even start: if you believe that *intent-based* whatever means the controller will guess what you want to do without you being able to specify precisely what it is, you clearly missed the [Fifth Generation Programming Language](https://en.wikipedia.org/wiki/Fifth-generation_programming_language) hype.

I don't blame you; [that hype peaked in 1980s](#Common_misconception)... proving yet again [Rule 11](https://tools.ietf.org/html/rfc1925).

### What Is Intent?

Now think about the way we configure network devices. Do you tell them *how* to do things, or do you just tell them *what* you want them to do? When you configure OSPF on an interface, do you really tell the box *how* to discover neighbors or just *what* you want it to do (figure out if there are any neighbors on that interface and exchange information with them)?

When I started going down that route the engineer who sent me the initial remark tried to be helpful (we were both struggling at this point to figure out whether we're dealing with something real or pure marketing hype). He started with:

> I think the result is "multi-devices configuration"

As anyone watching my [Network Automation 101 webinar](http://www.ipspace.net/Network_Automation_101) or attending the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) course knows I totally agree that dealing with network devices on a box-by-box basis is wrong and that we should look at the network as a whole and then derive device configurations from network-wide data model.

Obviously, I'm not the only one thinking along these lines. Dinesh Dutt (Cumulus Networks) and David Barroso (Fastly) described the same ideas in their parts of [Network Automation Use Cases](http://www.ipspace.net/Network_Automation_Use_Cases) webinar.

However, coming back to the basics: how is "multi-device configuration" different from Juniper's QFabric, or using a single ginormous box to build your network?

### A Down-to-Earth Definition

David Barroso came up with a good definition in an email exchange:

> Intent: I want vlans 10, 20 in my network device.
>
> Imperative: Configure vlan 10, remove vlan 11, configure vlan 20, remove vlan 21, 30, 40 and pray.

You probably know that David [got so frustrated dealing with so many broken devices](https://blog.ipspace.net/2015/06/napalm-integrating-ansible-with-network.html) that cannot take new configuration and apply it the way we handle configuration changes in Linux world where we usually just reload the server that he [started the NAPALM project to deal with it](http://blog.ipspace.net/2016/10/napalm-update-on-software-gone-wild.html)... and got infinitely more exposure to the network device brokenness than he would have had otherwise.

Is intent-based networking just the capability to apply new device configuration without worrying how to get from the old to the new one? That would make sense, but it's not flashy enough for vendor marketing.

### It's All about the Policy

Next attempt in the *automation vs. orchestration* discussion I mentioned in the beginning of the blog post.

> Maybe I'm wrong but my understanding is that the main difference is to use a "policy model" which is abstracting the classical network constructs. Of course, state of the network, automation, remediation or other assurance stuff still there but everything is "policy centric".

I still fail to see how that's different from configuring OSPF on all interfaces ;) After all, that's my routing policy. Likewise, isn't my ACL expression of my security policy?

### Or Maybe It's All about Abstraction Layers

Before you start telling me how stupid I am not to appreciate all the wizardry done by whatever startup... I agree we're doing lots of things at the wrong level of abstraction, I've been preaching the need for automation and network-centric (as opposed to device-centric) data models, and I agree that an end-user shouldn't know about VLANs when all she needs is connectivity between two VMs.

But seriously, I still think calling that *intent-based networking* instead of what it really is (a different, not necessarily better abstraction model) is a lot of meaningless marketing BS. Unfortunately, we'll likely be stuck with it like we are with *software-defined whatever*.

### What Could Possibly Go Wrong?

Every time someone adds yet another layer of abstraction, it reminds me of RFC 1925 rule 6 and 6a:

> \(6\) It is easier to move a problem around (for example, by moving the problem to a different part of the overall network architecture) than it is to solve it.\
> (6a) (corollary). It is always possible to add another level of indirection.

There's also the [Law of Leaky Abstractions](https://en.wikipedia.org/wiki/Leaky_abstraction), which will definitely bite you (intentionally or otherwise).

Every time someone claims their solution will reduce the complexity of whatever, I start thinking about [squashed complexity sausage](https://blog.ipspace.net/2012/07/virtualized-squashed-complexity-sausage.html).

And every time someone tells me about an umbrella system that will tie together disparate systems, [I hear lock-in](https://blog.ipspace.net/2015/01/lock-in-is-inevitable-get-used-to-it.html).

Then there's lack of standards. Somehow you have to communicate with the wonderful intent-based system (whatever it really is). Will you use GUI to do that? I wish you luck. Will you use an API? Is it standardized? Hint: no.

And finally, today you're complaining that the network devices do only what vendors want them to do. Tomorrow you'll be complaining that you can only express intent the vendors thought you might want to express, and that it got implemented in the way the vendors thought it might be implemented, not the way you want to see it work. The more things change, the more they stay the same.

### Still Not Enough?

Here are a few interesting blog posts I collected on this topic:

-   Russ White has [mostly the same reservations](https://rule11.tech/is-intent-all-that/) I do (if only he would write them down, so I could read his thoughts in 5 minutes instead of listening to him speak for 15);
-   Terry Slattery is a [bit more optimistic](https://www.netcraftsmen.com/cisco-live-2017-simplifying-the-network/);
-   Andrew Lerner is yet again [trying to introduce some order into the marketing mess created by the vendors](http://blogs.gartner.com/andrew-lerner/2017/07/11/intent-based-networking-faq/).

I also covered [intent-based networking](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) details in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
