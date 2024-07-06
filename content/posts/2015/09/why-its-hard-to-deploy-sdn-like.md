---
cli_tag: challenge
date: 2015-09-16 09:33:00+02:00
series:
- cli
tags:
- SDN
title: Why It's Hard to Deploy SDN-Like Functionality Today
url: /2015/09/why-its-hard-to-deploy-sdn-like.html
---
Whenever I talk about the various definitions of SDN (ending with the "SDN provides an abstraction layer"), old-timers sitting quickly realize that the SDN products that you can deploy in real life aren't that different from what we did in the past -- an SDN controller is often just an overhyped glorified network services orchestration system.

OK, so why didn't we have that same functionality for the last 20 years?
<!--more-->
### Diverting into Anecdata

Some large networks were fully provisioned by orchestration systems for years -- be it with home-grown tools, or ridiculously expensive multi-vendor solutions (Cisco alone had at least two or three products claiming to do network services provisioning in the past).

A while ago I was talking with someone who actually used one of those multi-vendor tools, and he had two major complaints: (A) any change was ridiculously expensive because (B) the solution provider wanted to do full-blown regression tests on every single hardware variant and software version they planned to deploy in the production network.

One has to wonder what led someone to such a level of paranoia.

### The Clumsy Configuration Interface

SDN evangelists are quick to point out how CLI is the root of all evil (guess what: it's not), but there is something [fundamentally wrong with most CLIs](/2014/02/is-cli-in-my-way-or-is-it-just-symptom.html) used on networking gear today: they were never designed with scripting, automation or machine-to-machine communication in mind. They were always targeting a lone network operator furiously typing on the keyboard; even cut-and-paste didn't always work, as some devices didn't do proper input buffering.

While it might be possible to fix the configuration part of the CLI mess (Cisco used to have CLI police that would stop the programmers from messing up too badly, but they must had disbanded it by the time MQC was coded), the instrumentation/monitoring part might be beyond hopeless.

Some vendors (example: Juniper) did the right thing. Every printout starts as a data structure which you can get in XML format or rendered through the printout template.

The XML format is extremely easy to parse in network automation environment (XML libraries are available for every operating system and major programming language) and quite resilient to adds and changes -- as long as the old tag and attribute names don't change, the code processing the XML output doesn't have to care about new fields, tags, or reordered data.

It seems that most other vendors still believe in producing printouts with **sprintf** calls liberally sprinkled throughout the code. Cisco is definitely one of them (but do keep in mind that they have a 30-year-old code base), and Arista might be another one -- I can see no other reason why they'd be so slow in rolling out the eAPI support for individual **show** commands.

The printouts produced by these vendors also tend to change across software releases (and even maintenance releases). After all, the network operator (or the TAC engineer) doesn't care if the printout is slightly different from the one produced the previous day. Automation scripts do.

{{<note>}}According to some senior instructors I chatted with, students in certain geographies experience the same behavior -- if the printout seen on the console doesn't match the one in the student guide character-by-character there must be something wrong.{{</note>}}

Processing output produced by such code by an automation script always involves some amount of screen scraping (PERL regexp anyone?), and heavy regression testing to ensure a software upgrade doesn't break the screen scraping functionality, resulting in very high costs of multi-vendor orchestration systems.

{{<note warn>}}Don't even try to tell me NETCONF is the answer. A **show** command executed through NETCONF on Cisco IOS returns the traditional printout in XML envelope, and multi-vendor data models are still a bit of a pipe dream.{{</note>}}

Unfortunately, I don't expect this sad state of affairs to improve until the old software dies (probably after I'll be old enough to retire) -- it would be pretty hard to persuade anyone to rip out all the legacy stuff in millions of lines of code. Or (if you're brave enough) you might go for vendor-supported screen scraping (aka [Cisco EDI](http://www.cisco.com/c/en/us/products/cloud-systems-management/enhanced-device-interface/index.html)).
