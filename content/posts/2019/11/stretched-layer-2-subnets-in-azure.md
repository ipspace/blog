---
date: 2019-11-11 08:45:00+01:00
ha-cloud_tag: stretch
series:
- ha-cloud
tags:
- bridging
- Azure
- WAN
title: Stretched Layer-2 Subnets in Azure
url: /2019/11/stretched-layer-2-subnets-in-azure/
---
Last Thursday morning I found [this gem](https://twitter.com/NZ_BenThomas/status/1192089805146001408) in my Twitter feed (courtesy of [Stefan de Kooter](https://twitter.com/sdktr/status/1192214467498647554))

> Greg Cusanza in #BRK3192 just announced #Azure Extended Network, for stretching Layer 2 subnets into Azure!

As I know a little bit about how networking works within Azure, and I've seen something very similar a few times in the past, I was able to figure out what's really going on behind the scenes in a few seconds... and got reminded of an old Russian joke I found somewhere on Quora:
<!--more-->
> Have you heard that Ivanov won a thousand in a game of chess?\
> Sure thing. But it was Rabinovich, not Ivanov. It was a game of poker, not a game of chess. It was ten thousand and not one thousand. And, well, he lost, not won.
{#joke}

In this particular case, it's not layer-2 subnet but IP addresses, and it's not new, but just a productized solution that people were implementing for years, and it comes with all the usual caveats that I've been talking about for a decade.

So what's really going on? Here's the diagram I "borrowed" from Microsoft's presentation (hope they don't mind) because I'm still on the road and it's too cumbersome to create a new one...but eventually there will be one in my [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar and we'll definitely talk about this particular can of worms in [Networking in Public Clouds](https://www.ipspace.net/PubCloud/) course.

![](/2019/11/s640-Azure+Extended+Network.jpg)

Azure Extended Network does **not** stretch a layer-2 broadcast domain (that would be stupid) but a layer-3 IP subnet to implement not layer-2 clustering tricks but layer-3 IP mobility. As the regular readers of my blog know there's a [major difference between stretching layer-2 and implementing IP mobility](/2013/02/hot-and-cold-vm-mobility/) which can be done with a variety of tools, although [stretched VLANs are commonly used](/2018/01/revisited-need-for-stretched-vlans/) because people who just bought shiny new hammers on advice of their trusted vendors tend to see nails everywhere they look.

One of the not-so-well-known tools that can be used to [implement IP mobility](/2012/08/mobile-arp-in-enterprise-networks/) is [routing on host routes](/2015/04/rearchitecting-l3-only-networks/). After all, if you [advertise /32 or /128 prefixes for individual IPv4 or IPv6 addresses](/2016/12/building-l3-only-data-center-with/) you're no longer bound by default subnet-level summarization (I'm talking about that in the *Addressing* part of my *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar). You're also [turning IP into a bad clone of CLNP](/2015/05/reinventing-clns-with-l3-only-forwarding/) but that's beyond the point.

That's exactly what Azure Extended Network does:

-   IP addresses of on-premises hosts are configured as additional IP addresses on the Network Interface Card (NIC) of the Azure VM (using Azure orchestration system);
-   IP addresses of Azure hosts are configured as additional IP addresses of the NIC of on-premises VM.

Whenever an on-premises host tries to reach an Azure VM it sends out an ARP request, and the on-premises Extended Network VM replies to it.

Whenever an Azure VM tries to reach an on-premises host, the Azure Virtual Router sends the traffic to the *local* IP address which is owned by the Azure VM running Extended Network code.

The last thing you need to complete the picture is a tunnel between the on-premises VM and Azure VM to exchange IP traffic. They could have used any IP-over-IP tunneling protocol but decided to go with VXLAN. That decision might have been driven by any one of these:

-   Having an already-implemented device driver (most probable, as the presenter talked about using VXLAN driver with Hyper-V virtual switch);
-   VXLAN runs on top of UDP, so it's pretty easy to get it through firewalls. It's also easy to insert an internal load balancer in Azure and have two or more Azure VMs to increase performance;
-   Using dynamic MAC+IP learning from ARP requests forwarded over the VXLAN tunnel instead of having a proper control plane. Fortunately it's not this one - you have to add addresses manually (that part of presentation starts around 35:00... and the presenter was also hit with [slow Azure API](/2019/06/how-microsoft-azure-orchestration/)).

The [presentation in which they announced this "feature"](https://myignite.techcommunity.microsoft.com/sessions/82848?source=sessions) (start watching @ 22:00) was full of warnings and caveats (starts @ 27:00 - funniest ones being "oh, and you have to reduce MTU within your subnet" and "latency will be *a little* higher") closely matching what I've been saying for years, but I'm pretty positive a lot of people will stop listening after seeing "you can move your IP addresses into Azure cloud", implement the stuff, and let you deal with the consequences after they ran away chasing another squirrel, so get prepared for the fallout.

Finally, as for "*it's nothing new*" remark I made - I'm aware of at least two prior implementations using the exact same trick, one of them being offered as a commercial product a few years ago (if anyone remembers what that product was, please write a comment).
