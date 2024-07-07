---
date: 2019-09-03 07:03:00+02:00
tags:
- automation
- SDN
title: If You Have to Simulate Your Whole Network, You're Doing It Wrong
url: /2019/09/if-you-have-to-simulate-your-whole/
---
*This blog post was initially sent to subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

Have you ever seen a presentation in which a startup is telling you how awesome their product is because it allows you to simulate your whole network in a virtual environment? Not only that, you can use that capability to build a test suite and a full-blown CI/CD pipeline and test whether your network works every time you make a change to any one box in the network.

Sounds awesome, right? It's also dead wrong. Let me explain why that's the case.
<!--more-->
Imagine you're writing a software for a small bank. It has about 100 bank tellers, but each one of them wants to do business their own way. Some of them want to use custom-designed forms, other prefer to do transactions only every second minute of the hour, still others want to use a different rounding algorithm to calculate interests... supposedly to accommodate their customers because "*mr. Jones, our biggest customer, prefers to have his interest rounded to odd numbers, because that's how we always did it for him.*" and "*mrs. Smith wants to have the money appear in her bank account an hour before someone pays her because she wants to start collecting the interest as soon as possible*"

To make it even more interesting, let's add some weird quantum entanglement to the mix. For example, whenever Bob (a teller in Portwenn) does a transfer of funds to a customer in Eastwick, the teller in Wokenwell might be unable to trigger any transactions for the next 10 minutes. Yeah, doesn't make sense, but neither do so many other things we have to deal with in real life.

Now imagine you want to implement *continuous integration* - the ability to test whether your software works after every change made to the source code. The only thing you can do is to emulate the whole morass, including all bank tellers and their obnoxious customers, and test every possible combination of transactions that might trigger the quantum entanglement... while keeping in mind that every bank teller runs their own customized version of the same transactions because of the supposed uniqueness of their customers.

Not only would any decent software developer quit the moment they'd hear the first paragraph of this story, anyone looking from the outside in would probably say "*I'll have what they're smoking, it must be good*"... and yet this is exactly how we build, configure and operate our networks.

The need to emulate the whole network in a virtual environment arises from two broken scenarios:

-   Every component in your network is a unique snowflake, and the only way to test whether whatever you changed won't crash the network when deployed is to test the whole network (see above);
-   You haven't mastered the "black magic" of creating device configurations from high-level data models and configuration templates and thus have to test every change you make to device configurations because you can't make the changes repeatable and thus consistent and reliable.

How could you get out of this morass? How about a (simplified) three-step process:

-   Get rid of snowflakes and exceptions. Define services the network is supposed to offer, standardize them and describe them with a [data model that is as simple and as abstract](/kb/DataModels/) as you can make it (the fewer parameters a service has, the easier it will be to implement and test it);
-   Unify your network design so that it's possible to predict the behavior of the whole network regardless of its size by wiring together a small set of components (example: a few access nodes, a few aggregation nodes, and a few core nodes);
-   Abstract the transactions the operators are allowed to make in the network, and use configuration templates to make device configurations consistent. It's much easier to test the impact of well-defined transactions with well-known outputs than it is to test any random change someone could make to a device configuration.

As I warned you, this is a highly simplified view of the challenge, but we have to start somewhere... and if you want to grasp the details we have you covered: you'll master plenty of them while working through our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions).
