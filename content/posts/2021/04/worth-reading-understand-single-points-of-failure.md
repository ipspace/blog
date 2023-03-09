---
date: 2021-04-25 07:53:00+00:00
dr_tag: other
high-availability_tag: dr
series:
- dr
series_title: Understand Your Single Points of Failure
tags:
- high availability
- cloud
- design
title: 'Worth Reading: Understand Your Single Points of Failure'
---
I've been saying the same thing for years, but never as succinctly as Alastair Cooke did in his 
[*Understand Your Single Points of Failure (SPOF)*](http://demitasse.co.nz/2021/04/aws-principles-understand-your-single-points-of-failure/) blog post:

> The problem is that each time we eliminated a SPOF, we at least doubled our cost and complexity. The additional cost and complexity are precisely why we may choose to leave a SPOF; eliminating the SPOF may be more expensive than an outage cost due to the SPOF.

Obviously that assumes that you're able to follow business objectives and not some artificial measure like uptime. Speaking of artificial measures, you might like the discussion about [taxonomy of indecision](https://rule11.tech/the-hedge-76-frederico-lucifredi-and-the-taxonomy-of-indecision/).