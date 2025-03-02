---
title: "Learning Networking Fundamentals at University?"
date: 2020-12-10 07:43:00
tags: [ networking fundamentals ]
networking-fundamentals_tag: important
weight: 900
---
One of my readers sent me this interesting question:

> It begs the question in how far graduated students with a degree in computer science or applied IT infrastructure courses (on university or college level or equivalent) are actually aware of networking fundamentals. I work for a vendor independent networking firm and a lot of my new colleagues are college graduates. Positively, they are very well versed in automation, scripting and other programming skills, but I never asked them what actually happens when a packet traverses a network. I wonder what the result would be...

I can tell you what the result would be in my days: blank stares and confusion. I "enjoyed" a half-year course in computer networking that focused exclusively on history of networking and academic view of layering, and whatever I know about networking I learned after finishing my studies.
<!--more-->
I checked the [curriculum of my alma mater](https://www.fri.uni-lj.si/upload/Slike/predmetniki/2020EN_BUN_RI.pdf) and things are getting both better and worse. Instead of a single course they offer [four communications-related courses](https://www.fri.uni-lj.si/upload/Zborniki/1000468_BUN_RI_UNP_Ra%C4%8Dunalni%C5%A1tvo%20-%20Copy%202.pdf)... as an elective module, which means that most of the graduates could be hard-pressed to recognize an IP address if it stared at them from the source code. One of those courses focuses on pure networking, another one is a distributed systems course (covering everything from NUMA to energy efficiency of distributed computing), the third one is a modeling course focusing on queuing theory, and the fourth one covers wireless and mobile networks.

Also keep in mind that [each CCNA-level course](https://www.netacad.com/courses/networking) has approximately the same length as one of those courses, so you can't expect someone finishing them to be much beyond the CCNA level of understanding.

On the other hands, Physics is a mandatory course, so after getting a Computer Science degree you'll know how to compute acceleration, forces, and momentum (maybe that's really important if you decide to start developing first-person shooter games), but not how to build a well-behaved distributed application. No wonder the problems [keep getting pushed down the stack](/2013/04/this-is-what-makes-networking-so-complex/) and [software developers keep reinventing networking](/2020/02/the-never-ending-my-overlay-is-better/) using [NAT and PBR](https://rule11.tech/the-experience-has-shown-that-keyword-rfc2915-rule-4/). Good job.

I wonder whether the situation is better elsewhere -- your comments are most welcome.

So, you get an enthusiastic engineer eager to work on computer networks and slightly underprepared after finishing a 3-year university program. What can you do? If you're in a small generalist IT team your best bet is to [assign them a mentor and hope for the best](https://www.ipspace.net/Developing_engineers_through_the_mentoring_process), but if you need more than an occasional new hire every few years you can do much better: train them.

When I was still working for a reasonably-sized system integrator we created our own training program, used our Cisco-certified instructors to run new-hire internal courses, and concluded the bootcamp with a hands-on exercise that included designing a small network, implementing it (using actual hardware so they figured out the difference between Ethernet and power cable), and presenting the solution to the customer (yes, we also worked on their presentation skills). 

It's not that hard to create your own version of the same idea, all you have to do is to realize you're in it for the long run and should invest into engineers you will need for the complex projects years down the road... and if you need someone to help you get started, I might know just the right person to do it.
