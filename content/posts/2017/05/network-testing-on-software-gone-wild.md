---
cicd_tag: podcast
date: 2017-05-12 12:45:00+02:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_78-Network_Testing.mp3
series:
- cicd
series_weight: 500
tags:
- automation
- podcast
- Software Gone Wild
title: Network Testing on Software Gone Wild
url: /2017/05/network-testing-on-software-gone-wild/
---
Network automation and orchestration is a great idea... but how do you verify that what your automation script wants to do won't break the network? In [Episode 78](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_78-Network_Testing.mp3) of Software Gone Wild we discussed the intricacies of testing network automation solutions with [Kristian Larsson](https://twitter.com/plajjan) (developer of [Terastream](/2013/11/terastream-part-2-lightweight-4over6/) orchestration softare) and [David Barroso](http://www.ipspace.net/Author:David_Barroso) of the [NAPALM](/search?q=napalm) and [SDN Internet Router](/search?q=sdn+internet+router) fame.
<!--more-->
We started with unit tests (what they are and whether they are useful), and quickly moved on to interesting stuff: functional tests and integration tests, which become really useful when you use the automation or orchestration system to configure an actual virtual lab and verify its operation after it has been reconfigured.

The real problem of running tests in a virtual lab is time-to-test. Developers would love to see tests done in a few minutes to verify that nothing major has been broken with the recent changes, while full integration or regression test suite takes hours... and Kristian was kind enough to explain how they tackle that challenge, as well as how they use the same tests in Continuous Integration environment and production network.

Talking about Continuous Integration -- we discussed what it is, how it works, and why it makes sense.

There are tons of other challenge in testing networks, and we covered at least these:

-   Who defines the tests and who develops them?
-   How can you use mockups to speed up the tests?
-   How can you test the software on numerous software versions at the same time?
-   How do you roll out changes incrementally?
-   How do I start this journey and where do I start?

For more details, listen to [Episode 78](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_78-Network_Testing.mp3) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild), and check out the [VRNetLab project](https://github.com/plajjan/vrnetlab).

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_78-Network_Testing.mp3){{</jump>}}

