---
title: "Imperative and Declarative API: Another Pile of Marketing Deja-Moo"
date: 2021-01-13 07:24:00
tags: [ automation, intent-based networking ]
---
Looks like some vendor marketers (you know, the same group of people who brought us the [switching/routing/bridging](https://blog.ipspace.net/2011/02/how-did-we-ever-get-into-this-switching.html) stupidity) felt the need to go beyond the usual SDN and intent-based hype and started misusing the *imperative* versus *declarative* concepts. Unfortunately some networking engineers fell for the ploy; here's a typical feedback along these lines I got from one of my readers:

>  I am frustrated by most people’s shallow understanding API’s, especially the differences between declarative (“what”) and imperative (“how”) API’s, and how that impacts one’s operations. Declarative APIs are the key pillar of what many vendors call “policy” or “intent-based” networking.

Let's try to unravel that. 
<!--more-->
![You keep using that word...](keep-using-that-word.jpg)

According to [Wikipedia](https://en.wikipedia.org/wiki/Declarative_programming):

> In computer science, declarative programming is a programming paradigm—a style of building the structure and elements of computer programs—that expresses the logic of a computation without describing its control flow.

I haven't seen a single API call that would tell the server **how** to do stuff. They always tell the server what we want to get done. Admittedly, some API calls are more abstracted than others, but that's a different story.

**Conclusion**: All API calls are declarative.

Back to [Wikipedia](https://en.wikipedia.org/wiki/Imperative_programming):

> In computer science, imperative programming is a programming paradigm that uses statements that change a program's state. In much the same way that the imperative mood in natural languages expresses commands, an imperative program consists of commands for the computer to perform.

All Create, Update, or Delete (three quarters of [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) API calls are executed to *change the state of the system*. Admittedly, some API calls tell the system what to do in vague manner, while others are more precise.

**Conclusion**: Many API calls are imperative.

Looks like we got to a bit of an absurd situation, and the only way to resolve it is to conclude that it's all just another pile of marketing deja-moo. QED.

![Deja Moo -- when you know you've seen that bullshit before](deja-moo.jpg)

### Summary

* Using *declarative* and *imperative* to describe API calls makes as little sense as [intent-based networking](https://www.ipspace.net/kb/tag/intent-based-networking.html) (TL&DR: every configuration is an expression of our intent).
* What really matters is the *level of abstraction* an API call provides, and the [atomicity of the requested operation](https://blog.ipspace.net/2019/04/rest-api-is-not-transactional.html).

Obviously that won't stop the vendor marketers from proudly creating slides claiming their product uses *declarative API*. Make sure to make fun of them whenever you see one -- it probably won't do any more harm than mr. Quixote did to the windmills, but it might feel good (he wasn't so lucky).

### A note to marketers

I [wrote this in 2015](/2015/07/some-ridiculous-sd-wan-claims.html) but of course nobody ever listens:

> I understand you have to do what you have to do, but you don't have to make yourself looking totally ridiculous in the process.

### More Information

I plan to cover intent-based networking and declarative- and policy APIs in Network Automation Concepts webinar (one of those things I feel need to get done before I [disappear for that coffee break](planning-coffee-break.html)).
