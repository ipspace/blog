---
title: "Applying BGP Policy Templates"
date: 2024-02-20 07:25:00+0100
tags: [ BGP ]
---
I got this question after publishing the [BGP Session Templates](https://blog.ipspace.net/2024/02/bgp-labs-session-templates.html) lab exercise:

> Would you apply BGP route maps with a peer/policy template or directly to a BGP neighbor? Of course, it depends; however, I believe in using a template for neighbors with the same general parameters and being more specific per neighbor when it comes to route manipulation.

As my reader already pointed out, the correct answer is *It Depends*, now let's dig into the details ;)
<!--more-->
Some BGP implementations (for example, Arista EOS) have a single object (*peer group*) that serves as a container for BGP neighbor parameters; others (for example, Cisco IOS XE) have *session* templates and *policy* templates. We'll ignore peer groups and focus on templates.

It's rare[^IJS] to use different *session* or *policy* parameters for IBGP neighbors. There's no good reason why an AS edge router would treat route reflectors differently, and route reflectors usually don't change route attributes anyway. Also, having a per-session MD5 password within an autonomous system is just asking for trouble (see also: just because you could doesn't mean you should).

[^IJS]: But feel free to do it to increase your self-esteem and job security 🤓

EBGP sessions in service provider networks seem to be a different beast[^DC]. You probably don't need more than just a few parameters on EBGP *sessions*. BFD comes to mind, but that's about it; you probably want to use a different MD5 password with every customer or peer. Routing policies are a different beast, though. You probably want the same routing policy applied to all routes received from or sent to your customers (or peers), with inbound prefix- or AS-path filters being an obvious exception.

Some BGP implementations allow you to apply prefix filters, AS-path filters, and route maps to the same neighbor, making your life relatively easy:

* Include generic filters (drop RFC 1918 address space, drop too-long AS-paths) in a route map that's part of the policy template. That same route map can also handle various BGP community schemes (marking route sources or geolocating them, setting the BGP local preference based on BGP communities...)
* Add neighbor-specific filters if you want to limit the accepted prefixes or AS paths (RPKI would be infinitely better, but that's a discussion for another day).

Other implementations are more limited and force you to use a route map to implement basic filters. Some of them (for example, Arista EOS and FRR) allow a route map to call (include) other route maps. You can use that functionality to:

* Create a common route map that implements shared routing policy
* Create per-neighbor route maps that filter incoming prefixes and then call the common route map.
* Apply per-neighbor route maps to individual BGP neighbors.

Finally, you might be forced to use a platform that requires route maps to implement simple filters but cannot chain route maps. Welcome to BGP consistency hell, where automation might be your only chance to stay sane.

[^DC]: We'll ignore the GIFEE scenarios in which vendor SEs promote using EBGP sessions between two spine and two leaf switches in a [leaf-and-spine fabric](https://blog.ipspace.net/series/dcbgp.html) *because all the hyperscalers build their networks this way*.