---
date: 2014-09-02 08:12:00+02:00
tags:
- SDN
title: Network Infrastructure as Database
series: [ niac ]
niac_tag: implement
url: /2014/09/network-infrastructure-as-database.html
---
A while ago I wrote about the idea of [treating network infrastructure (and all other infrastructure) as code](/2014/06/infrastructure-as-code-actually-makes.html), and using the same processes application developers are using to write, test and deploy code to design and implement networks.

That approach clearly works well if you can virtualize (and clone ad infinitum) everything. We can virtualize appliances or even routers, but installed equipment and high-speed physical infrastructure remain somewhat resistant to that idea. We need a different paradigm, and the best analogy I could come up with is a database.
<!--more-->
Imagine an organization that needs a large transactional database to run its business, and requires the frontline operators to modify data in that database with SQL statements (INSERT, UPDATE, DELETE). I haven't heard of anyone being even remotely that stupid -- and yet that's how most of us run our networks. Time to take another lesson from application development world.

It's obvious that one should interact with a production database only through well-defined and thoroughly tested transactions (whether you call them [transactions](http://en.wikipedia.org/wiki/CICS), application programs or web scripts is irrelevant). Direct CLI (SQL) access to the database should be either prohibited or limited to the absolute minimum.

Likewise, we should make changes to our network devices with well-defined transactions (example: *CREATE VLAN* or *REMOVE VLAN*). These transactions (call them scripts, playbooks or recipes if you wish) should be treated like any application code, and tested in a lab environment before being allowed to touch the production network.

And now for the usual set of objections:

**But I don't trust scripts**. Fantastic. Now tell me: is it better to rely on something that is tested and repeatable, or doing configuration changes on the fly hoping for the best?

**How do I know it will work?** Welcome to the world of software development. Write code, include unit and integration tests, test everything, deploy in a pilot environment, and finally in production. Lather, rinse, repeat.

**But it might mess up my configurations**. And you think nobody ever messed up their database? We have backups for a good reason -- and most networking gear has some configuration versioning and rollback mechanisms.

**But it might crash my switch**. It might. Database systems have their own bugs, and I'm positive you were able to crash some databases with invalid data or weird requests a few decades ago... but guess what: unless we start screaming at the vendors, and vote with our wallets, nothing will change.

**What about maintenance windows?** We have to use maintenance windows in current networks because we can't trust the manual configuration process. When was the last time you could do your e-banking transaction only at 2AM on a Sunday morning? Once everyone starts trusting the network configuration transactions, you'll be able to use them at any time.

Have you encountered any other objections? Write a comment!

Finally, you might decide that your network isn't big enough to warrant a network automation solution (or that you don't have the manpower to work on it). The next best thing you might do is [decoupling](/2011/12/decouple-virtual-networking-from.html): [move the dynamic parts of your network infrastructure into the virtual world](/2013/04/virtual-appliance-performance-is.html) where you can [treat is as code](/2014/06/infrastructure-as-code-actually-makes.html), and keep the physical part of your network infrastructure as static as possible.

### More Information

We talked about [network infrastructure-as-code](https://my.ipspace.net/bin/list?id=AutConcepts#NIAC) in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
