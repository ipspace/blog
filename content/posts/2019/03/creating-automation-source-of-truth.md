---
date: 2019-03-21 09:50:00+01:00
tags:
- automation
- data models
title: Creating Automation Source-of-Truth from Device Configurations
url: /2019/03/creating-automation-source-of-truth.html
series: [ ssot ]
ssot_tag: build
---
Remember the previous blog post in this sequence in which I [explained the need for single source-of-truth used in your network automation solution](/2019/03/building-network-automation-source-of.html)? No? Please read it first ;)

Ready for the next step? Assuming your sole source-of-truth is the actual device configuration, is there a magic mechanism we can use to transform it into something we could use in network automation?

**TL&DR: No.**
<!--more-->
I've seen tons of solutions (several of them available on GitHub) that tried to solve the problem once-and-for-all by parsing device configuration and extracting relevant bits from it. The first step of this idea works great for devices that can produce device configuration in machine-parseable format like JSON or XML (Junos, late IOS XE...); if you're not so lucky you'll have to write your own parser.

{{<note>}}
You might use one of the published solutions as a starting point, but you'll probably have to adapt it anyway as nobody wasted their time implementing the parser for all the [weird nerd knobs](/2015/08/musing-on-nerd-knobs.html) that someone in [their infinite wisdom decided to use in your network](/2013/04/this-is-what-makes-networking-so-complex.html).
{{</note>}}

OK, so now you have the relevant bits of information extracted from network devices. What's next? This is where this approach becomes complicated. You might decide what you got is good enough for your needs and dump the collected information into YAML or JSON files (one per device). Congratulations, you replaced text device configuration with even-less-readable representation of what the device should be doing.

{{<note info>}}
This approach might be perfectly viable if you have to replace platform A with platform B (example: migrating from IOS XE to Junos) assuming platform B has a superset of functionality used on platform A. I know of large organizations that decided it's worth the effort to automate configuration translation. However, while they executed the transition flawlessly, it didn't bring them any closer to having the network automated.
{{</note>}}

What we're aiming for in a decent network automation solution is more than just [device state in machine-readable format](/2018/09/network-infrastructure-as-code-is.html). In the ideal world, we'd like to have infrastructure- or service description in a high-level data model that ignores the irrelevant details. For example, instead of interface IP addresses and OSPF costs, we'd like to know about network nodes and links, and have IP subnets and routing protocol parameters derived automatically.

Having that goal in mind, the only way forward is to:

-   Take the parameters extracted from network devices and reverse-engineer the desired data model from those parameters (for example, having an interface in OSPF area 0 might indicate that the interface is a core link);
-   Recreate device configurations from the data model and standardized templates;
-   Compare desired device configuration with current device configuration;
-   Clean up the snowflake device configurations or enhance the data model and configuration templates until the two are in sync.

{{<note info>}}
There are tools on the market (example: Cisco NSO) that can do most of the job for you. However, don't expect them to be simple or cheap.
{{</note>}}

Is it worth the effort? After dealing with device configurations for ages and having seen the benefits of easy-to-generate standardized configurations I'd say the answer is a resounding YES, but it's hard to believe me while standing in front of the [Broccoli Forest of Despair](https://networkingnerd.net/2012/11/08/juniper-land-of-unicorns-and-broccoli/).

Want to try? Need help along the way? Hundreds of your peers enjoyed our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) course.
