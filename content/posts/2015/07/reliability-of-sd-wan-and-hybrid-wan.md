---
date: 2015-07-21 11:17:00+02:00
tags:
- SD-WAN
- SDN
- WAN
title: Reliability of SD-WAN and Hybrid WAN Solutions
url: /2015/07/reliability-of-sd-wan-and-hybrid-wan/
sd-wan_tag: bc
---
My [*Business Case for SD-WAN* blog post](/2015/07/business-case-for-sd-wan/) received numerous comments pointing out the potential pitfalls of hybrid WAN, including reduced security, unreliable Internet services and denial-of-service attacks.

While all those comments are perfectly valid, I still think hybrid WAN (whether implemented with traditional technologies or SD-WAN products) makes perfect sense.
<!--more-->
However, [like with any new technology](/2015/03/response-why-technology-still-matters/), you have to [understand the fundamentals](/2015/03/you-must-understand-fundamentals-to-be/) of SD-WAN (or hybrid WAN) solutions, and use them correctly.

{{<note warn>}}If your CIO decides (in his infinite wisdom gained by reading vendor whitepapers and listening to product pitches) to replace MPLS/VPN circuits with SD-WAN-over-Internet solution, he'll eventually get the disaster he deserves. The same might happen to anyone believing VPN-over-Internet solution can be made as reliable as a more traditional WAN solution.{{</note>}}

Fortunately, we've been using solutions similar to SD-WAN for at least a decade, so we've already learned a few useful lessons.

### Internet Uplinks Are Unreliable

We all know a zillion things can go wrong with Internet uplinks (and [eventually they will](/2012/10/if-something-can-fail-it-will/)):

-   If a link that costs you \$100 a month is down, you have zero leverage with your ISP. It will be fixed... eventually;
-   If you're experiencing packet drops on that same uplink, sometimes the only thing you can do is change the ISP;
-   If someone decides to blast you with a DDoS attack, you're toast... unless you have a high-end router sitting at a large Internet exchange, or you're paying for DoS scrubbing service (which you should consider doing for your hub site).

On the other hand, it's amazing how well Internet usually works, so it would be a shame not to use it. Also, most traffic transported across enterprise WAN is not really mission-critical, and it's a waste of money to transport it across high-quality infrastructure.

**Long story short**: don't ever count on reliability or availability of your Internet uplinks (particularly at remote sites).

### Redundancy is King

The usual way of dealing with unreliable components is to use redundancy. Apply the same thinking to your hybrid WAN design.

Use a combination of MPLS/VPN and Internet VPN, or Internet VPN with 3G backup. Use multiple access methods, so the cable-seeking backhoe doesn't bring down all uplinks.

### Keep Calm and Be Prepared

I guess we all agree the Internet uplinks will eventually fail. At that moment it's important to

-   Have a working backup solution that *has been properly tested*. The last thing you need when your high-capacity links fail are routing loops and traffic blackholes;
-   Have enough bandwidth available on the backup path to carry mission-critical traffic, together with a mechanism that will block non-critical traffic (otherwise the non-critical traffic would hose the backup links).

There are numerous tricks you can use to be prepared. Some organizations send mission-critical traffic over MPLS/VPN WAN all the time to ensure the MPLS/VPN links have enough bandwidth to carry that traffic when the Internet uplinks fail; others monitor the state of backup links (which should be a standard procedure anyway).

{{<note info>}}Cisco IOS has a 3G MIB, so we were able to write a monitoring solution for one of our customers that would alert them (and their mobile operator) when the 3G signal strength deteriorated below acceptable level.{{</note>}}
