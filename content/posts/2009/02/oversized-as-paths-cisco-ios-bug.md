---
date: 2009-02-20 21:32:00.004000+01:00
tags:
- BGP
title: 'Oversized AS Paths: Cisco IOS Bug Details'
url: /2009/02/oversized-as-paths-cisco-ios-bug.html
---
Numerous articles describing the widespread routing instabilities caused by [sloppy parser of a small router vendor](/2009/02/root-cause-analysis-oversized-as-paths.html) (including posts at [BGPmon](http://bgpmon.net/blog/?p=125), [Renesys](http://www.renesys.com/blog/2009/02/the-flap-heard-around-the-worl.shtml), [Arbor Security](http://asert.arbornetworks.com/2009/02/ahh-the-ease-of-introducing-global-routing-instability/) and [my blog](/2009/02/protect-your-network-with-bgp-maxas.html)) hinted that the unusual BGP update caused so many problems because the ISPs were using outdated Cisco IOS releases. This is definitely not the case; all classic IOS releases were affected.

Rodney Dunn from Cisco and myself were quickly able to reproduce so far unknown bug in Cisco IOS that occurs only when the inbound AS-path contains close to 255 AS numbers and the router does inbound or outbound AS-path prepending. The new bug is tracked as [CSCsx73770](http://www.merit.edu/mail.archives/nanog/msg15784.html) and affects downstream EBGP or IBGP sessions as follows:
<!--more-->
-   When you do *inbound AS-path prepending* and receive a BGP update where the total length of inbound AS-path and prepending exceeds 255, the AS-path in your BGP table is completely mangled. The path is sporadically advertised to IBGP or EBGP peers and kills downstream BGP sessions (remote BGP peer sends BGP notification due to invalid UPDATE message).
-   When you do *outbound AS-path prepending* and send a BGP update where the total length of the AS-path in your BGP table, prepended AS-path and your own AS-number exceed 255, the outbound EBGP update is incorrect and the downstream EBGP peer sends BGP notification, resulting in BGP session reset. IBGP peers are not affected, as IOS does not perform AS-path prepending on IBGP sessions.
-   If you don't prepend, you're safe. IOS marks BGP paths with AS-path length greater or equal to 254 as invalid and does not propagate them, so the AS-path length in the outbound update can never exceed 255 without prepending.

All the problems associated with CSCsx73770 can be avoided if you [limit the AS-path length](/2009/02/protect-your-network-with-bgp-maxas.html) with the **bgp maxas-limit** global configuration command.

When I was testing the IOS behavior in my lab, I was not aware how long the offending AS-path was, so my [initial analysis was incorrect](http://www.merit.edu/mail.archives/nanog/msg15530.html). With the input from NANOG mailing list [supplying to the actual length of the AS-path](http://www.merit.edu/mail.archives/nanog/msg15730.html), this is the most probably scenario: the offending AS-path length was close enough to 255 that the outbound AS-path prepending performed between Tier-1 providers (or their peers) that did not limit the AS-path length caused EBGP sessions to reset (if someone performs inbound AS-path prepending, the IBGP sessions would suffer). Those providers that implemented AS-path length limiting successfully protected their downstream peers and their customers (unless, of course, the customers were running really old IOS releases).
