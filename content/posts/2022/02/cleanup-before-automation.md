---
title: "Do a Cleanup Before Automating Your Network"
date: 2022-02-03 08:06:00
tags: [ automation ]
---
*[Remington Loose](https://www.linkedin.com/in/remington/) sent me an interesting email describing his views on the right approach to network automation after reading my _[Network Reliability Engineering Should Be More than Software or Automation](/2020/06/network-reliability-engineering-more-than-automation/)_ rant -- he's advocating standardizing network services and cleaning up your network before trying to deploy full-scale automation.*

---

I think you are 100% right to start with a thorough cleanup before automation. Garbage in, garbage out. It is also the case that all that inconsistency and differentiation makes for complexity in automation (as well as general operations) that makes it harder to gain traction.
<!--more-->
Anecdotally, I see customers that have long-serving, intelligent, capable network engineer/architects have more stable, more consistent and more standardized networks. That’s a lot of caveats but it is the case. Customers without long-term, competent, senior folk have a potpourri of things and it detracts from stability as well as automation. As an outside advisor I try to slowly push customers into standardization as the first few steps…and it pays off. After a few years of working with folks I get a lot of compliments and comments about how stable and reliable their networks now are…and they are ready to make the next “moves” which include automation.

I don’t want to say people shouldn’t start automating their networks or that automation is secondary but rather that “automation is great, you should start the journey for sure, but perhaps first you should spend time cleaning first”. The analogy in my mind is like using a robot vacuum. They are great and can save you time. But you should pick up the room before turning it on. If not, you can get into a situation of vacuum-meets-poop-now-you-have-poop-everywhere or fragile things get broken or vacuum fails to provide value as it gets stuck/snagged. Then you have to clean-up the mess made by the vacuum, fix/clean the vacuum and still clean the floor…so your one problem just became three. Likewise, using automation before standardizing is using a tool to fix a broken process and that really doesn’t work in my experience.

I don’t think it is a grumpy older-timer thing but I do think newer engineers fail to full appreciation the value of standardization and simplicity in design. I am not sure if this is one of those lessons you have to learn for yourself but I suspect it is more of a lack of mentoring/apprenticeship in the networking field. It speaks to the value of your content (I think) for junior folk and it highlights the ongoing need for a different method of training network engineers.