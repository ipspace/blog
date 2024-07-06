---
title: "Simplify and Standardize Mantra Encounters Reality"
date: 2022-05-24 06:04:00
tags: [ automation ]
---
I'm usually telling networking engineers seriously considering whether to automate their networks to cleanup their design and simplify the network services first.

> The only reasonable way forward is to simplify your processes – get rid of all corner cases, all special deals that are probably costing you more than you earned on them, all one-off kludges to support badly-designed applications – and once you get that done, you might realize you don’t need a magic platform anymore, because you can run your simpler network using traditional tools.

While [seasoned automation practitioners](/2022/02/cleanup-before-automation.html) agree with me, a lot of enterprise engineers face a different reality. Straight from a source that wished to remain anonymous...
<!--more-->
---

I have found that standardization efforts ebb and flow over time.

You may, for example, get your network infrastructure setup and working just the way you want it, but then have to augment it because of some oddball requirement or inevitable evolution over time. We built a large data center years ago with Cisco Nexus 7ks VDCs running Fabricpath. The initial design and implementations were very clean, standard and generally easy to build, support (other than the code bugs -- sigh) and automate. But over time, we had to upgrade supervisors and line cards to support higher bandwidth and TCAM demands, place fabric extenders in unusual locations, offload backup traffic from database clusters, begin supporting IP storage and attach vendor provided switches that come pre-installed in their OEM racks. 

Also, ever-present budget constraints forced our team into sub-optimal technical solutions. For example, we didn't have budget to upgrade our entire fleet of F2 line cards to F3s, so we had to phase the upgrades over 2 or 3 budget years. So the initial design that was highly standardized with consistent structured cable plant became less so over time, making buildouts, code upgrades and automation efforts more challenging.

Ruthless standardization introduces efficiencies and limitations. If your standard solution cannot account for one-offs, you (or your customers) end up building a parallel infrastructure (or shadow IT) to deal with them or missing out on business opportunities.

Effectively, there are no free lunches. What we do is complex. The technologies change continuously. Oversimplifying it just provides non-technical folks even less appreciation for what we do.

Sorry if this sounds like whining. It's not my intent. I absolutely love designing, building, operating and troubleshooting networks. I still find there is no substitute for a robust monitoring regime, deep technical expertise, strong IT management processes and resilient design.

---

Fortunately, there's a way forward even when faced with grim reality; I described some ideas in the _[Automate the Exceptions](/2016/07/automate-exceptions.html)_ blog post years ago, and I remember David Barroso having real-life examples in one of his webinars, but I can't find them :(
