---
index: true
kb_section: CiscoAutomation
minimal_sidebar: true
toc_title: Overview
url: /kb/CiscoAutomation/
title: Automation for Cisco NetDevOps
kb_tag: automation
author:
  name: Andrea Dainese
  link: https://www.linkedin.com/in/adainese/
---
Approaching IT automation can be confusing even for seasoned tech guys. There are few reasons:

* vendors are selling magic black boxes (as usual);
* vendor's solutions don't often work as expected (again, as usual);
* there are so many open-source tools supposedly solving the same problem;
* your needs are pretty unique and it seems that no tool can fit your needs.

If every IT infrastructure is like a snowflake, all snowflakes have some similarities in common. In other words:

* Try to abstract your infrastructure;
* Understand pros, cons and limits of every tool/framework/technology available today;
* Choose a set of tools that can cover 80% of your needs and extend them (or adapt your environment).

Obvious, but no less important:

* Do not reinvent the wheel;
* Understand theory first, and then focus on technologies or products;
* Learn from other's mistakes.

This set of articles will focus on technologies available today; numerous [ipSpace.net webinars](https://www.ipspace.net/Roadmap/Network_Automation_webinars) and [online courses](https://www.ipspace.net/Courses) already cover theory and popular tools.

## Frameworks

There are many ways to automatically interact with network devices. I would categories them as following:

* Zero Touch Provisioning (ZTP): the method to bring a brand new device in a configured state without logging in to it.
* Screen Scraping: the set of tools that connect to a terminal session (or line), giving commands and interpreting the output. I'm including web scraping (making HTTP requests and parsing HTML responses) in this category.
* NetConf and RESTConf: the "standard" solutions that will fix everything (maybe).
* Native Web API: HTTP/HTTPS services available to configure devices. Sometimes API are complete, sometimes not. I'm including in this category any API what can be consumed via HTTP/HTTPS, like REST, SOAP...
* Automation tools like Ansible, Salt Stack, Puppet, but also Cisco Prime Infrastructure, Cisco Evolved Programmable Network Manager, Cisco Data Center Network Manager, Cisco DNA Center, Cisco APIC-EM...
* Software Development Kit (SDK): libraries for many programming languages (usually Python and Java).
* Embedded interpreters (like Python or even Cisco EEM)

It's very important to understand pros, cons, and (above all) the limitations of each approach and underlying technologies before you start to use them. Keep in mind that whatever vendors say might not correspond with reality.

The rest of this series of articles will address individual categories I mentioned.
