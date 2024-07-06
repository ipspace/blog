---
title: "Improve BGP Startup Time on Cisco IOS"
date: 2023-02-07 07:09:00
tags: [ BGP ]
---
I like using Cisco IOS for my routing protocol virtual labs[^EOS]. It uses a trivial amount of memory[^RH] and boots relatively fast. There was just one thing that kept annoying me: Cisco IOS release 15.x takes forever to install local routes in the BGP table and even longer to select the best routes and propagate them[^WIR].

I finally found the culprit: **bgp update-delay** nerd knob. Here's what the [documentation](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-a1.html#wp6262913850) has to say about it:
<!--more-->
> When BGP is started, it waits a specified period of time for its neighbors to be established themselves and to begin sending their initial updates. Once that period is complete, or when the time expires, the best path is calculated for each route, and the software starts sending advertisements out to its peers.

Why would you want to do that? Back to documentation...

> This behavior improves convergence time because, if the software were to start sending advertisements out immediately, it would have to send extra advertisements if it later received a better path for the prefix from another peer.

That makes perfect sense. It would be ridiculous to waste CPU cycles selecting the best routes based on incomplete information and telling everyone else about your wonderful "discovery" while the BGP table is still being updated with incoming messages. It's much better to keep collecting incoming updates until the neighbors tell you they're done (assuming they know what [*End-of-RIB* marker](/2021/09/graceful-restart.html) is)[^2KA] and then do your job.

[^2KA]: Or wait for two keepalives, see the [comment by Jeff Tantsura](/2023/02/cisco-ios-bgp-update-delay.html#1650).

However, that procedure works well when a single router is restarted. As _[netlab](https://netlab.tools/)_ starts lab devices in parallel and configures BGP on them at the same time, all BGP routers wait for everyone else to send them the updates. Obviously nothing happens until the **bgp update-delay** timer expires, everyone gives up, selects the current best routes (which happen to be locally originated routes), and forwards them to the neighbors... and we have fully synchronized BGP tables in a second.

The default value of **bgp update-delay** is 120 seconds -- not unreasonable if you expect to receive full Internet routing table from a few BGP neighbors, but definitely way too long for a virtual lab. Adding **bgp update-delay 5** to _netlab_ [Cisco IOS BGP configuration template](https://github.com/ipspace/netlab/commit/e6cf2976446aa0e8bee75fb27ad1f570802f0975) turned a major annoyance back into a lovely experience.

Finally, keep in mind that what works best in a lab might not be suitable for production deployment. Don't tweak this nerd knob in a production network unless you have an extremely good reason to do it, see also the [comment by Mehdi SFAR](/2023/02/cisco-ios-bgp-update-delay.html#1652).

[^EOS]: ... although I made a decision to use Arista vEOS/cEOS whenever possible when creating blog posts. Repeatability is crucial -- anyone can download Arista VM/container software while Cisco keeps hiding IOSv like it would be its crown jewels.

[^RH]: ... as opposed to resource hogs like Nexus OS or several Junos platforms.

[^WIR]: ... compared to what I'd been experiencing 25 years ago when I was still teaching my BGP course (the precursor of CBCR course) at Cisco Europe.