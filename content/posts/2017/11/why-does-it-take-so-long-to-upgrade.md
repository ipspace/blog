---
date: 2017-11-20 07:59:00+01:00
tags:
- automation
title: Why Does It Take So Long to Upgrade Network Devices?
url: /2017/11/why-does-it-take-so-long-to-upgrade.html
---
One of my readers sent me a question about his favorite annoyance:

> During my long practice, I've never seen an Enterprise successfully managing the network device software upgrade/patching cycles. It seems like nothing changed in the last 20 years - despite technical progress, in still takes years (not months) to refresh software in your network.

There are two aspects to this:
<!--more-->
-   Why does it take so long to validate a new software release, and why are they still monolithic blobs, and why are they always full of fresh bugs? Let's postpone this one for another blog post ;), in the meantime read [this blog post](http://gestaltit.com/exclusive/tom/vendors-vars-enemy) by Tom Hollingsworth (in particular the *I Feel the Need for Speed* section).
-   Why does it take so long to roll out new software?

The second aspect is entirely our fault. We were so keen on being CLI heroes that we ignored what was happening around us. The leading $vendor having ancient software that can barely spell API and never got _configuration commit_ capability didn't help either -- the code base for their enterprise routing platform is almost four decades old, and their switching platform [got configure replace in 2017](/2017/11/update-cisco-nexus-switches.html).

Well, not everyone did the same mistake. I know people who roll out software upgrades with automated scripts ([here are a few ideas](/2017/08/upgrade-network-device-software-with.html) to get you started). I've also heard of people who bricked hundreds of routers because of insufficient checks and lack of [gradual rollout](https://networkingnerd.net/2016/04/20/automating-change-with-help-from-fibonacci/).

I know people who vote with their wallet and buy products that [support automation](/2016/10/network-automation-rfp-requirements.html). You can buy a router, a switch, a firewall, and (probably) a load balancer that had full support for automation for years if not decades from a major vendor for a reasonable price these days... but as long as everyone keeps buying what they've been buying for decades we won't move anywhere. It's like we would continue buying hierarchical databases like IBM IMS instead of using MySQL or whatever other variant of modern relational database (but wait... there are people [talking about migrating mainframe applications to AWS](https://medium.com/aws-enterprise-collection/yes-you-can-migrate-your-mainframe-to-the-cloud-92df0277d1ac)).

Anyway, until we can automate our stuff, and prove that it works, we won't move forward. Imagine bank tellers [having to do transactions by typing SQL INSERT/UPDATE queries directly into production database](/2019/05/stop-low-level-configuration.html) that has no rollback/commit capability. I doubt they would move any faster than we do.

Unfortunately, most of networking engineers don't even want to admit they have a problem. I never cease to be amazed at how disinterested some enterprise networking engineers are about network automation. Looks like they barely entered the denial phase of grief while everyone else is passing them by left and right.

If you're not one of them, but simply don't know where to start, check out [ipSpace.net Network Automation webinars](http://www.ipspace.net/Roadmap/Network_Automation_webinars). If you're focused more on solutions and architectures, go for the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) course.

However, before yammering about the sad state of networking, let's see what everyone else is doing. There are medical systems running on Windows XP, Equifax needed months to patch critical vulnerability, there are tons of environments where servers are never patched because they run mission-critical apps. Doesn't mean that we can't or shouldn't do better (we definitely should), only that we're not the only losers in IT.
