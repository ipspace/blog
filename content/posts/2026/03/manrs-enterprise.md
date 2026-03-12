---
title: "MANRS for Enterprise Customers"
date: 2026-03-17 08:13:00+0100
tags: [ Internet, security ]
---
In October 2023, I was [talking](https://blog.ipspace.net/2023/11/rapid-progress-rpki-route-origin-validation/) about [Internet routing security](https://my.ipspace.net/bin/list?id=BGPSec) at the DEEP conference in Zadar, Croatia. After explaining the (obvious) challenges and the initiatives aimed at making Internet routing more secure ([MANRS](https://manrs.org/)), I made my usual recommendation: vote with your wallet. However, if you're a company in Croatia (or Slovenia, or a number of other countries), you're stuck.

While ISPs in Croatia might be doing a great job, none of them is a [MANRS participant](https://manrs.org/netops/participants/)[^SCC], so we don't know how good they are. The situation is not much better in Slovenia; the only ISPs claiming to serve Slovenia are Anexia (a cloud provider) and Go6 Institute, the small network operated by my good friend (and True Believer in IPv6 and MANRS) [Jan Žorž](https://www.linkedin.com/in/janzorz/). Moving further north, I was unable to get any useful data for Austria, as its country code (AT) also matches "No Data" string in MANRS table, resulting in over 500 hits.
<!--more-->
[^SCC]: The "MANRS participants" web page is awful; it does not allow you to search for participants serving a particular country. The best I could do was to search for "HR", the country code for Croatia, and got an ISP from Ba**hr**ain and a C**hr**istian high school 🤦‍♂️

I'm positive all ISPs in countries with no MANRS participants[^SM] have a wonderful (bullshit) excuse: nobody is asking for MANRS compliance, so why should we spend any time on it -- the usual chicken-and-egg approach to security and compliance. No wonder things never move forward.

[^SM]: At least those that can spell MANRS

Anyway, if you do believe in *voting with your wallet* and *making your suppliers uncomfortable*, you might want to read the "[Internet Routing Supply Chain: An Enterprise’s Most Overlooked Dependency](https://manrs.org/2026/02/the-internet-routing-supply-chain-an-enterprisess-most-overlooked-dependency/)" white paper recently published by MANRS. They correctly identified the potential pressure point (connectivity buyers); the "only" thing left to do is to make enterprise buyers aware of the benefits of MANRS compliance. Maybe it's time to ask Jan Žorž and his friends (who made [RIPE-501/544 pretty successful](https://blog.ipspace.net/2012/06/choose-your-networking-equipment-with/)) for a few hints.
