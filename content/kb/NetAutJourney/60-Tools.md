---
kb_section: NetAutJourney
minimal_sidebar: true
title: Tools Used in My Automation Projects
toc_title: Tool Overview
url: /kb/NetAutJourney/60-Tools.html
---
I used numerous tools in my network automation projects. Here are some
of those I think are worth investing your time in.

## Ansible

Let's start with Ansible. While it is very versatile and easy to use,
it does have its shortcomings. I found myself creating extensive
[regular expressions in playbooks](https://www.ipspace.net/kb/Ansible/Parsing_Text_Printouts_Ansible.html),
some of which I am pretty sure I will regret later on
(so-called _[write-only code](https://blog.ipspace.net/2018/04/avoid-write-only-code.html)_).

It is also hard to avoid trying to use playbooks as a programming language.
Ansible sort-of lures you into it as the playbook abstraction(or DSL, _domain-specific language_
as I since learned) leaves you with a limited set of tools when it comes to more complex
logical structures. Before long, you create a task that loops over a long list,
calling an Ansible module for each item in the list. This approach utterly kills
the playbook performance and leads to a vast consumption of resources.

Which brings me to the next issue with Ansible: it is very resource-intensive.
Initially, I thought that pulling data from network devices would be a bottleneck,
but in most cases, the bottleneck is the CPU of the Ansible server. It's not a
huge problem if you have around 100 devices; on a network with close to 1300 devices,
a couple of my playbooks take too long to complete for all devices. I plan to rewrite
some of the _anti-patterns_ into Jinja2 or create more dedicated plugins for the CPU
intensive tasks, and I am looking at Nornir to enhance performance further.

Finally, you want to make sure Ansible is not dependent on the python libraries
that come with whatever OS you are running it on, sooner or later something breaks.
Pyenv can help with this - you can use it to run Ansible in a dedicated Python
environment, and stay in control of the libraries used.

{{<note info>}}You can also decide to [run Ansible in a Docker container](https://packetpushers.net/building-a-docker-network-automation-container/).{{</note>}}

## NAPALM

A terrible acronym for an [awesome tool/library](https://github.com/napalm-automation/napalm).
Each time I read _NAPALM_, I wonder whether other substances involved in war crimes
were considered as acronym candidates.

That said, it is fantastic to have a playbook created for doing something on one
platform do precisely the same thing on a completely different platform. Or witness
NAPALM doing a neat rollback of a configuration on a Cisco IOS device after a
configuration error. Using NAPALM as much as you can is the best possible
future-proofing of your effort, its benefits can hardly be overstated.

## Graphviz

[Library to create graphs](https://www.graphviz.org/) based on plaintext input files.
Brilliant in its simplicity, it can be used to generate flowcharts, network diagrams,
and other graphs from plaintext input files. I have started to use it to create
simple diagrams as it is so much quicker than using Visio.

Note that for more elaborate diagrams with multiple levels, the options for node
placements are limited. I plan to look at generating diagrams in SVG, so I can
include clickable URLs in the diagram, which could be a nice addition. I also plan
to tweak the current diagrams to include more details, such as IP addresses.

## FreeZTP

If you, like myself, enjoy watching a machine doing a tedious job better than you
could have done it yourself, [FreeZTP](https://github.com/PackeTsar/freeztp)
is the ticket for provisioning network devices. It includes logic to deal
with stackable switches, and there are some useful EEM scripts available
to do the stack switch renumbering.
