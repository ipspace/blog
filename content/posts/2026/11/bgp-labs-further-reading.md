---
title: "Help Me Make the BGP Labs Even Better"
date: 2026-11-03 08:24:00+0100
tags: [ BGP ]
---
I decided to add "Further Reading" sections to BGP lab exercises, containing links to vendor documentation and useful related blog posts. I naively expected to offload the job to Claude, commit the results, and move on. The "related blog posts" were a piece of cake; precise links to relevant vendor documentation turned out to be more of a challenge.

**TL&DR:** I would love to get your suggestions for further reading as PRs in the [BGP Labs repo](https://github.com/bgplab/bgplab).

Apart from FRRouting, the vendor documentation is mostly generated from whatever internal system and uses auto-generated anchors that can change at any moment -- somewhat "suboptimal" for what I wanted to do.
<!--more-->
Also, a lot of times it starts with "and then there was this protocol called BGP," goes into tons of details that are irrelevant when you want to configure (for example) a BGP neighbor, and gets to the **neighbor** command ~20 pages later. Great if you want to master BGP in one go, not so good if you believe in the "eating the elephant one bite at a time" approach.

However, while Claude did a good job with "related blog posts", I would love more diversity. It seems Claude knows who's paying for the subscription 😜, so it uses a lot of mine, but I never wrote entry-level content. I did set a few [somewhat strict](https://github.com/bgplab/bgplab/blob/master/.claude/skills/lab-further-reading/SKILL.md#4-find-blog-posts) rules on what's acceptable, but I doubt there's *nothing* out there explaining the basics of BGP without ads plastered all over the page.

I know most of you are well beyond the CCNA/CCNP stage of your career, but you might still have a few useful links stashed somewhere from those days. It would be great if you could add them to the relevant lab exercises (or, even simpler, [open an issue](https://github.com/bgplab/bgplab/issues) saying "these links would be relevant for this exercise").

Adding the links shouldn't be too hard:

* Open any lab exercise on [bgplabs.net](https://bgplabs.net/)
* Click the "View on GitHub" link in the left-hand sidebar
* Click on the "edit this file" button (the pencil in the right-hand corner just above the heading text).
* Make your changes in the "Further Reading" section
* Click the "commit changes" button and let GitHub guide you through the process of submitting a PR.

The labs are (as you know) free and open-source and will remain that way (no ads, no monetization, no enshittification), so the budget to motivate contributors is zero to 9 decimal places, apart from the warm and fuzzy feeling you might get, and a mention in the contributors list.

However, if we happen to meet in person, the first beer is on me ;)

### Revision History

2026-11-03:
: Claude did a surprisingly good job with "related blog posts", so I rewrote bits of the original blog post.
