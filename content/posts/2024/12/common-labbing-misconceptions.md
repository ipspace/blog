---
title: "Configuring IP Addresses Won't Make You an Expert"
date: 2024-12-16 06:39:00+0100
tags: [ netlab ]
netlab_tag: overview
---
A friend of mine recently wrote a nice post explaining how _netlab_ helped him set up a large network topology in a reasonably short timeframe. As expected, his post attracted a wide variety of comments, from "_netlab_ is a gamechanger" (thank you 😎) to "I prefer traditional labs." Instead of writing a bunch of replies into a walled-garden ecosystem, I decided to address some of those concerns in a public place.

Let's start with:
<!--more-->
> I thought that the point of setting up a lab is to learn the “how” to set it up and do packet captures when you make mistakes, so you know what went wrong and what it looks like when it goes wrong.

That's absolutely correct, and I do the same when trying out new stuff. However, I want to focus on the things I don't know, not on those I've been doing for 35 years, like enabling interfaces, configuring IP addresses, and assigning OSPF areas to interfaces. Supposedly, you need 10.000 hours of practice to become an expert, but I can tell you that nobody became an expert by configuring IP addresses for 10.000 hours. Getting rid of the boring stuff and focusing on what makes you a more experienced engineer is one of the main reasons I started developing netlab.

> I tend to reuse labs, so I don’t have to reinvent the wheel for every new lab. Once you have a few past labs, you can do almost anything with them.

That's what I've been doing in the past, and I hated it every time I had to do it. Either the topology was slightly off, the routing protocols weren't configured how I wanted them to be set up, or the AS numbers were wrong. You get the idea ;) Also, I often spent more time troubleshooting why my changes to the old topology did not work than testing new stuff.

You might call that learning. For me, the root cause of wasting time fixing old stuff was a lack of focus. As I don't have to implement ad-hoc changes on a production network in the middle of the day, mastering the art of making zero mistakes doesn't help much. OTOH, if you have to tweak running networks with surgical precision[^PYR], adapting the old lab topologies to new use cases might be precisely what you need.

[^PYR]: In this case, I strongly recommend you polish your resume and start looking for other opportunities.

_netlab_ allows me to create entirely new topologies in minutes. Besides getting the high-level details wrong (which is easy to fix if you use fast-starting containers), the networks created by _netlab_ work every time, primarily due to the [intensive integration testing](https://release.netlab.tools/) we do on [device configuration templates](https://blog.ipspace.net/2024/05/netlab-integration-tests/).

> Container labs take forever to start.

Opinions are great, facts are better. Let's go through them.

You can run network devices as *virtual machines*, *pure containers*, or *virtual machines inside containers* (the *vrnetlab* project).

Virtual machines take as long as they take to boot, from seconds (Linux, Cumulus Linux, VyOS) to the time it takes to [prepare a sandwich](https://xkcd.com/149/) (I won't name any names, but the major networking vendors are the biggest offenders). Virtual machines inside the containers take approximately the same time (aka "there's no magic").

"Native" containers always boot faster than corresponding virtual machines because they don't have to boot Linux first. For example, the Arista cEOS container starts faster than the Arista vEOS virtual machine.

I [measured the VM and container boot times](/2023/02/virtual-device-boot-times/) a while ago. I'm positive things have improved in the meantime (if nothing else, we have slightly faster CPUs), but I don't expect IOS XR to boot faster than VyOS any time soon.

Finally:

> How is netlab different from CML

Ignoring the "GUI versus infrastructure-as-code" conceptual differences, I was told that CML no longer includes _Autonetkit_, which means you must do most of your device configuration from scratch, like with GNS3 or EVE-NG (as opposed to getting a ready-to-run network with _netlab, see above for details).

If you know more, please leave a comment.
