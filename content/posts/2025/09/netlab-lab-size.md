---
title: "How Many Lab Devices Can netlab Handle?"
date: 2025-09-04 07:59:00+0200
tags: [ netlab ]
netlab_tag: use
---
**TL&DR:** Over 3000

A few weeks ago, [Christian](https://github.com/Muddyblack) opened an [issue](https://github.com/ipspace/netlab/issues/2603) describing how _netlab_ breaks when the lab topology has more than 250 devices. We fixed that, only to get into [another morass](https://github.com/ipspace/netlab/issues/2621): some code has complexity higher than O(n) (meaning that going from 100 to 200 devices makes things more than twice as slow). Christian is working on one of those problems at the moment (it's not that his ginormous labs won't start, it just takes a long time), and I decided it's time to polish a few other bits of the code.
<!--more-->
Another annoying problem Christian encountered was the slow execution of _netlab_ commands after the lab was started. For example, **netlab connect** (which is nothing more than a wrapper around **ssh** or **docker exec** command) took 14 seconds to connect to a lab device. The culprit was the _netlab_ snapshot file, which was stored in YAML format—parsing the file describing a 400-device lab took around 15 seconds on Christian's server.

I know YAML parsing is slow, so I wanted to change the encoding of the snapshot file to JSON. Fortunately, Stefano Sasso suggested [pickling](https://docs.python.org/3/library/pickle.html) the transformed data. I got that code working, and it reduced the time needed to read the transformed data (and recreate the objects) from [over five seconds](https://github.com/ipspace/netlab/discussions/2635#discussioncomment-14293098) to less than half a second.

In the meantime, Christian reported having a [running lab with over 3000 FRR containers](https://github.com/ipspace/netlab/discussions/2635#discussioncomment-14293601), while [Seb](https://github.com/sdargoeuves) has one with [~60 virtual machines](https://github.com/ipspace/netlab/discussions/2635#discussioncomment-14293369).

I don't think anyone has built a larger lab so far, and when we ship the fixed code (release 25.09 will be out in a week or two), the limiting factor for your labs will be the amount of RAM and CPU you have in your server, not _netlab_.