---
title: "When You Find Yourself on Mount Stupid"
date: 2022-06-14 06:20:00
tags: [ networking fundamentals ]
---
The early October 2021 Facebook outage generated a predictable phenomenon -- couch epidemiologists became experts in little-known [Bridging the Gap Protocol](https://twitter.com/ACM_IMC2021/status/1445725066403196928) (BGP), including its Introvert and Extrovert variants. Unfortunately, I also witnessed several unexpected trips to [Mount Stupid](https://www.smbc-comics.com/?id=2475) by people who should have known better.

To set the record straight: everyone's been there, and the more vocal you tend to be on social media (including mailing lists), the more probable it is that you'll take a wrong turn and end there. What matters is how gracefully you descend and what you've learned on the way back.
<!--more-->
As you might guess, I'm a regular visitor of that exalted peak, and one of my trips started with the idea of [using BGP/MPLS L3VPN (RFC 4364) as the network virtualization control-plane protocol](/2011/04/vcloud-architects-ever-heard-of-mpls/). After all, L3VPN was a solved problem a decade ago, and MPLS was the answer no matter the question[^1].

[^1]: The answer to all questions changed to LISP, but I'm digressing.

It turns out I made a typical error: I assumed that the experience gained in the environments I was familiar with (service provider networks) is universal and applies equally well everywhere (including large-scale data centers). Someone was graceful enough to pull me aside during one of the SDN conferences and exposed me to a contrarian view: BGP might not be fast enough to cope with a large-scale virtual machine migration event.

The "*too much churn for BGP*" argument turned out to be a bit of a red herring -- once you [do the math](/2011/09/long-distance-vmotion-for-disaster/), you realize it's not that easy to migrate so many virtual machines -- but it got me thinking. Eventually, I found other reasons why the MPLS/VPN architecture is [not the best solution for a single fabric connecting hundreds of thousands of edge switches](/2012/03/mplsvpn-in-data-center-maybe-not-in/) (a hyper-scale data center).

Psychologists are very familiar with the trips to Mount Stupid and created whole theories explaining that behavior (see: *[Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)*). We're not used to thinking about environments that are orders of magnitude outside of our comfort zone, or events with very low probability (see: *[The Black Swan](https://en.wikipedia.org/wiki/The_Black_Swan:_The_Impact_of_the_Highly_Improbable)*). We also tend to assume that whoever decides to do something that goes against our instinct must have missed some higher truth we're privy to.

There are also well-known techniques you can use to ensure your trip to that peak ends gracefully:

* Don't assume you're the smartest person in the room. Whoever has a contrarian view might have a reason for that.
* [Try to figure out the underlying causes and assumptions for that contrarian view](/2021/07/network-design-tricycles-carriers/) (or a design you disagree with). Ask questions, don't fight with whatever ammunition you find handy.
* In the end, you could find out that you were right, or you could slide down an utterly unexpected rabbit hole and learn tons of new things on the way.
* If you were wrong, admit it and fix whatever you might have published on the topic. Saying "*I was wrong, here's why, and here's what I've learned*" is usually the best way out of the uneasy situation.

Interested in another take on the subject? RFC 1925 is a mandatory reference text; you might also want to listen to the *[Learn from Our Experience](https://www.modem.show/post/s01e11/)* episode of the [MODEM podcast](https://www.modem.show/).
