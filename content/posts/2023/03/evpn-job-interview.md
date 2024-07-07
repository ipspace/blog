---
date: 2023-03-29 06:31:00+00:00
evpn_tag: intro
tags:
- EVPN
title: Studying EVPN to Prepare for a Job Interview
---
An ipSpace.net subscriber sent me this question:

> I am on job hunting. I have secured an interview and they will probably ask me about VxLAN BGP EVPN fabrics. If you have some time, it would be a great help for me if you could tell me 1 or 2 questions that you would ask in such interviews.

**TL&DR:** He got the job. Congratulations!
<!--more-->
I was fortunate enough never having to apply for a job (I was either a co-owner of a company or working on my own), and the last time I was involved in a hiring decision was over 20 years ago, so I'm not an accurate source of _interview questions_ ideas. However, what I did in those days was try to figure out whether:

* People knew their stuff at the approximate level of what they claimed their knowledge to be;
* They understood the fundamentals;
* They could get a (relatively) simple job done given all the documentation they need (we gave them a few hours for that part).

For that last bit, one could build a lab with preconfigured IP routing, and ask the candidate claiming to be fluent with boxes from vendor X to build EVPN/VXLAN fabric on top of that lab[^LG] given the vendor product documentation[^CG]. [_netlab_](/tag/netlab/) would be an easy way to set up that lab.

[^LG]: I vaguely remember someone telling me that approach might not be legal in some parts of the world. Comments from someone more familiar with such restrictions (should they happen to be real) would be appreciated!

I would always combine such a lab exercise with a followup Q-and-A session similar to what the ancient CCIE lab exams had[^RT]. I would ask the candidate why he used particular configuration commands, what those commands did, and what the **show** printouts mean. Explaining EVPN route types could be an excellent starting point.

[^RT]: That's how I lost one point on the CCIE lab exam: I got stuck on OSPF type-2 LSA.

[^CG]: In the world of ChatGPT you might want to limit the resources they can access... or you could let them generate the configuration with a large language model to test their troubleshooting skills 😁

Back to fundamentals -- here are just a few ideas for the questions you might want to consider:

* Why do we need VXLAN transport? What problem is it solving?
* Why do we need EVPN? What problem is it solving?
* Could we use VXLAN without EVPN? What would be the drawbacks?
* Why do we need proxy ARP?
* How does EVPN propagate ARP requests?
* Can you use IP multicast with EVPN and why would you want to?
* What is the role of anycast gateway?

{{<note info>}}Have a hard time answering these questions? You'll find the answers somewhere in [VXLAN Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) and [EVPN Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinars ;){{</note>}}

Want a tougher challenge?

* Why do some vendors advertise host IP addresses as RT5 prefixes?
* How does EVPN solve VM mobility challenges?
* Are different EVPN vendor implementations interoperable?
* What are good interoperability practices for EVPN?
* What are the differences between MLAG and EVPN dual-homing?

{{<note info>}}The last three questions were contributed by Dinesh Dutt (thank you!!!), and you'll find the answers to two of them in his [Multivendor Data Center EVPN](https://my.ipspace.net/bin/list?id=EVPN#MULTIVENDOR) presentation.{{</note>}}

If you happen to have too much time, I have another _fundamentals_ idea: we created tons of review questions for the  [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar. You might want to go through them although they don’t ever get close to VXLAN/EVPN.