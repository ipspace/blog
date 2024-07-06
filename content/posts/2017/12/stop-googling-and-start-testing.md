---
date: 2017-12-05 08:16:00+01:00
ospf_tag: rant
tags:
- OSPF
- MPLS VPN
title: Stop Googling and Start Testing
url: /2017/12/stop-googling-and-start-testing.html
---
Here's a question I got on one of my ancient blog posts:

> How many OSPF process ID can be used in a single VRF instance?

Seriously? You have to ask that? OK, maybe the question isn't as simple as it looks. It could be understood as:
<!--more-->
-   Can I have multiple OSPF processes in a single VRF instance?
-   Can I have many OSPF processes in a single VRF instance?
-   What is the maximum number of OSPF processes in a VRF instance?
-   What is the maximum number of processes in an instance, and is it a fixed number, or does it depend on the platform?

Before even trying to answer the question, you should ask yourself, "*what am I doing, and how did I get painted into this terrifying corner*" -- most questions like this result from a broken design. Even if you get the answer you like, you might be one of the very few people worldwide deploying this particularly crazy idea, so you might hit bugs that nobody has ever encountered before. Good luck getting them fixed unless you're buying millions worth of equipment per quarter ;) Or, as Andrius Adamavicius wrote in the comments:

> If you tested and it worked this is no way an indication that it is supported.
>
> Read documentation, especially Restrictions and Limitations sections, before putting anything in production deployment. Google is very efficient way to navigate vendors documentation that spans multiple unconnected or unlinked documents. If can\'t find an answer - open a ticket with your vendor to clarify specify SW/HW combo features/limitations.
>
> The prime abusement is \'ip nat enable\' where folks use it as a replacement for \'ip nat inside/outside\'. If both are working in the global routing table does not mean that both are supported. So, when something fails in production, after \'about 15 seconds\' of testing in the lab, then network redesign might be the only option.

Sometimes, when you start considering unusual ideas, it's worth stepping back and figuring out the original problem and whether you can solve it in some other way.

**Now, back to the question itself.**

Answering the first question yourself is straightforward -- you spin up a virtual router. If you work with Cisco IOS and don't have one on your laptop yet, it's time to fix that anyway. It took me about 15 seconds to get the answer from my decade-old Cisco 1812: yes, you can have more than one OSPF process per VRF (however, that does NOT mean that it's a good idea or supported; see also above).

The second question is also pretty easy to answer -- create a very large configuration, download it to the router, and see what happens. You could use something as simple as Notepad, or stop wasting your time with cut-and-paste and use Excel, Perl, Python, Ansible, or whatever else.

The answer to the third question might be \~30 (see [this article](/2009/05/vrf-routing-process-limitations.html) I wrote in 2009) due to internal IOS architecture, or more. Yet again, it's easy to test.

If the answer to the third question is way above 30, I don't think many people know what it depends on, but if you desperately want an authoritative answer, you should ask your Cisco SE and not a random blogger anyway.

Anyway, what disappointed me most was that whoever asked that question knew what Cisco IOS is, what OSPF is, and what VRF is... and yet he found it more appealing to waste time googling around and asking random people than to check things out (or asking the people who should know -- the vendor -- if he wanted a definitive answer), and maybe even sharing the results after figuring out what the answer is.
