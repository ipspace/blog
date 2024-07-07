---
date: 2008-08-26 07:07:00+02:00
tags:
- RIP
title: RIP route database
url: /2008/08/rip-route-database/
---
Did you know that RIP, the venerable routing protocol that is present in Cisco routers for the last 20 years, uses an internal database, not the IP routing table, to process RIP updates? This database contains no fancy information (like EIGRP topology table) that would allow RIP to converge faster, but there are still minor differences between the RIP database and the IP routing table.

The article in which I described that feature is long gone, but fortunately [archive.org saved the day](https://web.archive.org/web/20170803035921/http://wiki.nil.com/RIP_Route_Database).

{{<ct3_query>}}
