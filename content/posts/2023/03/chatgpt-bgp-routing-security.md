---
ai_tag: kick
title: "ChatGPT on BGP Routing Security"
date: 2023-03-30 06:27:00
tags: [ BGP, security, AI ]
---
I wanted to include a few examples of BGP bugs causing widespread disruption in the [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) presentation. I tried to find what happened when [someone announced beacon prefixes with unknown optional transitive attributes](https://labs.ripe.net/author/erik/ripe-ncc-and-duke-university-bgp-experiment/) (which should have been passed without complaints but weren't) without knowing *when* it happened or *who* did it.

Trying to find the answer on Google proved to be a Mission Impossible -- regardless of how I structured my query, I got tons of results that seemed relevant to a subset of the search words but nowhere near what I was looking for. Maybe I would get luckier with a tool that's supposed to have ingested all the world's knowledge and seems to (according to overexcited claims) understand what it's talking about.
<!--more-->
Here's my first attempt ([original query](/2023/03/chatgpt-bgp-1.png)):

> When did someone testing the propagation of an unknown BGP attribute cause Internet-wide disruption?

And this is what ChatGPT replied:

> The incident you are referring to is commonly known as the "BGPmon hijack" or the "Indosat hijack" and it occurred on April 2, 2014. During this incident, an Internet Service Provider (ISP) in Indonesia, called Indosat, accidentally announced over 28000 BGP routes with an invalid "AS Path" attribute. This announcement was propagated to other ISPs, which in turn propagated it further, causing a ripple effect across the global routing system.

For those unfamiliar with BGP security: BGPmon is a service that monitors the state of global BGP tables from numerous vantage points and sends alerts when someone hijacks your prefixes. Andree Toonk (the author of BGPmon) had never heard of "BGPmon hijack," but we quickly figured out that *BGPmon* often appears close to *hijack *in various reports, so there we go ;)

There was an Indosat incident in April 2014, but it involved 417.000 prefixes (which admittedly is over 28000 but by a large margin). Still, it was a simple reorigination leak with rewritten AS path, not something involving unknown BGP attributes.

Moving on:

> The invalid AS Path caused some routers to incorrectly identify Indosat as the best path to certain IP prefixes, leading to a widespread disruption of Internet traffic. Many popular websites and online services became unavailable, and the incident affected users worldwide for several hours.

True, but irrelevant. Showoff.

Then I remembered someone shouting at RIPE on a mailing list at the time of the incident[^RD], so maybe it was caused by a RIPE researcher. Here's my next question ([original query](/2023/03/chatgpt-bgp-2.png)):

[^RD]: It was a Duke University experiment using RIPE infrastructure

> When did a RIPE researcher testing unknown BGP attributes cause Internet disruption?

ChatGPT acted like a perfect salesman (never say no, and try to bluff your way through if you don't know what you're talking about) and produced this gem:

> There was an incident in 2019 where a RIPE NCC (Network Coordination Centre) researcher caused a temporary Internet disruption while conducting an experiment related to BGP (Border Gateway Protocol) route propagation.

Nice, it looks like ChatGPT found what I was looking for. Let's see what it found:

> On June 6, 2019, RIPE NCC researcher Job Snijders conducted an experiment to test a new method for improving the security of BGP routing. As part of the experiment, Snijders announced a new, unassigned BGP attribute to a limited set of peers on the internet's border gateway protocol (BGP) routing system. The announcement was intended to only reach a small number of networks and not cause any disruption.

Not a single "fact" in the above paragraph is true (trust me, I asked Job). What happened on June 6th, 2019 was a leak in which a [Swiss data center colocation company leaked 70.000 routes to China Telecom in Frankfurt](https://www.manrs.org/2019/06/large-european-routing-leak-sends-traffic-through-china-telecom/) that happily propagated them further. Job is also not aware of ever causing such an outage. He was [involved with hunting down undocumented BGP attributes](https://www.rfc-editor.org/rfc/rfc8093.html) when working on large BGP communities, though.

But wait, it gets better:

> However, due to a mistake in the configuration of one of the networks that received the announcement, the attribute was propagated widely across the Internet, leading to widespread routing problems. Several major Internet service providers, including Comcast and Verizon, reported issues with network connectivity, and some users experienced service outages.

I'm positive another leak resulted in Comcast and Verizon reporting problems, but not in early June 2019.

The worst (or the scariest) part of my interaction with ChatGPT: it all looked reasonable. Job Snijders is working on improving BGP, and it's feasible that he might have been working with RIPE (he's a frequent presenter at RIPE meetings). The rest of the story sounds legit until you start verifying the claims (including sending it to Job) and could be easily believed. What a fun world we live in, and it will only get better when the next generation of AI starts training on AI-generated stuff. As a well-known podcaster kept saying: "_never let facts get in the way of a good story_."

### GPT-4 Is Still Hallucinating

The obvious question after being faced with ChatGPT nonsense is "_would GPT-4 fare any better?_" I'm in no hurry to know that, and am therefore not willing to pay for the privilege of discovering the answer, but Andrew Yourtchenko (of the [Happy Eyeballs](/2013/03/happy-eyeballs-happiness-defined-by/) fame) kindly offered to run the queries for me. GPT-4 survived the first query but ([like any decent salesperson](/2023/03/worth-reading-dangers-knowing-everything/)) couldn't resist adding irrelevant information:

{{<figure src="/2023/03/gpt4-1.jpg">}}

The second query caused another bout of hallucination, this time inventing a researcher we never heard about:

{{<figure src="/2023/03/gpt4-2.jpg">}}

### Bing Fares Much Better

I asked Bing Chatbot the same questions. It couldn't find anything related to the first query (because the disruption wasn't Internet-wide):

> I’m sorry but I couldn’t find any information about the specific event you mentioned. However, there have been instances where BGP misconfigurations have caused internet-wide disruptions. BGP is what makes data routing on the internet possible and advertises viable routes for data. If BGP stops working, those routes can’t be found and disappear from the internet, so the data has nowhere to go.

Even better, it found the exact incident I was looking for after the second query:

> On 27 August 2010, the RIPE NCC’s Routing Information Service (RIS) was involved in an experiment using optional attributes in the Border Gateway Protocol (BGP). As a result of this experiment, a small but significant percentage of global Internet traffic was disrupted for a period of about 30 minutes

### Lesson Learned

Large language models still seem to be little more than stochastic parrots regardless of how well they perform on standardized tests[^ST], but you can get great results if you use them to implement smarter search or as a [front-end to another knowledge-based service](https://writings.stephenwolfram.com/2023/03/chatgpt-gets-its-wolfram-superpowers/).

Obviously that approach wouldn't make VCs happy -- imagine you have to admit that instead of the first stepping stone toward Artificial General Intelligence you created a better user interface ;)

[^ST]: Or maybe that just validates the opinion many people have about standardized tests ;)