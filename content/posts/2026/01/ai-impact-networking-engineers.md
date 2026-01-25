---
title: "Opinion: Impact of AI on Networking Engineers"
date: 2026-01-29 08:04:00+0100
tags: [ AI ]
ai_tag: opinion
---
A friend of mine sent me a series of questions that might also be on your mind (unless you're lucky enough to live under a rock or on a different planet):

> I wanted to ask you how you think AI will affect networking jobs. What's real and what's hype?

Before going into the details, let's make a few things clear:
<!--more-->
* AI is way more than just neural networks or Large Language Models (LLM). People have been working on AI technologies and solutions for decades, and have developed all sorts of useful tools, most of which are unknown to the general public. See the [Machine Learning for Network and Cloud Engineers](/2023/02/machine-learning-network-cloud/) book for a few examples.
* Any AI technology (or product) is just a tool, and like any other tool, has to be used correctly. It also helps if you understand what the tool does, how it works, and its limitations[^EWTM]. The [AI Networking Cookbook](https://www.packtpub.com/en-gb/product/ai-networking-cookbook-9781805807995) by Eric Chou might give you a few ideas.
* More and more AI researchers[^PEP] agree that standalone Large Language Models are a dead-end, which does not mean they are not useful as a front-end to a more powerful system (they absolutely are). Gary Marcus has [a lot to say](https://garymarcus.substack.com/) about that topic (for example, [here](https://garymarcus.substack.com/p/lets-be-honest-generative-ai-isnt), [here](https://garymarcus.substack.com/p/breaking-sir-demis-hassabis-becomes), and [here](https://garymarcus.substack.com/p/further-breaking-news-further-vindicating))[^AISDN]

[^EWTM]: Yeah, I know I'm expecting way too much from the world with the attention span of a squirrel.

[^PEP]: As opposed to pundits, Kool-Aid consumers, evangelists, and product managers

[^AISDN]: His blog posts often remind me of my OpenFlow/SDN blog posts. Everyone with enough experience knew that was a stupid idea that would never work in real life, but nobody wanted to point out the (lack of) state of the Emperor's clothes.

> It seems to me like AI is the new bootcamps, meaning that there are a lot of grifters out there promising success and proudly promising the demise of humans.

Hey, whenever there's hype and anxiety, you get a mix of well-meaning people peddling quick recipes[^QR], attention grabbers, "influencers", grifters, and scammers. Figuring out who's who is the fun part.

[^QR]: Paraphrasing [H. L. Mencken](https://quoteinvestigator.com/2016/07/17/solution/): for every technology challenge, there's a solution that is clear, easy, and wrong.

> I use LLMs every day, for things like transforming data, spotting where I made typos or simple mistakes, asking about error messages, and so on, but that's easier to do if you already have expertise in something, of course.

So do I. It would be a shame not to use a tool that could make your life easier (like Google Maps), help you get better results (like Grammarly), or help you get the job done faster (like Excel ;) However, you usually need time[^NT] to use a tool optimally, and I think we're still far away from that point with LLMs.

[^NT]: As in experiencing enough mistakes/blunders and learning from them

>  I fear for the beginners that don't have the experience or knowledge to tell the LLM when it's hallucinating, that they keep hearing "You're right" all the time, and that they could end up with massive gaps in their knowledge.

Hey, remember the "copy/paste from Stack Overflow" crowd? There's no difference between that crowd and the "copy/paste from ChatGPT" crowd, apart from a psychological blind spot that can result in a perfect ~~FUBAR~~ storm::

* Because LLMs produce intelligent-looking results, we believe they must be intelligent.
* We also learned that the computers are not wrong, so whatever an LLM produces must be right. Right? After all, Excel is never wrong[^ICPU], it's always your fault[^EYF]. [Oh, wait](https://www.joelonsoftware.com/2007/09/26/explaining-the-excel-bug/)...

[^ICPU]: [Intel CPU might be](https://en.wikipedia.org/wiki/Pentium_FDIV_bug), though

[^EYF]: Resulting in [errors in ~20% of gene-related peer-reviewed papers](https://en.wikipedia.org/wiki/Microsoft_Excel#Conversion_problems).

> Maybe that's just what every generation of grumpy old people think, though :)

Every (young) generation has a few people who want to understand how things work, work hard to get there, and usually reap some benefits of their hard work[^NBJ]. It also has plenty of people believing in miracles[^WL], quick recipes for success[^QRS], and self-help books[^SHB]. Surprisingly, some of the latter remain mediocre and often blame bad luck or external forces beyond their control.

[^WL]: Winning a lottery is an evergreen sure way to get rich

[^NBJ]: Not being a jerk also helps ;)

[^QRS]: More than half of the guys in my primary school class wanted to become mechanics. Today, they'd probably aim for influencers or some such. The belief in quick paths to success never stops.

[^SHB]: The fact that there are so many different self-help books and that new ones keep being published should tell you something.

Likewise, every generation of grumpy old people bemoans how kids these days don't understand the fundamentals. Some of that is true for some of the kids (the copy-paste crowd), but it's also true that some fundamentals are no longer relevant when the layers of abstraction [stop leaking](https://en.wikipedia.org/wiki/Leaky_abstraction). For example, decades ago, I was able to:

* Understand how transistors work, and build logic circuits out of discrete transistors or low-level components like NAND gates.
* Understand how integrated circuits work, and how you manufacture them.
* Know way too many details of modem- and Ethernet encoding schemas
* Design and build (wire-wrap) my own computer
* Port a compiler to that computer
* Build a network interface card
* Write my own file server operating system in assembly language on an 8-bit CPU with 64K of RAM
* Create my own interpreted language from scratch[^PGH] (think Python, but focused on simplifying forms-based UI)
* Create simple AI systems

[^PGH]: I still have the sources in Turbo Pascal. Let me know if you want to have them available on GitHub ;)

Is any of that relevant to whatever we have to do today? Of course not. (Almost) Nobody wants to know how a compiler or an operating system works these days.

Coming back to more relevant topics:

> What part of a networking job could a LLM do? What would you trust it to do in production? Do you think we are going to see agents operating networks?

Using AI in networking is not too different from deploying network automation, and some of my Introduction to Network Automation slides are still relevant, for example:

* Start with low-hanging fruits and read-only access[^ROA]
* Use protective measures on devices (role-based access control) to prevent inadvertent changes
* Until you're sure things work, keep an operator in the loop to confirm the actions an LLM suggests.

[^ROA]: With guardrails and rate limits -- you don't want an LLM blast your network into oblivion with an SNMP Query DOS.

For example, analyzing past tickets to identify the most likely root causes and using that analysis to generate troubleshooting suggestions could be a pretty interesting use case. Identifying devices that could be involved in a (perceived[^ATN]) network outage and collecting and analyzing initial troubleshooting information would be a huge boon. Even having a system that would write a detailed "this is why it's not the network" explanation in a bogus ticket[^CPROP] would be a major win 🤪

[^ATN]: It's always the network, most often BGP or DNS

[^CPROP]: Caused, for example, by a printer running out of paper

Finally:

> I don't know if you've seen some posts lately about agents being used as routers, speaking BGP and OSPF, kind of seems like stupid router tricks to me, but maybe there is a use case.

That's a pure publicity stunt, and light-years away from a sane, well-engineered solution. Collecting BGP or OSPF data in some [controlled](/2013/08/virtual-appliance-routing-network/) and [secured way](/2016/03/dont-run-ospf-with-your-customers/) (one-way BGP session, BGP-LS, or BMP), exporting that into some usable format, and then having an AI agent work on that data would make perfect sense, and might even be useful. On the other hand, using an AI agent to run a control-plane protocol like BGP or OSPF is approximately as efficient as using a [Rube Goldberg machine](https://en.wikipedia.org/wiki/Rube_Goldberg_machine) to make your morning coffee.
