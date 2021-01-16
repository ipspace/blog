---
title: "Worth Reading: Finding Bugs in C and C++ Compilers"
date: 2021-02-06 06:59:00
tags: [ worth reading ]
---
Something to keep in mind before you start complaining about the crappy state of network operating systems: people are [still finding hundreds of bugs in C and C++ compilers](https://blog.sigplan.org/2021/01/14/finding-bugs-in-c-and-c-compilers-using-yarpgen/).

One might argue that compilers are even more mission-critical than network devices, they've been around for quite a while, and there might be more people using compilers than configuring network devices, so one would expect compilers to be relatively bug-free. Still, optimizing compilers became ridiculously complex in the past decades trying to squeeze the most out of the ever-more-complex CPU hardware, and we're paying the price.

Keep that in mind the next time a vendor dances by with a glitzy slide deck promising software-defined nirvana.
