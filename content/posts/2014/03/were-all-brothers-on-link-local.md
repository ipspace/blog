---
date: 2014-03-18 07:31:00+01:00
tags:
- IPv6
- security
title: We’re All Brothers on Link-Local
url: /2014/03/were-all-brothers-on-link-local.html
video_tag: ipv6sec
---
I was listening to [excellent opening presentation](https://www.ernw.de/download/TROOPERS_IPv6SecSummit_ERNW_IPv6_Structural_Deficits.pdf) Enno Rey had at [Troopers 2014 IPv6 security summit](https://www.troopers.de/troopers14/troopers14-ipv6-security-summit-2014/index.html) (he claimed he was ranting, but it sounded more like some of my polite blog posts) and when I've seen this slide I could literally hear a blog post clicking together in my head.

{{<figure src="/2014/03/s1600-We're+All+Brothers+on+Link+Local.jpg">}}

In short: IPv6 has many shortcomings, but this might not be one of them.
<!--more-->
### The Layer-2 Subnet Model Is Broken

You probably know my opinion on the [current layer-2 networking model](/2012/05/transparent-bridging-aka-l2-switching.html) -- apart from being a [single failure domain](/2012/05/layer-2-network-is-single-failure.html), it's also a [single security domain](/2013/04/compromised-security-zone-game-over-or.html).

We can either accept that fact (and work on hardening the end-systems), [split our oversized layer-2 domains into smaller ones](/2013/11/make-every-application-independent.html) (where all hosts in a smaller domain become totally equivalent from the security perspective), or implement a properly hardened network that:

-   Authenticates users before allowing them to connect to the network;
-   Assigns addresses to users in an auditable fashion;
-   Enforces source address checks on every packet sent by the user.

{{<note info>}}Come to think of it, we do have such a network implementation. It's called Fibre Channel.{{</note>}}

Of course, the networking industry took another approach:

-   [Pretending the problem doesn't exist](http://etherealmind.com/poster-eight-levels-vendor-acceptance/) until enough users started screaming;
-   Explaining how solving the problem breaks existing applications and is thus unreasonable;
-   Implementing layers of kludges on top of broken architecture (large-scale Ethernet subnets), resulting in overly complex solutions like [SAVI](http://demo.ipspace.net/get/D4%20-%20Source%20Address%20Validation%20Improvement.mp4).

Obviously, it's not just the vendors' problem. Plenty of customers are buying the cheapest possible switches and later complaining how securing them properly is impossible. Unfortunately, some of the really expensive switches aren't any more secure ;)

### Some Got It Right

There's a single company (AFAIK -- I hope you'll prove me wrong in the comments) that handles the layer-2/layer-3 boundary correctly, restoring the original meaning of [data-link layer](http://en.wikipedia.org/wiki/OSI_model#Layer_2:_data_link_layer) (before [bridges were invented](/2010/07/bridges-kludge-that-shouldnt-exist.html)): Microsoft's [Hyper-V Network Virtualization connects VMs straight to a layer-3 virtual switch](/2013/12/hyper-v-network-virtualization-packet.html) that block all rogue RA messages and terminates all ND exchanges. Amazon VPC and Juniper Contrail do something very similar, but only for IPv4.

Finally, there's always the option of putting every single user in its own subnet. Good luck with that -- your ops people and the switch vendors (who will run out of TCAM) will love you.

### Need More Information?

-   [IPv6 webinars](http://www.ipspace.net/IPv6) cover a wide range of IPv6 topics, including [IPv6 security](http://www.ipspace.net/IPv6_security);
-   The [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar includes information on forwarding tables (including the size of the IPv6 forwarding table) in numerous data center switches from top-10 vendors.
