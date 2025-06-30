---
title: "Start netlab Tools without Changing Topology File"
date: 2025-06-30 09:14:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
[Dan Partelly](https://github.com/DanPartelly) figured out that we [have to configure](https://github.com/ipspace/netlab/pull/2463) the [standard (IETF)](https://datatracker.ietf.org/doc/html/rfc5303) 3-way IS-IS handshake on old IOSv images. On the other hand, [all IS-IS integration tests pass](https://release.netlab.tools/_html/iosv-libvirt-isis) for IOSv and IOSvL2. I wondered what was going on.

Fortunately, a few months ago, I spent some time installing the client-side Edgeshark components on my laptop. All I needed to do was enable the [**edgeshark**](https://netlab.tools/extool/edgeshark/) tool in my lab topology and restart the lab.
<!--more-->
I already had the lab topology that would replicate the problem -- the "[network types](https://github.com/ipspace/netlab/blob/dev/tests/integration/isis/10-network.yml)" IS-IS integration test -- and I wanted to use it without modifying it. Obviously, I could copy it into another file and modify that one, but that's how you end up with a thousand twisty little files, all alike.

However, there's always another nerd knob&trade;. *netlab* allows you to [enable an external tool](https://netlab.tools/extools/#enabling-tools-in-user-defaults) *in all lab topologies* with a default setting, and you can [specify a default setting in an environment variable](https://netlab.tools/defaults/#changing-defaults-with-environment-variables). All I had to do to enable *Edgeshark* integration was:

```
$ export NETLAB_TOOLS_EDGESHARK_ENABLED=True
```

A few minutes later, I had an answer to my initial question: at least FRRouting and Arista EOS ignore the missing sub-TLVs in the P2P IS-IS hello messages and happily establish adjacency with a Cisco router sending pre-standard content.