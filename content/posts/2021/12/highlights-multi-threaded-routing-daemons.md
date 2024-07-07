---
title: "Highlights: Multi-Threaded Routing Daemons"
date: 2021-12-07 07:53:00
tags: [ IP routing, BGP ]
---
The *[multi-threaded routing daemons](/2021/11/multi-threaded-routing-daemons/)* blog post generated numerous in-depth comments here and on LinkedIn. As always, thanks a million for keeping me honest and providing more details or additional perspectives. Here are some of the best bits.

Jeff Tantsura provided the first dose of reality:

> All modern routing protocols implementations are multi-threaded, with a minimum separation of adjacency handling, route calculations and update generation. Note - writing multi-threaded code for complex tasks is a non trivial exercise (you could search for thread safety and similar artifacts and what happens when not implemented correctly). Moving to a multi-threaded code in early 2010s resulted in a multi-release (year) effort and 100s of related bugs all around.

Dr. Tony Przygienda added his hands-on experience (he's been developing routing protocol software for ages):
<!--more-->
> There is nothing special in NOSes about preemption or thread safety as paradigms AFAIS except maybe that we compute on inconsistent state assuming epsilon consistency while having to meet soft and hard time constraints. So it's just advanced system programming with usual design trade-offs in terms of primitives & their performance/complexity impact with a sprinkling of load shedding work preserving schedulers. Tricky part IMO is to have specs written in a way that allow for better (i.e. less fragile parallel designs in terms of correctness, reliability and maintainablity). Even with such specs, good parallel designs in this space is not a given, it's pretty easy to end up with a non-obviously "bad" parallel design. Proper parallel system architecture/design under those conditions is then partially a question of experience & the tooling available/chosen so more of an art/craft than simple engineering discipline or trade-off. All this is way too long and acrybic and convoluted for a "short writedown". And such a writedown is guaranteed to put to sleep everyone except a handfull of people deep into programming such systems ;-)

His conclusions:

> Which does not mean you should thread/parallelize happily as your first choice if you don't have good amount of experience with it. It's a very sharp knife to grab as a tool design and implementation wise.

Henk Smit started with "_let's define what the hard problem is_":

> Multi-threading where you divide your workload in a fixed number of threads doesn't count. That's relatively trivial. E.g. a hello thread, an update thread and a route-computation thread. That's still O(1) scalability. To be able to brag, your code should be able to used a large number of cores on your route-processor.

He also pointed out things get interesting once you get beyond a single forwarding instance:

> Another thing to consider is how router OS's deal with multiple VRFs. Suppose you have a 1000 VRFs on a PE, and each VRF runs a routing protocol with a CE. What are you going to do? Spawn a 1000 processes? That doesn't scale really. Have one process per routing protocol, with 1 thread per VRF? Or are you going to use worker-threads? These are the harder questions.

Justin Pietsch approached the lack of massive multi-threading from the "_others have solved it, why can't we_" perspective:

> I'm disappointed that there aren't more scalable solutions. I want BGP daemons to catch up to modern databases. How do we get Network router vendors to think the same way that current database people do, they should not be held back by hardware and they should take advantage of hardware. At what point do I take an in memory no-sql database and hook on a simple BGP protocol parser?

Back to Henk, he made a similar point:

> I am surprised about the lack of true improvement BGP implementations have made in the last 20 years. I mean architectual and performance wise. A lot of work has gone into the protocol (writing RFCs). But not in the implementations themselves, it seems. I guess it is easer to write drafts than to write code. As far as I know, there is no BGP implementation that does everything multi-threaded at scale. Reading from sockets, doing ingress policy, bestpath-computation, route-installation, egress-policy, generating output updates. It should be possible to do all of that on multiple cores, in every stage. Some stages require locking, or must be single-threaded. E.g. installing new routes in the Adj-RIB-In. But other things (policy, bestpath computation, rib-install, update-generation) you can do on many cores in parallel.

Finally, Minh Ha pointed to another elephant lurking in the corner. It doesn't help to have a perfect routing daemon implementation if it takes forever to install routes into FIB:

> But the FIB download time is most crucial. Again this problem has been known for over 10 yrs; it's the FIB download and installation time that's the biggest bottleneck in modern routers, not the control-plane side of thing. And this problem gets exponentially worse the higher the number of routes one has in the RIB. In short, according to Juniper, RIB sharding may or may not help with FIB download time. I suppose there's only so much maths/algorithmics can do in the face of physical constraints.

Also from Minh - as the code gets more complex, it's harder to optimize it:

> Henk's point on the lack of improvement in BGP implementation in the last 20 yrs is very much worth paying attention to, and his remark "it is easer to write drafts than to write code" is spot-on. Could it be that due to the explosion of the code base, now in the hundred thousand lines of code, it's simply led to architectural dead end due to complexity and therefore, too hard to convert this code base into a multithreading equivalent?
>
> Among the biggest issues of multithreading are synchronization and inter-dependency, and this gets much harder to solve as the code gets more and more complex. Inter-thread synchronization overhead and OS-scheduler inefficiency are the main reasons why as we start to add more core, performance will hit a peak and then reverse as more cores are added. In fact, Juniper's RIB sharding touches on this topic as well.
>
> So not only do we need better implementation of protocols, don't forget the centralized (again, centralization doesn't scale) OS scheduler will be one of the biggest, if not the biggest bottleneck, as you have more and more cores at your disposal. This problem is exactly the same one plaguing router's crossbar fabric, as the central scheduler hits its limit when interface speed improves by leaps and bounds.
>
> And don't forget the compiler. Just because CPU vendors come up with more cores, doesn't mean they can come up with a superb compiler that can generate codes that take advantage of the cores. The failure of VLIW/EPIC Itanium is a glaring example; certain things only work in PPT. When it comes to massive parallelism, we can't omit any factor as they're not isolated, but interplay into complex outcomes.

So now we know we're dealing with a really hard problem, and maybe the lack of progress indicates it's not worth solving? Here's what Henk had to say:

> I wonder why nobody has attempted to write such a "perfect" implementation yet. And I wonder why nobody has asked for one. Maybe current implementations are deemed "good enough"?

And the final thoughts of Minh Ha:

> In a word, imho, don't expect any significant improvement in quality of BGP implementations anytime soon. Plus pay more attention to the FIB download and insertion bottleneck. This can be the most painful part of the problem and can get really nasty at the million-route scale or higher.

I plan to revisit this topic in a few years -- let's see how much real-life adoption Junos RIB sharing and similar approaches get.
