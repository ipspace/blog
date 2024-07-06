---
date: 2011-09-16 07:14:00+02:00
tags:
- BGP
title: Responsible Generation of BGP Default Route
url: /2011/09/responsible-generation-of-bgp-default.html
---
Chris sent me the following question a while ago:

> I\'ve got a full Internet BGP table, and want to [responsibly]{.emphasis} send a default route to a downstream AS. It\'s the \"responsibly\" part that\'s got me frustrated: How can I judge whether the internet is working and make the origination of the default conditional on that?

He'd already figured out the **neighbor default-originate route-map** command, but wanted to check for more generic conditions than the presence of one or more prefixes in the IP routing table.
<!--more-->
Let's start with the easy part: conditional origination of a BGP default route. If you attach a route map to the **neighbor default-originate** router configuration command then the default route will be sent to the specified neighbor only when the configured route map matches at least one prefix in the *IP routing table*. The catch is in the "*match in the IP routing table*" part -- you cannot use any of the BGP attributes as matching criteria in the route map.

Here's a simple example: if the IP prefix 10.255.255.7/32 is in the IP routing table, the BGP default route will be sent to BGP neighbor 10.0.7.9. I'm using a loopback interface to generate the host route; you could easily create a [track-object-based static route to *null 0*](/2011/09/shut-down-bgp-session-based-on-tracked.html) and use EEM (or any other mechanism) to change the state of the track object.

``` {.code}
interface Loopback202
 ip address 10.255.255.7 255.255.255.255
!
router bgp 65000
 neighbor 10.0.7.9 remote-as 65100
 neighbor 10.0.7.9 default-originate route-map CheckDefault
!
ip prefix-list CheckDefault seq 5 permit 10.255.255.7/32
!
route-map CheckDefault permit 10
 match ip address prefix-list CheckDefault
```

Chris already had a great idea how to solve the problem:

> I\'d really like to use that sort of construct to match AS-paths: If I see ASes belonging to Google, Facebook, etc, then that\'s probably a good sign.

There's a way to check whether paths from a certain AS are in the BGP table without listing the whole table -- the **show ip bgp paths** command. The AS paths are stored in a hash table (to save memory) and this **show** command dumps the AS paths table without walking through the whole 350.000 routes (or whatever the BGP table size might be when you read this article).

You can use the **show ip bgp paths** command in an EEM applet combined with an output filter matching individual AS numbers you're interested in to change the state of a track object (and thus influence the IP routing table).

For example, you could use **show ip bgp paths \| include \_(32934\|13413)\_** to display paths containing Facebook's or Twitter's AS (two most important parts of the Internet in some people's opinion) in your BGP table and check for the presence of '0x' string (which is always present in a non-empty **show ip bgp paths** printout).

However, even the **show ip bgp paths** command burns a lot of unnecessary CPU cycles which you might need for more useful things on your PE-routers. It's best to offload the Internet connectivity test to a central server; you can do it on your route reflector or you could deploy a BGP daemon on a Linux host, check the BGP tables there, and insert (or revoke) a BGP prefix that signals all PE-routers to send (or revoke) the BGP default route. In case you want to go down this path it might be worth watching the free [FRRouting Architecture and Features](https://www.ipspace.net/FRR) webinar.
