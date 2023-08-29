---
title: "Random Thoughts on Zero-Trust Architecture"
date: 2023-09-05 06:05:00
tags: [ security ]
---
When preparing the materials for the [Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic) section describing [Zero-Trust Network Architecture](https://my.ipspace.net/bin/list?id=Design#2023_02), I wondered whether I was missing something crucial. After all, I couldn't find anything new when reading the [NIST documents](https://www.nist.gov/publications/zero-trust-architecture) -- we've seen all they're describing 30 years ago (remember Kerberos?).

In late August I dropped by the fantastic [Roundtable and Barbecue](https://www.eventcreate.com/e/sigs-roundtable-august) event organized by Gabi Gerber (running [Security Interest Group Switzerland](https://www.sig-switzerland.ch/)) and used the opportunity to join the Zero Trust Architecture roundtable. Most other participants were seasoned IT security professionals with a level of skepticism approaching mine. When I mentioned I failed to see anything new in the now-overhyped topic, they quickly expressed similar doubts.
<!--more-->
Fortunately, we had a vendor consultant to guide us, and he explained that this time, it's all about processes, frameworks, and maturity levels. Speaking about frameworks, we should focus on three domains: users, applications, and data. There's just a tiny bit of a problem there: I heard that story years ago, and every attempt to do something along those lines failed. It turned out it was impossible to create something as "simple" as an application directory, connectivity requirements between applications, and the rules specifying who should have access to what resource. If we failed to get that information years ago, why should we believe we'll get it this time? Maybe because Gartner talks about ZTA this time, and so the CxOs might listen? I still don't buy it.

However, when I asked [Michele Chubirka](https://www.ipspace.net/Author:Michele_Chubirka) for her opinion on ZTA she explained it way better:

{{<long-quote>}}
Identity is the key word with Zero Trust. I’m doing a talk this week on IAM and I say the following at the very beginning, “The boundary of cloud is one of identity.” You could essentially say the same thing about the zero trust concept. The boundary is identity and the intersection with the data classification. With Zero Trust, the concept is that access is “default closed.”

To implement Zero Trust properly, you need to have a well-established, single, system of record and source of authority for identity. You would not believe how many orgs still don’t have that.

Then you need to have a data classification standard and a process for labeling data in your organization with those classes (e.g. restricted, confidential, public, etc…). Finally, with regards to applications, they should be risk tiered.

I use a pretty simple formula for this: the class of the data and the exposure of the application. For example, if it’s an externally facing app that processes restricted data (e.g. credit card numbers), then that application would have the highest risk tier. If you do all of this, then you have the appropriate logical resource hierarchy to support a Zero Trust implementation. Now you can add in authN and authZ within the context of a least-privilege design. If you do NOT do all of that, then you’re doing mobile device management, not Zero Trust.

The biggest problem I see is that no one believes that the boring prep work is important. It’s very difficult to clean up identity systems. No one wants to do a privacy inventory to determine what class of data their apps handle. Talking about results is sexier than the requirements to get to Zero Trust. 
{{</long-quote>}}

Let's be optimistic and assume we can get all those processes and frameworks in place; it's time to get our hands dirty. If you want to implement Zero Trust, you shouldn't trust the transport network, the network addresses, or the end devices. The direct consequences of those requirements: you need end-to-end encryption and user authentication on every request. That's relatively easy to do if you use web access to applications and a veritable Mission Impossible in legacy environments. But don't worry; plenty of vendors will gladly sell you magic boxes (Santa Claus not included) to replace all your outdated security appliances and fix your old stuff.

But wait, it gets worse. The high-level consulting fluff is confusing even those few security professionals who could implement ZTA. I was talking with someone working for a software development company that consistently uses infrastructure-as-code and continuous deployment processes. He couldn't figure out how to implement ZTA until I told him it's all about authenticating users and ensuring they can access only the resources (applications and data) they're authorized to access. They could already derive all that information and probably already do user authentication at the application level. ZTA seems to be a no-brainer to them, but the impenetrable detail-free fluff thrown around by vendors and industry analysts made it impossible to figure out what needs to be done (hint: NIST documents might help).

Anyway, if you're interested in ZTA and happen to be relatively close to Zurich, don't miss the October 6th [SIGS Zero Trust Workshop](https://www.eventcreate.com/e/sigs-zero-trust-training) with John Kindervag, supposedly the creator of ZTA ([Wikipedia disagrees](https://en.wikipedia.org/wiki/Zero_trust_security_model#History)) -- Gabi's events are always worth attending.
