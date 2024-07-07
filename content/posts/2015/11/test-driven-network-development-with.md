---
cicd_tag: podcast
date: 2015-11-13 08:01:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_44-Test-Driven_Network_Development.mp3
series:
- cicd
series_weight: 100
tags:
- podcast
- SDN
- network management
- Software Gone Wild
title: Test-Driven Network Development with Michael Kashin on Software Gone Wild
url: /2015/11/test-driven-network-development-with/
---
Imagine you'd design your network by documenting the desired traffic flow across the network under all failure conditions, and only then do a low-level design, create configurations, and deploy the network... while being able to use the desired traffic flows as a testing tool to verify that the network still behaves as expected, both in a test lab as well as in the live network.
<!--more-->
Later on, as you make changes to the network, the unit tests you wrote (yeah, that's how software developers call this stuff) allow you to verify the change you made didn't break the network connectivity.

Finally, imagine having to work on an unknown network with thousands of accumulated quirks. Starting with unit tests (expected traffic flows) will help you understand the network, and give you a verification tool at the same time.

Michael Kashin built an Ansible-based tool that allows you to do all of that and is using it to work on the networks of his clients. He explained how it works in [Episode 44](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_44-Test-Driven_Network_Development.mp3) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild). For more details, [visit his blog](http://networkop.github.io/), in particular these blog posts:

-   [Building a simple network TDD framework](http://networkop.github.io/blog/2015/06/15/simple-tdd-framework/)
-   [Quick start](http://networkop.github.io/blog/2015/07/17/tdd-quickstart/)
-   [Verifying TDD scenarios](http://networkop.github.io/blog/2015/07/10/test-verification/)

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_44-Test-Driven_Network_Development.mp3){{</jump>}}

