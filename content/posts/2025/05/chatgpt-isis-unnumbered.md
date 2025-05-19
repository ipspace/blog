---
title: "ChatGPT Strikes Again: IS-IS on Unnumbered Interfaces 🤦‍♂️"
date: 2025-05-24 08:36:00+0200
tags: [ AI ]
ai_tag: kick
---
In the last few days, I decided to check out how much better ChatGPT has gotten in the last year or two. I tried to be positive and was rewarded with some [surprisingly good results](https://blog.ipspace.net/2025/05/chatgpt-netlab-topology/). I even figured out I can use it to summarize my blog posts using prompts like this one:

> Using solely the information from blog.ipspace.net, what can you tell me about running ospf over unnumbered interfaces

And then I asked it about unnumbered interfaces and IS-IS, and it all went sideways:
<!--more-->
{{<figure src="/2025/05/chatgpt-isis-unnumbered.png">}}

I questioned its sanity...

> Wow, are you sure that Cisco IOS configuration works?

... and ChatGPT quickly backtracked (and then provided a working configuration):

> You're absolutely right to question the configuration example I provided earlier. Let's clarify the correct approach for configuring IS-IS over unnumbered interfaces on Cisco IOS.

Seriously? While I'm impressed with the progress LLMs have made, we're still stuck at the *sloppy [bullshitting](https://blog.ipspace.net/2024/07/worth-reading-chatgpt-bullshit/) overconfident intern* stage. If you don't know what you're doing, it will quickly send you down the wrong path, but then I guess that's no different from the well-known Google-and-Paste approaches to solving technical problems (also known as *throwing spaghetti at the wall to see what sticks*).
