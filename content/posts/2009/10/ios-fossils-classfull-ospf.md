---
date: 2009-10-02 06:46:00.001000+02:00
ospf_tag: config
tags:
- OSPF
- IOS fossils
title: 'IOS Fossils: Classful OSPF Redistribution'
url: /2009/10/ios-fossils-classfull-ospf.html
---
In the classful days of the Internet, it made sense to limit the amount of information redistributed between the routing protocols. OSPF was always classless, but RIPv1 wasn't ... and you could get all sorts of crazy routes from RIP that would mess up the rest of your network if they ever got redistributed into OSPF. To prevent that, Cisco's engineers introduced the **subnets** option in the OSPF **redistribute** command.

{{<note>}}
Either the OSPF **redistribute** command is really old (before the **distribute-list** command started accepting extended ACL, which could filter on the subnet mask), or someone was too dumb to use the extended ACL, and Cisco had to provide an obvious workaround.
{{</note>}}

By the time Cisco implemented EIGRP and BGPv4 (IOS release 9.21, 15+ years ago), the absurdity of the classful redistribution was already obvious. These routing protocols accept whatever routes you want to redistribute, and their variants of the **redistribute** command don't have the **subnets** keyword. However, nobody ever took steps to remove this fossil from the IOS code.
<!--more-->
I wouldn't care if we were talking about an obscure option like the [OSPF-to-BGP redistribution tags](https://blog.ipspace.net/2009/05/ios-fossils-ospf-to-bgp-redistribution.html), but the OSPF **redistribute** command is one of the most confusingly harmful IOS routing protocol commands (the only one getting close in my opinion is the **auto-summary** in EIGRP). One of the IOS releases introduced a warning that would be printed whenever you're configuring redistribution into OSPF without the **subnets** keyword (great job: wouldn't it be better to fix the problem?).

``` code
rtr(config)#router ospf 999
rtr(config-router)#redistribute static
% Only classful networks will be redistributed
```

Alas, the warning is incorrect. Yuri Selivanov sent me an interesting observation: while the subnets don't get redistributed without the **subnets** keyword, supernets do. The "classful" filter is not even working correctly (or, at the very least, it's not doing what the Cisco IOS claims).

I am positive Cisco will never fix this problem, and we'll have to cope with this command until the last bits of IPv4 code are erased from Cisco IOS, but here are a few things they could have done:

-   Remove the classful redistribution filter from the code and make the **subnets** keyword obsolete. I sincerely doubt any reasonably-sized network is running classful redistribution with recent IOS code (and who cares about the network cores running on AGS+).
-   Add another option to the OSPF process that disables the filter. This option would have to be explicitly stored in the router configuration like the **log-adjacency-changes** OSPF configuration command (to ensure the old configurations work) but should be turned on for all new instances of OSPF routing protocols.

Undoubtedly a few people (mostly old-timers) would get confused once or twice, but the number of OSPF support cases might be "slightly" reduced.
