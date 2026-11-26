---
date: 2019-05-24 08:04:00+02:00
series: vagg
tags:
- Internet
- BGP
- IP routing
title: If You Worry About 768K Day, You’re Probably Doing Something Wrong
url: /2019/05/if-you-worry-about-768k-day-youre/
vagg_tag: basics
---
A few years ago we "celebrated" 512K day - the size of the full Internet routing table exceeded 512K (for whatever value of K ;) prefixes, overflowing TCAMs in some IP routers and resulting in interesting brownouts.

We're close to exceeding 768K mark and the *[beware 768K day](https://blog.thousandeyes.com/what-is-768k-day/)* blog posts have already started appearing. While you (RFC 2119) SHOULD check the size of your forwarding table and the maximum capabilities of your hardware, the more important question should be "*Why do I need 768K forwarding entries if I'm not a Tier-1 provider*"
<!--more-->
I [wrote about this topic a long while ago](/2010/09/virtual-aggregation-quick-fix-for/) and [again around 512K day](/2014/08/do-you-really-need-to-see-all-512k/), and [David Barroso proved you don't need more than \~100K entries to cover 99.99% of the traffic of a very large content provider](/2015/01/sdn-router-spotify-on-software-gone-wild/) (and even less if you're peering at an IXP), but it seems people still don't want to grasp the details, so let's try again:

- You need the full Internet routing table if you're within the Default Free Zone (DFZ);
- You have to be in the DFZ if you're not getting transit from an upstream provider, otherwise it's easier to use a default route toward your upstream.
- The only exception to the previous bullet is dealing with multiple upstream providers that don't want to talk to each other and play de-peering chicken games (see also: Cogent). If that's the case, switch the providers.

A very large majority of autonomous systems thus don't need the full Internet routing table, but that doesn't mean that you should blindly follow a default route toward your upstream provider. As the very minimum, you should:

- Accept prefixes for upstream providers' customers directly from the upstream providers (hint: check whether the AS path contains two or three distinct AS numbers);
- Use default routes that rely on reachability of a third-party prefix (hint: 8.8.8.8 or 1.1.1.1 if you don't trust Google);

Alternatively, you could decide to use a default route toward your primary upstream provider, and install only the prefixes received from other upstreams or peering partners into your forwarding table.

{{<note>}}
Your device must support filters between the BGP table, IP table, and forwarding table for this approach to work. Most decent networking operating systems have such functionality.
{{</note>}}

Finally, you could use the approach David Barroso pioneered (and a vendor or two later promoted as the best thing they ever figured out):

- Use the full Internet routing table together with NetFlow data to figure out which autonomous systems matter to you.
- Install those prefixes (plus potential exceptions) into the forwarding table and use the default route(s) for everything else.

Of course it's easier to request full routing table from all upstreams, yammer when the BGP convergence takes forever (because the \$0.99 CPU in your ancient switch has a hard time dealing with the changes), or blame the vendor for the too-small TCAM size.

Alternatively, you could decide to get the job done, in which case you might want to listen to Software Gone Wild episodes *[SDN Router @ Spotify](/2015/01/sdn-router-spotify-on-software-gone-wild/)* and *[SDN Internet Router Is in Production](/2015/10/sdn-internet-router-is-in-production-on/)*, and watch the *[Forwarding Optimizations](https://my.ipspace.net/bin/list?id=SDNUseCases#Forwarding%20Optimizations)* part of *[SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases)* webinar.
