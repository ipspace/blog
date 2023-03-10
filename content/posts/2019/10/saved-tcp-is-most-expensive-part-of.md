---
date: 2019-10-29 10:56:00+01:00
multihoming_tag: session
series:
- multihoming
tags:
- TCP
- data center
title: 'Saved: TCP Is the Most Expensive Part of Your Data Center'
url: /2019/10/saved-tcp-is-most-expensive-part-of.html
---
Years ago [Dan Hughes](https://www.linkedin.com/in/danhughes1234ie/) wrote a great blog post explaining how expensive TCP is. His web site is long gone, but I managed to grab the blog post before it disappeared and he kindly allowed me to republish it.

---

If you ask a CIO which part of their infrastructure costs them the most, I'm sure they'll mention power, cooling, server hardware, support costs, getting the right people and all the usual answers. I'd argue one the the biggest costs is TCP, or more accurately badly implemented TCP.
<!--more-->
Ask any CCNA what is the difference between UDP and TCP and they'll tell you 'reliability'. But let's look at what do we mean by that, and why it costs money.

Take a simple client/server application (or weblayer-\>app layer - it doesn't really matter) and think about reliability of that connection. There are two things that matter :

1.  can it handle packet loss, and if so how much
2.  can it handle the individual TCP connection being reset and try again

Most apps rely on TCP to handle point 1, but point 2 is the really interesting one. Imagine a world where your application vendors were mandated to make their TCP connections retry. You can now:

1.  Load balance them to a different host
2.  pass them through a different firewall - without any state sync

So, things you no longer need:

-   VMotion
-   Fabricpath
-   L2 networks
-   state failover between firewalls/LBs

This completely changes your cost model, you no longer need the super expensive VMware - you can use the free version because you don't need the VMotion. You don't need fancy nexus switches, you can use whoever gives you the best bang for your buck. You don't need to buy the whole lot from one vendor, you can use commodity, or whoever suits you best. And you don't need any of this crazy L2 networking that people are using to leave landmines all over the network. You can build a nice simple hierarchical L3 network. You can just put one firewall in each location, and have it advertise a default.

vMotion is a truly amazing piece of technology, but it's become a crutch to avoid fixing the very simple problem of 'make my TCP connection retry'. And with the converged infrastructures now being sold by the big vendors, it's become an excuse to keep you the customer in the premium equipment world, and is stopping you saving money by moving to commodity.

So, dear CIO, do a simple bit of maths. Work out the difference between being able to buy cheap servers/network/storage, and premium ones. Add in the extra support costs. Add the saving from having half the number of firewalls and load balancers. That's probably quite a big number.

Now, work out the SDE time to make your applications do the right thing. Bet you'll earn a bonus from this one ;-)

---

As I keep saying, we\'re still paying for the \"wisdom\" of the ancients who decided that [TCP/IP doesn\'t need a session layer](https://blog.ipspace.net/2009/08/what-went-wrong-tcpip-lacks-session.html)\...
