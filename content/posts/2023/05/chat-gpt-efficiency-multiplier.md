---
title: "Is ChatGPT an Efficiency Multiplier?"
date: 2023-05-10 06:29:00
tags: [ AI ]
ai_tag: opinion
---
I got this comment on one of my ChatGPT-related posts:

> It does save time for things like converting output to YAML (I do not feed it proprietary information), or have it write scripts in various languages, converting configs from one vendor to another, although often they are not complete or correct they save time so regardless of what we think of it, it is an efficiency multiplier.

I received similar feedback several times, but found that the real answer (as is too often the case) is *It Depends*.
<!--more-->
ChatGPT and other large language models are great tools if you have to produce large amounts of bland boilerplate text that could fit into a few bullets[^BYBF]. It's also not too awful when used to summarize that text[^GPU]. If that sounds like your job description, then ChatGPT is indeed an efficiency multiplier, and some people found it useful when generating reports or even [blog posts](https://martinfowler.com/articles/2023-chatgpt-tech-writing.html).

[^BYBF]: ... but you'd be fired if you failed to expand those bullets into a 50-page document.

[^GPU]: ... so we're burning tons of GPU cycles producing and 
summarizing bullshit just for the appearances. Lovely. It was probably cheaper (but less comfortable) when we had to wear suits and ties.

Unfortunately, what we're usually looking for in engineering is *knowledge management*, and most of the examples cited by my reader fall into that category. If you're looking for something simple, then ChatGPT might give you the correct answer, but the moment you need a solution to a more complex question, it quickly turns into an [overconfident intern](https://economistwritingeveryday.com/2023/04/17/chatgpt-as-intern/)[^EB] with no idea that some stuff it knows just isn't true[^LB]. 

[^EB]: ... or, as Daniel Dib put it, [an expert beginner](https://twitter.com/ioshints/status/1639897544485400576).

[^LB]: ChatGPT-4 is much better than the original ChatGPT, but as one of my friends put it, _the upgrade just moved the terminator line of bullshit_.

You can use what ChatGPT gives you as a starting point for your research, but I usually spend more time trying to fix its answer than I would have spent doing a more traditional search. For example, imagine you have to configure VLANs on an unknown platform. What do you think will work better:

* Find the *configure VLANs* document for that platform to get a rough idea of how to do it, and then search for individual configuration commands to figure out the details.
* Have an intern come up with a sample configuration and then try to fix the hard-to-spot errors (like missing **add** keyword in **switchport trunk allowed vlan** command).

The answer probably depends on how you're used to work, and some people might find it easier to fix stuff than to do the initial research, in which case an imprecise answer might be better than no answer, but unfortunately, I'm not wired that way.

Also, sometimes _maybe not too wrong_ might be good enough, or as my friend put it:

> I think it is more between “I do it myself with 95% probability of success” and “I pay someone else to do it with somewhat unknown probability of success (assumed higher than 95%, but it’s opaque)”. When these remaining 5% translate into real money, suddenly everything becomes a lot less critical :-) saw it again and again :-)

**Back to the basics:** it's unrealistic to expect a language model trained on an unknown dataset covering everything from social sciences to quantum physics to give precise answers like what you'd get from Excel[^CB].

As with any other tool, we should stop drinking the Kool-Aid (or ignoring progress) and use AI tools in a way that brings the best out of them, regardless of what the vendors promised. For example, we should use language models for language processing -- including relevant documentation (context) with the query often [produces much better results](https://www.buildon.aws/posts/well-arch-chatbot), as do external plugins like the [Wolfram plugin](https://www.wolfram.com/wolfram-plugin-chatgpt/). 

[^CB]: ... unless you're [hitting a CPU bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) or [sorting human genes](https://www.theverge.com/2020/8/6/21355674/human-genes-rename-microsoft-excel-misreading-dates).  