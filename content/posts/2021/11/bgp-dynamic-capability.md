---
title: "Dynamic Negotiation of BGP Capabilities"
date: 2021-11-30 07:15:00
tags: [ BGP ]
---
I wanted to write a blog post explaining the intricacies of *Advertisement of Multiple Paths in BGP*, got into a yak-shaving exercise when discussing the need to exchange BGP capabilities to enable this feature, and decided to turn it into a separate prerequisite blog post. The optimal path selection with *BGP AddPath* post is coming in a few days.

### The Problem

Whenever you want to use BGP for something else than simple IPv4 unicast routing the BGP neighbors must agree on what they are willing to do -- be it multiprotocol extensions and individual additional address families, graceful restart, route refresh... (IANA has the [complete BGP Capability Codes registry](https://www.iana.org/assignments/capability-codes/capability-codes.xhtml)).
<!--more-->
BGP capabilities were designed to be negotiated at the start of a BGP session and advertised within the BGP OPEN message, which means that you have to tear down BGP sessions whenever a new functionality (like *BGP Add Path*) or address family is configured. 

Some BGP implementations expect you to tear down the sessions yourself which makes for fun troubleshooting if you never heard about BGP capability exchange -- nothing happens until you clear the BGP session, and then all of a sudden everything works[^L1]. 

Other implementations are more aggressive[^SUP] and automatically reset BGP sessions whenever you configure something that requires a renegotiation of BGP capabilities[^DCAP]. Some go as far as calling that Hammer-of-Thor approach *Dynamic Capability Exchange*.

[^L1]: Makes you wonder whether there's some truth behind the _did you reload the box_ question you get from level-1 support.

[^SUP]: I could get snarky and claim they are more aggressive to lower the vendor support costs, but vendors would never risk the stability of your network to reduce their costs, would they?

[^DCAP]: At least some implementations of *dynamic capabilities* are configurable.

### The Solution

Then there's the right way of doing things: *[Dynamic Capability for BGP-4](https://datatracker.ietf.org/doc/html/draft-ietf-idr-dynamic-cap-16)* draft describes a new CAPABILITY BGP message that can be used to renegotiate BGP capabilities without bringing down a BGP session. For whatever reason, that document has been sitting in draft status for almost a decade -- looks like everyone loves bringing down their BGP sessions for no good reason.

### Is There Anybody Out There?

I know I'm missing tons of details and I'd love to get your feedback. I hope to be able to end with a table describing how various BGP implementations work, so please leave a comment:

* How does the platform you use handle changes in BGP address families or other BGP features like additional paths?
* Is the tear down of BGP session on a configuration change that requires capability renegotiation: nonexistent, automatic or configurable?
* Did anyone implemented Dynamic Capability for BGP-4 draft? A quick search indicates it might be implemented by NX-OS, but the documentation [claims something completely different](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/unicast/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_Unicast_Routing_Configuration_Guide_7x/b_Cisco_Nexus_9000_Series_NX-OS_Unicast_Routing_Configuration_Guide_7x_chapter_01011.html#task_4546602316DF4854AD465E4960FE41FF) (automatic reset of BGP sessions).


