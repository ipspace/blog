---
date: 2009-12-21 06:52:00+01:00
tags:
- Internet
title: 'ITU and Internet Billing: It’s a Déjà-Vu All Over Again'
url: /2009/12/itu-and-internet-billing-its-deja-vu.html
---
My friend [Stretch](http://packetlife.net/blog/) alerted me to an [article published by BBC News](http://news.bbc.co.uk/2/hi/uk_news/politics/8417680.stm), which reports that "an EU cyber security expert" told "a House of Lords committee" (wow, that's the perfect body to deal with Internet issues) that the proposal submitted by Chinese to an ITU-T study group required "modifications to BGP" which would "threaten the stability of the entire Internet."

Regardless of whatever the original proposal has been, the information has been distorted, twisted, adapted, abstracted, and misunderstood so many times before being published that it's impossible to figure out what exactly has been going on. The [account of an eyewitness](http://seclists.org/nanog/2009/Dec/621) (sitting in the Kampala talks in September) doesn't tell much more.
<!--more-->
I've [tried to get to the source](http://www.itu.int/md/T09-SG03-090921/sum/en), but I couldn't. ITU-T, a UN standardization body with delegates representing governments from member countries (read carefully: this means they're getting paid out of your pockets ... twice), takes [great care to hide its operations from its investors](http://www.itu.int/TIES/registration/DM1013.pdf) (you and me).

OK, let's try to figure out what we can:

**(A) What does ITU have to do with Internet billing?** Nothing at all, but (as I've [pointed out in my previous ITU-related post](/2009/11/itu-grabbing-piece-of-ipv6-pie.html)), with their precious crown jewels (ISDN, ATM) losing importance, they're trying to get their fingers into another juicy pie that will justify having more standardization meetings.

**(B) What could be the technical background?** None. As [Roland Dobbins was quick to point out](http://seclists.org/nanog/2009/Dec/624), anyone with a basic understanding of how BGP and Netflow work would realize immediately that the Chinese could get whatever traffic/billing data they want with the existing technology. Anyone familiar with the basics of BGP attributes (and extended BGP communities) would also realize that you can easily add new communities to BGP routes without upsetting anyone else. The whole shenanigan (from the Chinese as well as the EU security expert) is a smokescreen for something else.

**(C) What are the Chinese doing in this game?** As Greg Ferro has pointed out in his (now gone) blog post, the Chinese government is misusing ITU (and some somewhat clueless delegates traveling to its meetings) to push its goals through the side door. Having arrived late to the game and not being involved enough in the standardization body that created the Internet (IETF), they're trying to leverage whatever influence they have in ITU-T.

**(D) So, what is it that they want?** Short version: they want others to pay parts of their Internet bills. To make it more presentable, the claim is that "they have the backing of a number of developing countries, who currently have to bear the cost of international internet connections" (quote from the BBC news article). Nothing new; we've been there in the 1990's. Read the [short description of the ICAIS controversy](http://www.cybertelecom.org/broadband/icais.htm), or explore the reasons why Trump [wanted to pull the US out of the Universal Postal Union](https://en.wikipedia.org/wiki/Universal_Postal_Union#2019_Extraordinary_Congress).

Before someone tells me I'm sounding too negative, I'm not against commercial agreements between Service Providers, more so if they're fair to both parties. However, I abhor bogus technical arguments being used to cloak shady deals pushed through a non-transparent organization trying to get involved in something it never belonged in.

Last but not least, if they really want to be useful, they could try to tackle some of the real problems the Internet is facing, such as an architecture for scalable multihoming.
