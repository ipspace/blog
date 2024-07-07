---
date: 2016-06-01 12:45:00+02:00
tags:
- security
- SDN
- SD-WAN
title: What Is Software-Defined Security?
url: /2016/06/what-is-software-defined-security/
sd-wan_tag: rant
---
Gabi Gerber is organizing a [Software-Defined Security event](http://www.digs.ch/de/digs-special-interest-group-sdn/) in Zurich next week in which I'll talk about real-life security solutions that could be called *software defined* for whatever reason, and my friend [Christoph Jaggi](http://uebermeister.com/about.html) sent me a few questions trying to explore this particular blob of hype.

For obvious reasons he started with "*Isn't it all just marketing?*"
<!--more-->
> While many people in the industry talk about Software Defined Security (SDS) the usage of the term seems to be more driven by marketing than by technology. Since decades most, if not all security functionalities are defined through software. What makes SDS different and what is new?

You're absolutely right, and from this perspective the Software-Defined Security makes even less sense than Software-Defined Networking (some network devices implement forwarding functionality in hardware).

Changing the Software-Defined terminology to something that makes sense is a lost battle, but at least we can hope to find a useful definition. The one focusing on "*managing services through* [*abstraction*](https://my.ipspace.net/bin/get?doc=14cb35a0-d02e-11e5-a2b0-005056880254) *of* *lower-lever functionality*" works reasonably well. I would also ask for:

-   [Well-documented API](/2014/02/cli-or-api-wait-do-you-really-have-to/) that can be used to extract operational state from the device and change device configuration or soft state;
-   Capability to create security services on demand and [insert them in the forwarding path](/2014/02/service-insertion-with-openflow/) on as-needed basis.

> Security is a process and not a single function. The objective of the process is to have data and network security. Encryption, intrusion detection, intrusion prevention, DDoS mitigation and data loss prevention are just some of the functions that support the process. Where does Software Defined Security (SDS) fit in?

All of the functions you mentioned can be abstracted and made simpler to consume. For example:

-   [Microsegmentation solutions](https://my.ipspace.net/bin/get?doc=8b38b330-ba2f-11e5-a2b0-005056880254) automatically deploy [distributed firewall rules built from data contained in orchestration system](/2015/03/microsegmentation-in-vmware-nsx-on/) (example: VM names or groups mapped into IP addresses);
-   [Software-Defined WAN solutions](/tag/sd-wan/) automatically protect all traffic transported across public networks;
-   [Service chaining solutions](https://my.ipspace.net/bin/get?doc=cb9671a6-bfb1-11e5-a2b0-005056880254) allow an operator to stitch together multiple security services on demand.
-   [Network Function Virtualization](http://www.ipspace.net/Network_Function_Virtualization) (NFV) frameworks allow users to deploy instances of security functions on as-needed basis.

> A full automation requires that all resources needed are constantly online and reachable. Can this create additional attack surface that can be exploited?

Absolutely. Every API creates an additional attack surface, and centralized management or orchestration systems contain crown jewels coveted by every intruder. However, that's nothing new; we were facing similar challenges for decades.

> What are the typical use cases of SDS? Is it limited to virtualized data centers or is it used in other environments as well?

Most SDS use cases I'm aware of are indeed deployed in data centers, primarily in private or public clouds. These use cases include:

-   Microsegmentation (the focus of the [DIGS Special Event](http://www.digs.ch/de/digs-special-event/) on June 7[th]{style="vertical-align: super; font-size: 80%;"}), including automatic creation of security rules and automatic validation of security policies;
-   DoS detection and mitigation tools, including automatic fallback to third-party scrubbing services;
-   Firewall bypass for high-volume flows;
-   Programmable network taps and tap aggregation networks;
-   Scale-out network services;
-   High-speed traffic analysis;
-   Consistent edge policy enforcement.

We'll discuss most of them in the [2[nd]{style="vertical-align: super; font-size: 80%;"} DIGS SDN Meeting](http://www.digs.ch/de/digs-special-interest-group-sdn/) on June 7[th]{style="vertical-align: super; font-size: 80%;"} and I described many of them in the [SDN Use Cases](http://www.ipspace.net/SDN_Use_Cases) webinar.

> What are the key points to look at in terms of software defineability when shopping for an SDS solution?

I would start with [Gartner's Shiny New Object](http://blogs.gartner.com/andrew-lerner/2015/01/15/netsecdirtydozen/) checklist:

-   Do we have a problem?
-   Can the root cause of the problem be solved by changing our policies or processes?
-   Will I get a similar solution from my existing vendors within a year?
-   Do I have existing network or security capabilities that can address most of the technology requirements?
-   If we buy new technology, do we have the right processes and expertise to properly use it?

In many cases it turns out that the root cause of the problem we're trying to solve is [not technology](/2014/09/youve-been-doing-same-thing-for-last-20/) but people, silos, [broken processes](/2013/11/typical-enterprise-application/) or rigid policies... and even if we buy new technology we won't solve the root cause.

If however you have to buy new technology (including new deployments and regular refresh cycles) I'd check that:

-   You can get the functionality you need in [virtual format](/2013/04/virtual-appliance-performance-is/) (even if you end up buying a physical box);
-   You can interact with the security functions (software solutions, VMs or physical appliances) through a well-documented API;
-   The solution you plan to deploy includes the minimum possible amount of moving parts (gateways, integration points, plugins...).
