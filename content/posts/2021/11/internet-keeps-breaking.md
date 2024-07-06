---
title: "Why Does Internet Keep Breaking?"
date: 2021-11-04 06:58:00
lastmod: 2021-11-06 13:31:00
tags: [ Internet, BGP ]
---
James Miles sent me a long list of really good questions along the lines of "_why do we see so many Internet-related outages lately and is it due to BGP and DNS creaking of old age_". He started with:

> Over the last few years there are more "high profile" incidents relating to Internet connectivity. I raise the question, why?

The most obvious reason: Internet became mission-critical infrastructure and well-publicized incidents attract eyeballs.

Ignoring the click baits, the underlying root cause is in many cases the [race to the bottom](https://en.wikipedia.org/wiki/Race_to_the_bottom). Large service providers brought that onto themselves when they thought they could undersell the early ISPs and compensate their losses with voice calls (only to discover that voice-over-Internet works too well).

<!--more-->
{{<note info>}}The initial version of this blog post incorrectly claimed that FRR does not support multi-threaded routing daemons. Removed the offending part of the blog post; more details later.{{</note>}}

The only way out of that morass is either simplified services (example: [Deutsche Telekom Terastream](/2013/11/deutsche-telekom-terastream-designed.html)), increased automation (bringing its own perils, see also [Facebook October 2021 outage](/2021/10/circular-dependencies-considered-harmful.html)) or ever-more-appalling quality of support and service.

For example, we knew for ages what needs to be done to stop fat-finger incidents, and yet many large ISPs like Verizon (not picking on them, it’s just that [their SNAFU went public](/2019/07/rant-some-internet-service-providers.html)) did absolutely nothing to implement the most rudimentary safeguards like limiting the number of BGP prefixes a customer can advertise. 

You don't have to take my word for it. There are [public services ](https://twitter.com/Qrator_Radar) tracking BGP leaks[^BL] and hijacks[^BH], and small-scale incidents happen every week. We're also [facing a few global leaks and hijacks every quarter](https://blog.qrator.net/en/q3-2021-ddos-attacks-and-bgp-incidents_146/)[^HT_AT].

[^BL]: Advertising unexpected transit routes through customer networks

[^BH]: Advertising IP prefixes belonging to third parties as originating within your autonomous system.

[^HT_AT]: I got a link to this report from a [tweet by Andree Toonk](https://twitter.com/atoonk/status/1451220431764017155).

A long while ago a group of engineers focused on Internet stability defined best practices under the [MANRS umbrella](https://www.manrs.org/). Many ISPs started following them, but there are still too many of the sloppy incompetents out there. Compare the list of [MANRS participants](https://www.manrs.org/isps/participants/) with the list of [Tier-1 providers](https://en.wikipedia.org/wiki/Tier_1_network) and reach your own conclusions.

> BGP & DNS are some of the oldest protocols in regular use, are the protocols creaking with modern approaches?

I wouldn’t say so. Considering the limitations of hop-by-hop destination-only packet-by-packet forwarding, BGP works just fine (and is [good enough for many use cases](https://homepages.dcc.ufmg.br/~cunha/papers/arnold19hotnets-bgp.pdf)). It has too many knobs because vendors always tried to solve the next feature request with [one more intent-based knob](/2018/01/bgp-route-selection-failure-of-intent.html) instead of a [plugin architecture](/2020/11/pluginized-protocols.html), but that’s a different story.

The real problem of BGP seem to be the implementations. There are so many things running on decades-old code that was written to run well on single core 16- or 32-bit processors with 4MB of RAM. 

<!--
For example, FRR still can't use more than a single thread (and thus a single CPU core) per daemon. Straight from [FRR documentation](http://docs.frrouting.org/projects/dev-guide/en/latest/process-architecture.html) (as of early November 2021):

---

_As FRR is deployed at larger scales and gains ever more features, each adding to the overall processing workload, we are approaching the saturation point for a single thread per daemon. In light of this, there are ongoing efforts to introduce multithreading to various components of FRR_

---
-->
DNS seems to be in a bit more of a tight spot due to DNSSEC -- the [replies don’t fit into a single UDP packet anymore](https://www.potaroo.net/ispcol/2021-10/rsa.html). I know just enough about DNS to be able to form wrong opinions, but from where I’m sitting it looks like we would have to change the way we do things and the default settings, but maybe not the whole protocol.

> As the oldest protocols in regular use, are engineers losing the skill to effectively deploy them?

Both protocols (like everything else) are getting more and more complex as people pile new features on top of what was once a stable infrastructure. For example, even though I was running DNS- and email servers in 1990s (and even ported _sendmail_ to MS-DOS to implement my own email service), I wouldn’t dream about running them these days — there are too many details I’m simply not familiar with.

BGP seems to be doing a bit better from the edge AS perspective — connecting your AS to two somewhat competent ISPs is as easy as it ever was. Beyond that, there's a steep learning curve.

However, successfully implementing a science project doesn’t give you experience to run a large-scale system, and as the number of large-scale systems is limited, it’s [hard to migrate from one to the other](/2018/12/bifurcation-of-knowledge.html). The situation is similar in any sufficiently-commoditized infrastructure discipline, from power transmission to gas pipelines or water supply. Being able to pull cables through the walls doesn’t make you an expert in high-voltage power lines.

Unfortunately, what we’re lacking in networking (and most of IT in general) is a solid foundation on which to build things, rigorous training that the traditional engineering disciplines have, an equivalent of Professional Engineer exams, and [professional liability](/2021/10/worth-reading-professional-liability.html). We’re often [throwing spaghetti at the wall](https://archive.psg.com/051000.sigcomm-ivtf.pdf) and get ecstatic when some of them stick.

> Have we put too many extras and/or sticky plasters on the protocols and they are now destabilizing?

We put too many extras and sticky plasters everywhere. Too much of the infrastructure out there is a smoking pile of unstable kludges that eventually collapse.

We’re also increasingly relying on cheap (or free) third-party services, and get totally stupefied when they disappear for a few hours. The number of hidden dependencies in the stuff that runs everyday life is horrifying.

Want a longer version of this rant? You'll find it in the _[Upcoming Internet Challenges](https://www.ipspace.net/Upcoming_Internet_Challenges)_ webinar.
