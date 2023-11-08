---
title: "Open BGP Daemons: There's So Many of Them"
date: 2023-11-08 08:02:00
tags: [ BGP, security ]
---
A while ago, the *[Networking Notes](https://blog.computer-networking.info/)* blog published a link to my "*[Will Network Devices Reject BGP Sessions from Unknown Sources?](https://blog.ipspace.net/2023/10/reject-unknown-bgp-session.html)*" blog post with a [hint](https://blog.computer-networking.info/bgp-h3/): [use Shodan](https://www.shodan.io/search?query=port%3A179+product%3A%22BGP%22) to find how many BGP routers accept a TCP session from anyone on the Internet.

The results are appalling: you can open a TCP session on port 179 with over 3 million IP addresses.

{{<figure src="/2023/11/shodan-179.png" caption="A report on Shodan opening TCP session to port 179">}} 
<!--more-->
Most of those IP addresses immediately close the connection[^NP], but over 380.000 IP addresses send back BGP OPEN and BGP NOTIFICATION (go away) messages revealing the Router ID and Autonomous System Number (ASN).

[^NP]: not perfect, but not terribly wrong either. See the previous blog post for details.

{{<figure src="/2023/11/shodan-bgp.png" caption="Shodan got BGP messages from 380.000 IP addresses">}}

{{<figure src="/2023/11/shodan-router-id.png" caption="Did you know Telecom Italia uses private IP addresses for router IDs?">}}

To make matters worse, for Shodan to displays the BGP messages:

-   A BGP-speaking device must be reachable from the global Internet (not a good idea).
-   It must accept TCP sessions on port 179 from unknown IP addresses (bad, but that's how this world works).
-   It must be able to complete TCP session establishment, which means that it's sending BGP TCP packets with TTL much greater than one and not checking the incoming TTL (can't make a public comment, we're in the NSFW territory).
-   It must send a few BGP messages before closing the session. While there might be a number of open-source BGP daemons exhibiting that behavior, I found a [single networking vendor in that category in my tests](/2023/10/reject-unknown-bgp-session.html#ugly) (and yes, they do set TTL to 255 on EBGP sessions by default just to make sure they can reply to anyone who wants to talk with them).
  
The reality is probably less dramatic. Any BGP-speaking router might have dozens of interfaces with dozens of IP addresses you can reach from the Internet. Still, that's a lot of potentially vulnerable devices[^FUD].

[^FUD]: Don't tell me no networking vendor ever had a parsing bug that would cause the device (or routing daemon) to crash when receiving a well-crafted message. See [this blog post](https://blog.benjojo.co.uk/post/bgp-path-attributes-grave-error-handling) and [this presentation](https://www.blackhat.com/us-23/briefings/schedule/index.html#route-to-bugs-analyzing-the-security-of-bgp-message-parsing-32162) for some fun details.

Finally, Shodan allows you to limit your queries to organizations or IP prefixes. If you're running BGP in your network (in particular, if you're a service provider), do yourself a favor, check whether your routers are exposed to the Internet, and deploy a few ACLs on Internet-facing interfaces.
