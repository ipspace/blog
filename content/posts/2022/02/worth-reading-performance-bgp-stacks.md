---
title: "Worth Reading: Performance Testing of Commercial BGP Stacks"
date: 2022-02-19 08:27:00
tags: [ BGP ]
---
For whatever reason, most IT vendors attach "_you cannot use this for performance testing and/or publish any results_" caveat to their licensing agreements, so it's really hard to get any independent test results that are not vendor-sponsored and thus suitably biased.

Justin Pietsch managed to get a permission to [publish test results of Junos container implementation](https://elegantnetwork.github.io/posts/BGP-commercial-stacks/) (cRPD) -- no surprise there, Junos outperformed all open-source implementations Justin tested in the past.

What about other commercial BGP stacks? Justin did the best he could: he published *[Testing Commercial BGP Stacks](https://github.com/netenglabs/bgperf2/blob/master/README.md#targets)* instructions, so you can do the measurements on your own.
