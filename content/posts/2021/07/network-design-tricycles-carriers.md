---
title: "Designing Networks: From Tricycles to Aircraft Carriers"
date: 2021-07-12 15:52:00
tags: [ design ]
---
I planned to take my summer break seriously and stop blogging until late August, but then I shouldn't have looked at my Twitter feed (my bad), where the AI algorithms selected just the [right morsel](https://twitter.com/joshobrien77/status/1414372302461050883) to trigger the maximum rantiness. I would strongly recommend you [read the original tweet](https://twitter.com/maxclark/status/1414037172794101766) and all the responses first -- it looks like it was a serious suggestion, not a trolling exercise ([here's a copy of the original idea](/2021/07/Remove-Redundancy.jpg) in case the tweets get lost in the mists of time).
<!--more-->
Done? OK, here's my take on what the author of that inflammatory tweet was saying: "_the networks I design need no redundancy, and thus I consider redundancy to be unnecessary._" Good for him, and we could have stopped right there, but I got the feeling it went further along the lines of "_and I'm willing to die on this hill and to prove how misguided y'all are._" Ouch.

Now step back and think for a moment about the various requirements we're facing when designing networks. It ranges from "_my Grandma needs Internet_" (kid's tricycle) to hyperscaler data centers (aircraft carriers?) and air traffic control (rockets?). Claiming one could apply the lessons learned from one's small corner of the world to all of them is potentially a bit arrogant.

However, there's always a nugget (or two) in every public spat; one just has to have the nerve to look for it ;) In this particular case:

* State-sharing redundant solutions are way less reliable than non-redundant solutions. I'm looking at you, [firewall clusters ](/2019/11/stretched-vlans-and-failing-firewall.html)and [multi-supervisor switches](/2014/04/should-we-use-redundant-supervisors.html)... and I can't force myself to look at stackable switches.
* Trying to increase system resiliency by [deploying complex redundant infrastructure](/2018/01/revisited-need-for-stretched-vlans.html) benefits only sloppy application developers and infrastructure equipment manufacturers. You might end up with a brittle solution that will break faster than the non-redundant infrastructure components or the craplication running on top of it.
* In many cases, we build redundant solutions to cover our backsides. Nobody could blame me for a failure if I did everything in my power to prevent it, right?

Does that mean the author of that tweet was correct? Of course not -- the only way to get a resilient system (which includes infrastructure and everything running on top of it) meeting whatever requirements you might have is to [figure out the real requirements first](/2019/12/figure-out-what-problem-youre-trying-to.html), and then follow the excellent suggestion made by Albert Einstein: "Everything should be as simple as it can be, **but not simpler**."
