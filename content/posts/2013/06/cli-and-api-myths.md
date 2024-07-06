---
cli_tag: basics
date: 2013-06-24 07:38:00+02:00
series:
- cli
tags:
- SDN
- network management
title: CLI and API Myths
url: /2013/06/cli-and-api-myths.html
---
Greg Ferro published a great blog post explaining why he [decided to use node.js to build his cloud automation platform](http://etherealmind.com/thoughts-on-choosing-node-js-for-automation/). While I agree with most things he wrote, this one prickled me the wrong way:

> In my view, an Application Programmable Interface(API) is the fundamental change that makes Software Defined Networking (SDN) a "thing". We need to realise that the CLI is a "power tools" for specialist tradespeople and not a "knife and fork" for everyday use.

While I agree with his view on CLI, keep in mind that API is no different.
<!--more-->
### Device-Level API

Take a closer look at the product and programming documentation (not marketing fluff) of any product with CLI and API interface. What you'll find in almost all cases is that:

-   Both methods provide a *configuration and monitoring* (management plane) interface. F5 iRules and similar tools are an obvious exception.
-   The available functionality is usually the same, with the exception of vendors who never understood the concept of *feature parity.*

Surprised? You shouldn't be -- CLI, API (and Web GUI) are doing the same thing behind the scenes: changing values of configurable variables and data structures. It doesn't matter which mechanism you use to set a variable value or insert a new data structure in a linked list -- no API will save the day if the software you're interacting with doesn't support the functionality you need.

{{<note>}}Newer platforms commonly use the same API exposed to the end-user to implement their CLI and GUI.{{</note>}}

Also keep in mind that no two APIs are identical (or even similar). Almost every device-level API (including whatever-over-NETCONF) is proprietary; the rare exceptions are standard SNMP MIBs and Quantum plug-ins (Did I miss anything? Write a comment!).

The only difference between CLI and API is the target audience. CLI is easier for humans, API is easier for machines. However, any programmer worth his salt should be able to create an abstraction layer offering reasonable entry points to the outside world and dealing with device-specific idiosyncrasies (that's what [Netdev](https://github.com/NetdevOps/puppet-netdev-stdlib) is aiming to do for Puppet) \... and ensuring transactional consistency on a device that doesn't support the concept (like Cisco IOS) is mission impossible regardless of which configuration method you use.

### Network-Level API

I love listening to SDN pundits telling us how it's too expensive to touch every device in the network to provision a new *whatever* and how SDN and APIs will solve that problem. Really? Would you mind rereading the previous section?

The way we provision services today is too expensive and cumbersome, there's no doubt about that, but changing the configuration/programming paradigm from text-over-SSH to JSON-over-SSL is nothing more than eye candy. What we need is a *network-level abstraction,* at which point it doesn't matter (yet again) whether we use CLI or API to configure the network-wide services. What matters is the *level of abstraction*.

### Theory or Reality?

There are several tools out there that give you a network-level API, including [NCS from Tail-f](/2013/05/tail-f-network-control-system-first.html) (now Cisco), [VMware NSX-T](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) and [Cisco ACI](https://www.ipspace.net/Cisco_ACI_Deep_Dive), and a plethora of _[intent-based](/tag/intent-based-networking.html)_ systems. However, we're all aware of networking vendors' dismal track record when it comes to network management tools. Why should they do any better this time?
