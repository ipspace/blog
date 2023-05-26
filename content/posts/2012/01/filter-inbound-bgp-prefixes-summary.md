---
url: /2012/01/filter-inbound-bgp-prefixes-summary.html
title: "Filter Inbound BGP Prefixes: Summary"
date: "2012-01-16T07:32:00.000+01:00"
tags: [ Internet,BGP ]
lastmod: 2020-11-18 06:44:00
---
I got plenty of responses to the [*How could we filter extraneous BGP prefixes*](https://blog.ipspace.net/2012/01/how-could-we-filter-extraneous-bgp.html) post, some of them referring to emerging technologies and clean-slate ideas, others describing down-to-earth approaches. Thank you all, you’re fantastic!

Almost everyone in the “down-to-earth” category suggested a more or less aggressive inbound filter combined with default routing toward upstream ISPs. Ideally the upstream ISPs would send you [responsibly generated default route](https://blog.ipspace.net/2011/09/responsible-generation-of-bgp-default.html), or you could use static default routes toward well-known critical infrastructure destinations (like root name servers).
<!--more-->
{{<note update>}}2020-11-18: Removed links to Cisco-hosted prefix filter, added links to MANRS and Team Cymru.{{</note>}}

The best overall solution came from Killian – find a prefix filter that throws away most of the unnecessary garbage. Cisco was maintaining one a while ago (and now it's gone); you might find something similar on [MANRS](https://www.manrs.org/) web site or [Team Cymru Github repository](https://github.com/team-cymru/network-security-templates).

Someone else also suggested (in an e-mail) dropping all prefixes that are more than three AS away. His reasoning – you’re probably not more than three autonomous systems away from a tier-1 ISP, and it doesn’t make too much sense second-guessing them.

When implementing this idea, make sure you’re matching three distinct AS numbers (using a regular expression [like this one](/kb/tag/BGP/Filter_Excessively_Prepended_BGP_Paths.html)), not AS paths up to three entries long. AS paths could be longer due to AS-path prepending.

If you want to achieve more balanced traffic load, you could combine this idea with the one from Octavio – accept all prefixes from “near” autonomous systems and all prefixes larger than /18 (or whatever would still fit into your TCAM) from the rest of the Internet.

In any case, you should start your contemplation with the [business side of the problem](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies): what’s the true business need for full Internet routing table? Or, as Pete put it, “*If you have traffic to justify the peerings, then you can presumably afford the router that can take full Internet BGP routing table.*”
