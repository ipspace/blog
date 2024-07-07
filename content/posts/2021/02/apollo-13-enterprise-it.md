---
title: "Rant: Don't Ever Compare Enterprise IT Shenanigans with Apollo 13"
date: 2021-02-15 07:43:00
tags: [ design ]
---
Here's a [recent tweet](https://twitter.com/JoeOnisick/status/1356975753003294727) by my friend Joe Onisick that triggered this blog post:

> My favorite people are the ones that start with "how could we make that work?" Before jumping into all of their preconceived bs on why it won't work.

I couldn't agree more with that sentiment. The number of people who would invent all sorts of excuses just to avoid turning on their brains and keep to their cozy old methods is staggering. Unfortunately, someone immediately had the urge to switch into what I understood to be a [heroic MacGyver mode](/2013/08/temper-your-macgyver-streak/) (or maybe it was just my lack of caffeine, in which case I apologize for the misquote... but you might still like the rest of the rant):
<!--more-->
> I often use the quote from Apollo 13(movie):
>
> "*I don't care about what anything was designed to do. I care about what it can do.*"

There are a few tiny difference between Apollo 13 and enterprise IT:

* Apollo 13 was designed to be robust and reliable with tons of safeguards and redundancy mechanisms, or they would have no chance to fix it. You might want to revisit their [software development practices](https://www.synopsys.com/blogs/software-security/apollo-11-software-development/) and compare them with *fail fast* mentality we have today.
* Apollo 13 worked as designed until a disaster struck. Today  we often have to deal with things that barely function when we use them the way they were supposedly designed to be used;
* According to urban myths three lives might have been involved in the Apollo 13 story and the whole world was watching. I don't think we're often in that position in IT, or we would have better rules and regulations, and maybe even deserve the *[engineering](/2018/01/how-to-become-better-networking-engineer/)* title we love to use.
* The sole purpose of fixing Apollo 13 was to bring those three people down to earth. After that, the capsule was scrapped, and they fixed whatever problems they could in subsequent missions. What we're commonly seeing these days (after a [MacGyver comes to rescue the situation](/2013/04/this-is-what-makes-networking-so-complex/)) is a stupid temporary hack that should have never seen the light of day becoming a permanent technical debt... and yes, we do use the [duct tape of networking](/2015/06/software-defined-wanwell-orchestrated/) (NAT, GRE, and PBR) to fix way too many issues that would deserve a redesign.

So the next time you want to propose to use duct tape (because it was used to save Apollo 13) or [some magic technology](/2020/09/business-needs-excuses/) to solve a crisis, please don't. Maybe it's worth starting with "*[what problem are we trying to solve?](/2013/01/long-distance-vmotion-stretched-ha/)*"
