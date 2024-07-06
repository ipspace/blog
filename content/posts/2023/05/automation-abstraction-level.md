---
title: "Find the Optimal Level of Automation Abstraction"
date: 2023-05-18 07:03:00
tags: [ automation ]
---
_[Tom Ammon](https://www.linkedin.com/in/tomammon/) sent me his thoughts on choosing the right level of abstraction in your network automation solution as a response to my [What Is Intent-Based Networking](/2018/06/what-is-intent-based-networking.html) blog post, and allowed me to publish them on ipspace.net._

---

I totally agree with your _what_ vs _how_ example with OSPF. I work on a NOS team where if we wanted, we could say, instead of "run OSPF on these links", do this:
<!--more-->
* Send hello messages on these links
* Detect neighbors
* Transition through the neighbor states
* Form adjacencies
* Calculate best paths.

But, we would never do that. To do that at even medium scale would make the deployed network increasingly fragile as you add nodes, and it's just plain a lot of work - toil that returns no discernible operational benefit.

To me this is very much like the distinction between declarative and imperative approaches. You still have to have imperative logic at some point as you near the bottom of the stack (you can't just say to a CPU register "hey, give me the best path between A and Z!") but you get a lot of nice benefits by building things in such a way that you can trust and somewhat ignore the lower layers of the tech stack as you put your human focus on the stuff higher up. 

Lately, I've been thinking about automation (at least, the configuration management part of automation) more in terms of layers of abstraction, and one's operating position in those layers. I think the conclusion I am coming to is this: You should operate your network at the highest layer of abstraction possible that will allow you to hit your reliability, availability, and other business targets.

It takes $(effort) to automate (and maintain!) a solution to autoprovision branch routers/switches/SD-WAN appliances, configure correct BGP peers, configure endpoint ports, etc.. It takes $(effort)+N to build orchestration that will let you say "build me a branch office using the normal pattern". But it should be a conscious choice and I think proactively choosing the layer of abstraction you want to work at can be really empowering. It's really just a matter of how high an abstraction you want to ride (and crash) on.
