---
title: "Imperative and Declarative API: Another Pile of Marketing Deja-Moo"
date: 2021-01-13 07:24:00
tags: [ automation, intent-based networking ]
lastmod: 2021-01-14 08:01:00
intent-based-networking_tag: declarative
series_weight: 500
series: [ niac ]
niac_tag: rant
---
Looks like some vendor marketers (you know, the same group of people who brought us the [switching/routing/bridging](/2011/02/how-did-we-ever-get-into-this-switching.html) stupidity) felt the need to go beyond the usual SDN and intent-based hype and started misusing the *imperative* versus *declarative* concepts. Unfortunately some networking engineers fell for the ploy; here's a typical feedback along these lines I got from one of my readers:

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

* Using *declarative* and *imperative* to describe API calls makes as little sense as [intent-based networking](/tag/intent-based-networking.html) (TL&DR: every configuration is an expression of our intent).
* What really matters is the *level of abstraction* an API call provides, and the [atomicity of the requested operation](/2019/04/rest-api-is-not-transactional.html).

Obviously that won't stop the vendor marketers from proudly creating slides claiming their product uses *declarative API*. Make sure to make fun of them whenever you see one -- it probably won't do any more harm than mr. Quixote did to the windmills, but it might feel good (he wasn't so lucky).

### A note to marketers

I [wrote this in 2015](/2015/07/some-ridiculous-sd-wan-claims.html) but of course nobody ever listens:

> I understand you have to do what you have to do, but you don't have to make yourself looking totally ridiculous in the process.

### Feedback on Twitter

[Kristian Larsson wrote a lengthy Twitter thread](https://twitter.com/plajjan/status/1349294267961929728) explaining his views on the topic, and allowed me to copy that thread into this blog post:

---

I don't think the meaning of declarative and imperative is the same for an API as it is for a computing paradigm or programming language, which seems to be the Wikipedia definition you've gone by. Primarily, your mapping of imperative to *how* leads to an incorrect conclusion. For an API, it's not about telling a program how to perform a command. I think you should see the 'how' as what low level commands you need to string together to achieve your high level intent.

I think of it like this; an imperative API exposes *verbs* that you then call. add_user() is an imperative command. Calling add_user('ivan', pwd) twice in a row will fail due to username uniqueness. *How* do I achieve "user Ivan ssh-key is X". Since calling add_user('ivan', pwd) fails if the user exists, I first have to rm_user('ivan'), then add_user('ivan', pwd). Reverse the order of those commands, and it means something entirely different.

In a declarative API on the other hand, you merely specify a list of users - your intent - and let device figure it out. If the user exists before doesn't matter, then nothing happens, or it's updated with new parameters. If it didn't exist, it's created etc. You could say that add_user() could be made idempotent, which is true and that would make that API *call* less imperative and more declarative, but it is still fundamentally imperative. The declarative approach is to declare the list of users, not performing actions on that list.

Declarative APIs are generally easier to work with since we effectively delegate the sisyphean task of reaching the intended configuration to the device. Pretty much everything is imperative at a low level. Idempotency is a way to build declarative things out of imperative ones.

Higher level APIs tend to be more declarative than the underlaying low level things they abstract over, which in turn tend to be more imperative. In a stack of abstractions, declarativeness tend to rise the higher up in the stack you go and vice versa.

NETCONF / YANG is a mostly declarative API. The configuration you declare is declarative. You tell the device that there should be 4 BGP neighbors, you don't do add_bgp_neighbor() or rm_bgp_neighbor(). But NC / YANG also supports imperative things, like restarting a device is not something you configure, it is naturally something you tell it to do, a imperative verb - "restart!" These are modeled in YANG as actions, since that is what they are! Thus it is possible to build an imperative API in NETCONF YANG through actions that modify the applied configuration - but who would want that?

I think describing APIs as declarative or imperative is a useful classification and helps in understanding the capabilities and behavior of them. As usual, it's not black and white though. Soon someone is going to come along with "but but, in NETCONF, the RPC for editing the supposedly declarative configuration is called 'edit-config' which sounds very verbish!?". Yes, but edit-config takes a declarative config. There is no add-config or remove-config RPC :) NETCONF / YANG is fundamentally model driven, because you teach your client once about edit-config, then it can modify (add, delete or modify) any configuration described by a YANG model. When you add ABC (successor of BGP) then you don't need to teach it about add_abc_neighbor()

---

While I agree with most everything he wrote, and abstraction layers and idempotency are important, I still don't think it's OK to take well-defined terms and reuse them in a vague way (when you find a non-marketing definition of *imperative* versus *declarative* API please do let me know).

Also keep in mind that many APIs that people would claim are *declarative* because they offer a layer of abstraction are not really *idempotent* (= you cannot declare your intent twice).

### More Information

I plan to cover intent-based networking and declarative- and policy APIs in [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar (one of those things I feel need to get done before I [disappear for that coffee break](planning-coffee-break.html)).

### Revision History

2021-01-14
: Added comments by Kristian Larsson
