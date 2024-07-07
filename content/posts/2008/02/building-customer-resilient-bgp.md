---
date: 2008-02-29 06:44:00.008000+01:00
tags:
- BGP
title: Building Customer-Resilient BGP networks
url: /2008/02/building-customer-resilient-bgp/
---
When [Kate Gerwig](http://searchtelecom.techtarget.com/meetEditorial/0,289131,sid103,00.html), my wonderful editor from [SearchTelecom.com](http://searchtelecom.techtarget.com/), and myself agreed on the contents of the "[Building customer-resilient BGP networks](http://searchtelecom.techtarget.com/tip/0,289483,sid103_gci1302784,00.html)" article, we had no idea that it would become extremely relevant just days before it was published. The article describes the tools a Service Provider should use to ensure that its customers cannot harm its BGP routing data (and consequently its other customers and the Internet at large).

On February 24th, someone in Pakistan decided to block local access to YouTube ... and someone else decided that the best way to approach the problem was to block the whole world's access to YouTube.
<!--more-->
YouTube (AS 36561) advertises its networks as nicely aggregated IP prefixes (one /20, one /22, one /19 and one /24). The hijackers decided to block the /22 range by announcing more specific (/24) prefixes. Their upstream provider had no filters in place and accepted these prefixes (BIG mistake). They soon propagated throughout the Internet, until someone in YouTube noticed them and started originating the same /24 prefixes.

{{<note info>}}In-depth analysis of the incident including an animation of the BGP changes is [posted on the RIPE NCC web site](http://www.ripe.net/news/study-youtube-hijacking.html).{{</note>}}

Since YouTube is way better connected to the major Internet providers as the offenders, from most points in the Internet the AS paths of the YouTube-originated prefixes were shorter than the ones the hijackers used, resulting in corrected routing. Ten minutes later, YouTube started announcing even more specific prefixes (/25) that completely restored connectivity to their servers.

I'm just guessing that someone had to remove the usual filters that drop the /25 (and longer) prefixes from being accepted from the customers in the meantime (Good work!).

The big debate people are having these days is: "can anything be done to stop this". Of course there is a solution: major Service Providers use [Internet Routing Registries](http://www.irr.net/) and document their autonomous systems, routes and routing policies (and [every AS should be doing the same](http://www.irr.net/docs/faq.html)). However, the solution is not enforced globally and while some Service Providers use the registries to build filters for their customers, no-one is willing to pull the plug and implement the filtering policies on all ingress/egress points.

Unfortunately, you cannot implement the IP prefix filters on major exchange points, as there's no reasonable way you could download the prefix lists covering the full Internet routing table into the routers and filter hundreds of thousands of IP prefixes. The last chance to implement the filters is on the regional level.
