---
title: "The BGP Multi-Exit Discriminator (MED) Saga"
date: 2023-11-30 07:54:00
tags: [ BGP ]
---

[Martijn Van Overbeek](https://www.linkedin.com/in/martijnvanoverbeek-ccie38666/) left this comment on my [LinkedIn post](https://www.linkedin.com/posts/ivanpepelnjak_bgp-labs-using-multi-exit-discriminator-activity-7130543496884555776-uqIQ) announcing the [BGP MED lab](/2023/11/bgp-labs-multi-exit-discriminator.html):

> It might be fixed, but I can recall in the past that there was a lot of quirkiness in multi-vendor environments, especially in how different vendors use it and deal with the setting when the attribute does exist or does not have to exist.

**TL&DR:** He's right. It has been fixed (mostly), but the nerd knobs never went away. 

In case you're wondering about the root cause, it was the vagueness of RFC 1771. Now for the full story ;)
<!--more-->
This is what [RFC 1771 had to say](https://datatracker.ietf.org/doc/html/rfc1771#section-9.1.2.1) about the use of MED in path selection process:

> If the local system is configured to take into account MULTI_EXIT_DISC, and the candidate routes differ in their
  MULTI_EXIT_DISC attribute, select the route that has the lowest value of the MULTI_EXIT_DISC attribute.

Now remember that MED is an **optional** non-transitive attribute. Any decent programmer should realize the above rule is incomplete[^AFB]: what do you do when comparing a route with MED and another without it? You could:

[^AFB]: After missing the intricacy, coding an approximate (or plain wrong) solution, having that code pass all the tests (because no one ever considered that someone might decide to set MED only on the backup link), and getting a bug report caused by a Priority 1 TAC case coming from a yelling customer.

* Consider the missing MED equal to zero (best)
* Consider the missing MED equal to infinity (worst)
* Do the right thing and say "_one cannot compare missing values_"

There's also the question, "_does comparing MED across routes coming from different autonomous systems make sense?_" The sane answer seems to be *of course not* (as there's no standard definition of what MED means), but RFC 1771 never considered that academic question[^CF]. Also, arguing with a network architect holding a large purchase order and a broken design is usually counterproductive.

[^CF]: ... with another academic question being "_do autonomous systems in a confederation count as same AS or different AS?_"

You probably know what happened next: different vendors chose to do different things, creating a total mess that made MED nearly useless. The cacophony of options also spawned a cottage industry of nerd knobs -- after all, if you want to unseat a competitor and replace their boxes in a large network, your stuff has to behave exactly like theirs.

RFC 4271 [fixed most ambiguities](https://datatracker.ietf.org/doc/html/rfc4271#section-9.1.2.2)[^LPX]:

[^LPX]: ...and added a lengthy paragraph describing the corner cases that can happen if a router removes MED on IBGP updates.

* MED is only comparable between routes learned from the same autonomous system;
* Routes without MED are considered to have MED = 0.

However, once you implement a workaround to a multi-vendor interoperability SNAFU or as a fix for a broken design, that nerd knob never disappears -- we still have **bgp bestpath med missing-as-worst**, **bgp bestpath med confed**, and **bgp always-compare-med** nerd knobs, not to mention the **bgp deterministic med** abomination caused by partial ordering of multi-dimensional path metric ([here's ](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/16046-bgp-med.html) a decent description of the last one).

### Revision History

2023-12-04
: MED is a _non-transitive_ attribute (the original blog post incorrectly stated it is transitive). Fix triggered by Aleksei's comment -- thank you!
