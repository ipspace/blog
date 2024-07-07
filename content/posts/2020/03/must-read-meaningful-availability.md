---
date: 2020-03-21 14:20:00+01:00
high-availability_tag: need
series_title: Meaningful Availability
series_weight: 510
tags:
- high availability
title: 'MUST READ: Meaningful Availability'
url: /2020/03/must-read-meaningful-availability/
---
Defining service availability using the [famous X nines](https://en.wikipedia.org/wiki/High_availability#%22Nines%22) (and all the hacks like "planned downtime doesn't count") is pretty useless in a highly distributed system where the only thing that really matters is the user experience, not ping response times. One should ask *what precisely should we be measuring, and how could we make sure we can act on the measurements*

More details in a [concise analysis](https://blog.acolyer.org/2020/02/26/meaningful-availability/) of the [Meaningful Availability paper](https://www.usenix.org/system/files/nsdi20spring_hauer_prepub.pdf) by the one-and-only [The Morning Paper](https://blog.acolyer.org/).
