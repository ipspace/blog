---
title: "Rapid Progress in BGP Route Origin Validation"
date: 2023-11-07 06:27:00
lastmod: 2023-11-15 19:38:00
tags: [ BGP, security ]
---
In 2022, I was invited to speak about Internet routing security at the [DEEP conference](https://deep-conference.com/) in Zadar, Croatia. One of the main messages of the presentation was how slow the progress had been even though we had had all the tools available for at least a decade ([RFC 7454](https://datatracker.ietf.org/doc/html/rfc7454) was [finally published in 2015](/2015/02/rfc-7454-bgp-operations-and-security.html), and we [started writing it in early 2012](/2012/03/my-first-internet-draft-has-just-been.html)).

At about that same time, a [small group of network operators started cooperating on improving the security and resilience of global routing](https://www.manrs.org/about/history/), eventually resulting in the [MANRS initiative](https://www.manrs.org/) -- a great place to get an overview of [how many Internet Service Providers care about adopting Internet routing security mechanisms](https://www.manrs.org/netops/participants/).
<!--more-->
In September 2022, I took the list of [Tier-1 providers from Wikipedia](https://en.wikipedia.org/wiki/Tier_1_network)[^T1C], did a quick search on the [MANRS Network Operator Participants](https://www.manrs.org/netops/participants/) page, and came up with this slide[^CLP]:

[^T1C]: Please note that the Wikipedia list of tier-1 providers is changing over time. Fortunately, you can [view the history of changes](https://en.wikipedia.org/w/index.php?title=Tier_1_network&action=history).

[^CLP]: Click the slide to get a larger picture

{{<figure src="/2023/11/rov-september-2022.png" link="/2023/11/rov-september-2022.png">}}

I wasn't able to make it to Zadar -- I got COVID-19 a few days before the conference started -- but I did turn the presentation [into a webinar](https://www.ipspace.net/Internet_Routing_Security). As I delivered the webinar in April 2023, I updated that same slide, and the progress made in half a year was remarkable. I was also a bit skeptical that large organizations managed to make so much progress in such a short time.

{{<figure src="/2023/11/rov-april-2023.png" link="/2023/11/rov-april-2023.png">}}

The organizers of the DEEP conference were kind enough to invite me to have the same presentation this year, and of course, I updated that same slide. In the meantime, MANRS started measuring how thorough the ISPs were in signing their prefixes (RPKI) and registering them in the Internet Routing Registry (IRR), making the data more meaningful than just the "*I claim I do all of that*" declarations I had been skeptical about back in April.

{{<figure src="/2023/11/rov-october-2023.png" link="/2023/11/rov-october-2023.png">}}

A [recent MANRS blog post](https://www.manrs.org/2023/10/rovista-measuring-current-rov-protection/) delivered the icing (and the cherry) on the cake -- a group of academics [managed to measure how well individual autonomous systems use Route Origin Validation](https://dl.acm.org/doi/10.1145/3618257.3624806) (ROV) to block invalid prefixes. Almost all tier-1 service providers they were able to measure got the perfect score:

{{<figure src="/2023/11/rov-adoption-november-2023.png">}}

Even better: ROV adoption at the tier-1 level shields the autonomous systems using those tier-1 providers from distant shenanigans. However, it obviously cannot protect customers of a regional ISP from bogus announcements created in the same region.

If you want to know how well ROV protects end users, check out the work done by [Geoff Huston and his team](https://www.potaroo.net/ispcol/2023-11/measure-roas.html). They are using Cloudflare RPKI beacons (meaning the destination is always close to the end-user) and doing measurements from the web browsers. Here's their view of the worldwide ROV adoption:

{{<figure src="https://www.potaroo.net/ispcol/2023-11/roas-f3.png" caption="Worldwide ROV adoption (from potaroo.net)">}}

Now for some bad news: as is evident from the above map, the future is not evenly distributed. As I was preparing yet another BGP security presentation for an Italian conference, I used the results of the [RoVista measurement tool](https://rovista.netsecurelab.org/) to see whether Italian ISPs perform Route Origin Validation[^NPI], and the results were dismal:

{{<figure src="/2023/11/rov-adoption-italy.png" link="/2023/11/rov-adoption-italy.png">}}

Plenty of work still needs to be completed before we have secure and resilient Internet routing.

[^NPI]: Please note I'm not picking on Italian ISPs; I just wanted to show locally relevant data. We'd probably get similar results for most countries.
