---
date: 2020-12-05 07:06:00+00:00
high-availability_tag: need
series_weight: 500
tags:
- high availability
title: 'Interesting: Differential Availability'
series_title: 'Differential Availability'
---
Someone pointed me to a [high-level overview of Google's Spanner database](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/45855.pdf) which included this gem:

> A second refinement is that there are many other sources of outages, some of which take out the users in addition to Spanner (“fate sharing”). We actually care about the differential availability, in which the user is up (and making a request) to notice that Spanner is down. This number is strictly higher (more available) than Spanner’s actual availability — that is, you have to hear the tree fall to count it as a problem.

In other words, it doesn't matter if your distributed database fails if its user are also gone. Keep this concept in mind every time you're designing a high availability solution -- some corner cases are simply not worth solving.