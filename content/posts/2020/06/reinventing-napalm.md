---
title: Building a Multi-Vendor Automation Platform
date: 2020-06-01 08:06:00
tags: [ automation ]
---
One of the attendees in our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course sent me this question:

> While building an automation tool using Python for CLI provisioning, is it a good idea to use SDK provided by device vendor, or use simple SSH libraries Netmiko/Paramiko and build all features (like rollback-on-failure, or error handling, or bulk provisioning) yourself.

The golden rule of software development should be "_don't reinvent the wheel_"... but then maybe you need [tracks](https://en.wikipedia.org/wiki/Continuous_track) to navigate in the mud and all you can get are [racing slicks](https://en.wikipedia.org/wiki/Racing_slick), and it might not make sense to try to force-fit them into your use case, so we're back to "_it depends_".
<!--more-->
{{<note info>}}Nick Buraglio wrote a great blog post [explaining how you should deal with wheels that don't exactly fit your needs](https://forwardingplane.net/2018/02/19/strategy-series-build-vs-buy-sorta/).{{</note>}}

In this particular case, the target was a multi-vendor automation platform:

> I want to support Cisco, Juniper, and Alcatel routers... and build a REST wrapper around my automation.

Based on these goals, one would have to:

* Define the operations the platform provides through REST API (example: deploy configuration, deploy OSPF routing, validate topology...);
* Define REST API calls to perform those operations.
* Implement the same operations for multiple platforms.

Now let's focusing on the last bullet, and the potential gotchas we'd have to deal with:

* Rollback-on-error
* Recovery from botched configuration deployment
* Handling configuration errors

{{<note info>}}I wrote about some of these aspects in a [previous blog post](/2019/04/recovering-from-network-automation.html).{{</note>}}

Faced with a wide variety of target platforms, it's almost impossible to get SDK toolkits that would implement all the required functionality. For example, it's easy to implement rollback-on-error on Junos using its commit/rollback configuration mechanism, and a [lot harder to do it in Cisco IOS](/2017/03/netconf-transactional-consistency-on.html).

Fortunately, someone has solved the multi-vendor configuration management challenges, and it would be a waste not to look at whether [NAPALM](https://my.ipspace.net/bin/list?id=Ansible#NAPALM) (or [NetPalm if you want to have REST API](https://github.com/tbotnz/netpalm)) could provide at least some of the required functionality, potentially at a lower level of abstraction. For example, while NAPALM provides configuration _management_ (merge, replace, rollback), it does not provide configuration _generation_ based on a universal data model... but then maybe you need [ntc-rosetta](https://github.com/networktocode/ntc-rosetta).

As always it comes down to **knowing your tools**: 

* Figure out what problem you're trying to solve;
* Break that problem into smaller components;
* Explore the existing tools... it's rare that you're the first one trying to solve a particular problem;
* Find out whether the existing solutions fit your needs, and adjust your needs if needed;
* At the very least, explore the existing solutions to figure out how they got the job done. For example, the developers of NAPALM spent years dealing with real-life production challenges, and it would be a total waste to ignore that accumulated knowledge.

Oh, and the more tools you're familiar with, the better your tool selection process might be. I'm trying to keep a [list of network automation tools](/kb/Ansible/Useful_Network_Automation_Tools.html) on our web site (additions welcome), and we covered [almost a dozen of them](https://my.ipspace.net/bin/list?id=NetAutSol&module=9) in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course.