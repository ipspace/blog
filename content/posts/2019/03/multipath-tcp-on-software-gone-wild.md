---
date: 2019-03-22 10:24:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_100-Multipath_TCP.mp3
multihoming_tag: session
series:
- multihoming
tags:
- podcast
- TCP
- Software Gone Wild
title: Multipath TCP on Software Gone Wild
url: /2019/03/multipath-tcp-on-software-gone-wild.html
---
I mentioned Multipath TCP (MP-TCP) numerous times in the past but I never managed to get beyond "*this is the thing that might solve some TCP multihoming challenges*" We fixed this omission in [Episode 100](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_100-Multipath_TCP.mp3) of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild) with [Christoph Paasch](https://www.linkedin.com/in/christophpaasch/) (software engineer @ Apple) and [Mat Martineau](https://www.linkedin.com/in/matmartineau/) from Open Source Technology Center @ Intel.
<!--more-->
We started with the basics: what is MP-TCP, why should we care, and how it's used in end-user devices. Next step: how can we use MP-TCP stack available in user devices like iPhone and connect to a Linux server with MP-TCP... and once we got to the servers, the obvious question was "*can we use MP-TCP* *to get rid of MLAG?"* After that, we started exploring the usual rabbit trails, and you'll have to [listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_100-Multipath_TCP.mp3) to find out where they led us ;).

If you want to know even more, explore these links:

-   [Multipath TCP IETF working group documents](https://datatracker.ietf.org/wg/mptcp/documents/)
-   [Linux Kernel Multipath TCP Project](https://multipath-tcp.org/)
-   [Linux MPTCP Upstreaming Wiki](https://github.com/multipath-tcp/mptcp_net-next/wiki)
-   [Mailing list](https://listes-2.sipr.ucl.ac.be/sympa/info/mptcp-dev)

{{<jump>}}
[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_100-Multipath_TCP.mp3)
{{</jump>}}
