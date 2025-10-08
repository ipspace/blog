---
title: "Why Can't We Have Good Documentation"
date: 2025-10-14 07:51:00+0200
tags: [ training ]
---
Daniel Dib [asked a sad question on LinkedIn](https://www.linkedin.com/feed/update/urn%3Ali%3Aactivity%3A7378661316384870400/):

> Where did all the great documentation go?

In more detail:

> There was a time when documentation answered almost all questions:
> 
> * What is the thing?
> * What does the thing do?
> * Why would you use the thing?
> * How do you configure the thing?

I've seen the same thing happening in training, and here's my cynical TL&DR answer: because the managers of the documentation/training departments don't understand the true value of what they're producing and thus cannot justify a decent budget to make it happen.
<!--more-->
I got my first dose of reality when attending a beta-teach of Cisco's Router Software Configuration course[^RSC]. RSC was an excellent course that met Daniel's requirements, but the new version was a watered-down affair, answering only "how do you configure that thing?"

[^RSC]: RSC -- the 1-week course that told you everything you needed to know about Cisco devices in the mid-1990s.

Everyone in the room complained[^CTM], but the people running the course and collecting our feedback were not yielding a bit. Whenever someone mentioned that a good course should cover the technology fundamentals before going into the configuration process, their answer was "_but there are generic technology courses out there, so whoever wants to know those details can attend those courses_."

[^CTM]: Obviously, I complained too much. I was never again invited to a similar event.

That situation changed dramatically when a fed-up instructor said, "_You know, more than half of my students attend the course because they've heard it's a great technology overview course. Some of them might not ever touch a router._" You could literally see Ka-Ching go on in some heads, and the technology introduction was back in the course.

The sad part of that story is that the right decision was made for the wrong reasons -- the potential increase in the sale of the student kits, instead of considering the marketing value of great training. People creating the CCNA certification and the CCNA Academy knew the importance of "infecting" people looking for generic networking knowledge with product-specific details like the configuration syntax. Once someone knows how to configure a particular device, they'll usually recommend it when making a purchasing decision (because they'll look like a wizard when it's time to configure it). Apple knew that ages ago when they started offering student discounts on their laptops.

Documentation is no different. If you learn how Spanning Tree Protocol works from Cisco's documentation, you might also learn how to configure it. Unfortunately, it takes at least an order of magnitude more effort to create excellent documentation than it takes to make an irrelevant step-by-step configuration task list followed by (oftentimes misleading or incomplete) command reference. If the documentation team cannot justify the value of excellent documentation to get a bigger budget[^RE], they have no other choice but to participate in the industry-wide race to the bottom.

[^RE]: The costs of the training and documentation teams are usually not even a rounding error in the vendor's financials.

Now, imagine the vendor then makes it easy to test the concepts on their virtual devices. Most vendors got at least that particular message, with Cisco being a sad exception (apart from the Nexus OS image). It looks like the bureaucrats won.

Fortunately, there are still organizations producing decent documentation. It was easy to figure out ~90% of the time how things work from AWS or Azure documentation. Maybe it's time we all move to the cloud 😜.