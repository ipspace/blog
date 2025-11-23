---
title: "netlab as the Universal Configuration Translator"
date: 2025-11-28 07:30:00+0100
tags: [ netlab ]
netlab_tag: overview
---
_[Dan Partelly](https://github.com/danpartelly), a heavy _netlab_ user (and an active [contributor](https://github.com/ipspace/netlab/graphs/contributors)), sent me this interesting perspective on how one might want to use _netlab_ without ever building a lab with it. All I added was a bit of AI-assisted editing; my comments are on a grey background._

---

In all podcasts and interviews I listened to, netlab was referred to as a "lab management solution". But this is misleading. It's also a translator, due to its ability to abstract devices, and can easily generate perfectly usable configs for [devices](https://netlab.tools/platforms/) or [technologies](https://netlab.tools/module-reference/) you have never worked on.
<!--more-->
{{<long-quote size="90">}}
Even better, while those configurations are not _vendor-approved_, they're thoroughly tested with almost 200 integration tests. You can explore the [tests](https://github.com/ipspace/netlab/tree/dev/tests/integration) and the [test results](https://tests.netlab.tools/) online.
{{</long-quote>}}

This is invaluable. It makes you money. I'm actually surprised that in all those podcasts, this aspect was never mentioned. They all miss the point. For example, do you speak Juniper? Not quite, but with those generated configs and your mind, you can feel confident taking a job.

{{<long-quote size="90">}}
I keep hoping that one day someone will create an MCP server that uses the tested configurations, or even generate them on the fly, to improve the reliability of LLM-generated device configurations.
{{</long-quote>}}

Have doubts? Don't worry; you can actually prove the configs work with Netlab validation tests. This can make you money today, instantly. And if you just need the configs, you don't even need to spawn a VM or container. Of course, the rest is on you. Keep cool and do the job.