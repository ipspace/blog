---
title: "BGP Labs: Multivendor External Routers"
series_title: "Choose External Routers from Five Different Vendors"
date: 2023-10-25 05:50:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
A quick update [BGP Labs project](https://bgplabs.net/) status update: now that [netlab release 1.6.4](/2023/10/netlab-1-6-4-more-bgp-nerd-knobs.html) is out I could remove the dependency on using Cumulus Linux as the external BGP router.

You can use any device that is supported by **[bgp.session](https://netlab.tools/plugins/bgp.session/)** and **[bgp.policy](https://netlab.tools/plugins/bgp.policy/)** plugins as the external BGP router. You could use Arista EOS, Aruba AOS-CX, Cisco IOSv, Cisco IOS-XE, Cumulus Linux or FRR as external BGP routers with netlab release 1.6.4, and I'm positive Jeroen van Bemmel will add Nokia SR Linux to that list.

If you're not ready for a _netlab_ upgrade, you can keep using Cumulus Linux as external BGP routers (I'll explain the behind-the-scenes magic in another blog post, I'm at the [Deep Conference](https://deep-conference.com/) this week).

For more details read the updated [BGP Labs Software Installation and Lab Setup](https://bgplabs.net/1-setup/) guide.
