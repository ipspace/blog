---
date: 2020-09-16 06:20:00+00:00
series:
- host-firewalls
tags:
- security
- firewall
title: Why Don't We Have Dynamic Firewall Policies
---
One of the readers of the [Considerations for Host-Based Firewalls](/2020/09/considerations-host-based-firewalls/) blog post [wrote this interesting comment](/2020/09/considerations-host-based-firewalls/#115):

> Perhaps a paradigm shift is due for firewalls in general? I'm thinking quickly here but wondering if we perhaps just had a protocol by which a host could request upstream firewall(s) to open access inbound on their behalf dynamically, the hosts themselves would then automatically inform the security device what ports they need/want opened upstream.

Well, we have at least two protocols that could fit the bill: [Universal Plug and Play](https://en.wikipedia.org/wiki/Universal_Plug_and_Play) and [Port Control Protocol (RFC 6887)](https://tools.ietf.org/html/rfc6887).
<!--more-->
{{<note>}}Interesting bits of trivia: 

* UPnP is a set of standards defined by [Open Connectivity Foundation](https://openconnectivity.org/foundation/) and published as ISO/IEC standards. One has to wonder what made them choose this standardization path instead of working within IETF. [Maybe this](/2020/09/worth-reading-making-rfc/)?
* PCP is [implemented on Junos](https://www.juniper.net/documentation/en_US/junos/topics/concept/nat-port-control-protocol.html) but not on Cisco IOS (at least I couldn't find it). No surprise there either...
{{</note>}}

However, we have a much bigger problem. Continuing with the comment...

> The firewall would have the ability to permit or deny the traffic based on its larger policy definition. This would resolve both the issue of admins not knowing what ports are needed for an application and could help resolve the issue of "stale" policies left on the firewalls.

Let's start with some ground rules. We expect firewalls to work at reasonably-high speeds, and as TCP/IP uses connectionless datagram transport at layer-3 (watch [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar if this sounds like Latin), the only mechanism a firewall can use to decide whether to drop or pass an incoming IP packet is to:

* Extract the relevant packet headers;
* Identify the flow the packet belongs to (hoping other security mechanisms deployed in the network prevented too-blatant flow spoofing);
* Use the flow-level information to make the drop/pass decision.

The crucial part of any firewall implementation is thus the flow admission policy. Here's how traditional firewalls approach that challenge:

* Firewall rules are created based on the best knowledge of security policies and application requirements (lots of [handwaving](https://wiki.c2.com/?HandWaving) in this sentence, but it doesn't matter);
* Firewall rules are downloaded into firewall(s). In many cases, everything ever known about any deployed applications' requirements is dumped into a single hand-crafted firewall ruleset which quickly resembles an unmanageable spaghetti mess of Gordian knots.
* Faced with an incoming packet not belonging to a well-known flow, a firewall scans the security rules, finds a rule that specifies what to do with the packet, executes the desired action, and remembers the decision in its flow table.
* Next-generation firewalls might look beyond packet headers when making the initial pass/drop decision, and might be able to look at the first few packets of a new session when deciding what to do (I [described the process VMware NSX firewalls are using](https://my.ipspace.net/bin/list?id=NSX#FW) in the [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinar).

**TL&DR summary**: to make any firewall work, we need a well-defined set of rules.

Back to the proposal made in the comment I quoted above (slightly rephrased):

* A host would request a firewall to open an inbound port;
* The firewall would permit/deny that request based on its policy;
* This would resolve the issue of application developers or server admins not knowing what ports the applications are using;
* It could help resolve the problem of stale firewall policies.

Unfortunately, you can't change the ground rules. **A security device needs predefined security policy** when deciding whether to permit a security-related request. It doesn't matter if the security policy is written in a high-level language, or using the familiar 5-tuples. It doesn't matter if the request is signaled in a TCP SYN packet on with an out-of-band protocol. The fundamental question still remains _how do we define a security policy_?

Assuming we know the required connectivity between various components of numerous application stacks deployed in a typical Enterprise IT environment (another _[then a miracle occurs](http://www.sciencecartoonsplus.com/gallery/math/math07.gif)_ assumption), we could implement the proposal... but we could also find all the necessary information using out-of-band information collection means and create a firewall-friendly security rules (lists of source/destination addresses and ports) in the background.

There are numerous production-grade implementations out there doing exactly that for source/destination IP addresses (NSX microsegmentation and public cloud security groups come to mind), and finding the application port numbers is as easy as executing **netstat -ltup** on a Linux server and parsing the results. An extra protocol thus won't give much more.

Given all that, one has to ask "_so what exactly is the problem we're trying to solve?_" In most cases, the problem is "_we have no clue who should be allowed to talk to whom_" and no amount of magic technology will ever solve that problem for us. As [I pointed out numerous times in various presentations](/2014/09/youve-been-doing-same-thing-for-last-20/) (you might enjoy watching [Business Aspects of Networking Technologies](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies) webinar), you can not solve people- and processes problems with black-box technologies and layers of abstraction, and continuing to do the same broken thing and expecting different results is one of the definitions of insanity.

More to come...