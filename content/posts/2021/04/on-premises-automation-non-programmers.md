---
title: "Starting Network Automation for Non-Programmers"
date: 2021-04-19 06:22:00
tags: [ automation ]
---
The reader asking about [infrastructure-as-code in public cloud deployments](/2021/04/starting-infrastructure-code.html) also wondered whether he has any chance at mastering on-premises network automation due to lack of programming skills.

> I am starting to get concerned about not knowing automation, IaC, or any programming language. I didn't go to college, like a lot of my peers did, and they have some background in programming.

First of all, thanks a million to *everyone needs to become a programmer* hipsters for thoroughly confusing people. Now for a tiny bit of reality.
<!--more-->
Dozens (if not hundreds… I never asked) networking engineers successfully completed our network automation course with no prior programming experience. What you do need to master however is computational thinking -- the ability to figure out step-by-step processes and data structures needed to support them -- as explained in these blog posts:

* [You Don’t Need Programming Skills to Build Network Automation Solutions](https://blog.ipspace.net/2016/12/you-dont-need-programming-skills-to.html)
* [Use Your Networking Knowledge to Design Automation Solution](https://blog.ipspace.net/2017/05/use-your-networking-knowledge-to-design.html)

> What would be the best way to start the network automation journey?

Here's what worked for me:

* Get at least some familiarity with tools like Git and Vagrant.
* Even if you have plenty of spare gear, build a [small virtual lab](https://blog.ipspace.net/2021/04/exercise-build-network-automation-lab.html) just to get experience (if you want to build it on Linux, I [collected a few useful pointers](https://netlab.tools/install/)).
* Find the simplest possible problem that is ripe for automation. Some engineers collected software versions, others system uptime (to find [crashes or UPS failures](https://blog.ipspace.net/2017/04/network-automation-is-much-more-than.html)) or [transceiver levels](https://github.com/steve-krause/netauto-class/tree/master/transciever_report) (to find failing links), or verified that all devices had the same syslog or NTP servers configured.
* Want to create diagrams? Course attendees created [VLAN diagrams](https://blog.ipspace.net/2017/11/create-vlan-map-from-network.html), [IP multicast distribution trees](https://blog.ipspace.net/2017/12/create-ip-multicast-tree-graphs-from.html), [graph of BGP sessions](https://github.com/ctopher78/network-automation-course/tree/master/Homework2), or [L3VPN connectivity models](https://github.com/pke11y/net-auto-sol/blob/master/summary-report/blog/parse_cisco_pyats.md).
* Build a simple data model describing desired state of your networking infrastructure or service, and a simple deployment script that builds device configuration from that data model and deploys it. It could be as simple as “a list of NTP servers that have to be configured everywhere” or as complex as “deploy data center fabric with X leafs and Y spines”. You might get some ideas [looking at what others did](https://www.ipspace.net/NetAutSol/Solutions). 
* Adding complexity to the previous example, deal with changes to the data model (instead of adds, deal with adds, updates, and deletions). You could cheat and use configure replace or do something more complex.
* Build a [complete service deployment solution](https://theworldsgonemad.net/2021/automate-dc-pt1/).
* Add [validation](https://github.com/johnsondnz/ipspace-validation-example/blob/master/README.md) and testing to that solution. NAPALM had validation for a long while, [Ansible](https://blog.ipspace.net/2021/03/ansible-validation.html) and [NetworkToCode](https://blog.ipspace.net/2021/03/schema-enforcer.html) launched their validation solutions earlier this year.

Not surprisingly, this is the exact sequence of steps we’re using in the [automation course](https://www.ipspace.net/Building_Network_Automation_Solutions) ;)

> I hear a lot about Ansible, but recently read your rant about some nuisance. Nornir (Cisco DevNet?) is a popular topic, but I am fed up with Cisco certs and I'd like to keep this journey vendor agnostic if possible.

Ansible is like democracy: it’s the worst possible tool, but has the easiest learning curve. I highly recommend it to anyone who has no programming experience because that removes one of the mental barriers (“I don’t know how to program”). But remember that it’s like a tricycle: you don’t want to stay there if you ever plan on getting from A to B in a reasonable time, or if you like downhill racing. Eventually you’ll have to start exploring other tools like Nornir, and the beauty of most network automation tools like Ansible and Nornir is that they’re open-source and free.

I never looked into what Cisco DevNet certifications are, but in general Cisco’s certifications aren’t too bad as a blueprint of what needs to be learned, and if you’ll have to interact heavily with Cisco devices in your network, it’s not a bad idea to use their tools to manage those devices… obviously always keeping in mind that you want to remain vendor-agnostic.

### Revision History

2021-04-19
: Added network diagram solutions.
: Added links to examples and validations tools.
