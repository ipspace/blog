---
title: "On AI Agents Speaking BGP"
date: 2026-02-25 07:39:00+0100
tags: [ AI, BGP ]
ai_tag: rant
---
I guess your LinkedIn feed is as full of AI nonsense as mine is, so I usually just skip all that posturing. However, every now and then, I stumble upon an idea that makes sense... until you start to dig deeper into it.

There was this post about [AI agents speaking BGP](https://www.linkedin.com/posts/olofk_networkautomation-ai-keepautomationweird-activity-7418405774898417664-rNIN) with an associated [GitHub repo](https://github.com/stiltzkin10/bgp-ai-agent), so I could go take a look at what it's all about.

The proof-of-concept (so the post author) has two components:
<!--more-->
* A natural-language interface to BGP information (makes sense)
* A vibe-coded (so claims the author) BGP daemon.

That second part made me facepalm. We have several high-quality open-source BGP implementations[^OSB], and at least FRRouting (I haven't tested the others) can produce the required information in easy-to-consume (for machines) JSON format, in case you think that's easier to work with than text printouts[^JSB]. Adding a REST API in front of that (should one be so inclined) is a piece of cake.

[^OSB]: Plenty of IXPs are using one of them, and the Internet must be up and running, or you wouldn't be reading this.

[^JSB]: Some people disagree because of the inevitable bloat caused by text-to-JSON expansion.

Wouldn't it be better to use a well-maintained, field-tested, pretty scalable implementation and pair it with something that adds value (natural language interface) instead of trying to prove you can reinvent a rough approximation of a wheel? Why do people feel they have to do that?
