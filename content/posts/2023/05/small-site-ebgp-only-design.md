---
title: "Small Site EBGP-Only Design"
date: 2023-05-03 07:03:00
tags: [ BGP, design ]
---
One of my subscribers found an unusual BGP specimen in the wild:

* It was a small site with two core switches and a WAN edge router
* The site had VPN concentrators running in virtual machines
* The WAN edge router was running BGP across WAN IPsec tunnels
* The VPN concentrators were running BGP with core switches.

So far so good, and kudos to whoever realized BGP is [the only sane protocol to run between virtual machines and network core](https://blog.ipspace.net/2016/03/dont-run-ospf-with-your-customers.html). However, the routing in the network core was implemented with EBGP sessions between the three core devices, and my subscriber thought the correct way to do it would be to use IBGP and OSPF.
<!--more-->
{{<tldr intent="Summary" model="excited ChatGPT using GPT-4 model" comment="Had to tell ChatGPT to create an exciting summary, the regular one was too boring 🤷‍♂️">}}Discover the ideal BGP design for a small site with unusual routing configurations! Dive into the pros and cons of four design options, and learn why the traditional IBGP design stands out as the top choice. Unravel the mysteries of BGP's original intent and adaptability in a growing network!{{</tldr>}}

Before going into the "_it depends on what exactly_" part of the blog post, let's list the viable design options:

* **EBGP-only design**: EBGP sessions between adjacent devices using directly-connected IP addresses.
* **Traditional IBGP design**: IGP is used to build the network topology, IBGP between loopback addresses is used to propagate external (WAN, VPN) information. Please note that this design would not reduce the number of BGP sessions between core devices[^RR]
* **IBGP-only design**: IBGP sessions are established between directly-connected IP addresses, and every device is a route reflector treating all IBGP neighbors as route reflector clients.
* **Two-way redistribution**: EBGP information is redistributed into core IGP and back into BGP (when needed) at the other edge of the network. One-way redistribution (BGP to IGP) might work if you use default routes and static advertisement of site prefix on the WAN edge router.

I could easily implement any one of the above designs, but I had enough late-night troubleshooting calls to know I shouldn't. Here are the important questions to ask when choosing the design to use:

* How supportable is it?
* How easy would it be explain it to other members of my team?
* How likely is it that someone who would have seen the device configurations for the first time would figure out what's going on?
* What is the likelihood that I’d be called at 2AM because no-one else can figure out what's wrong with the network?
* How much would I hate dealing with this network design during that 2AM call?

Based on these criteria, I'd go for the traditional IBGP design with EBGP-only design being a distant second. IBGP-only design is way outside the [Overton window](https://en.wikipedia.org/wiki/Overton_window), and two-way redistribution is a ticking bomb. Even a one-way redistribution is brittle -- all it takes to break it is an exhausted engineer throwing random commands at the network devices in a desperate attempt to make the network work.

There's another longer-term consideration: as all constants eventually turn into variables (just ask any programmer who's been around long enough), all networks inevitably grow, and you should ask yourself "_how will my design cope with a growing network?_"

Adding new switches to the network is trivial in the IBGP+IGP design: enable OSPF on core interfaces and move on. If the core switches running BGP advertise the default route into IGP, then the access switches don't need to run BGP.

Extending EBGP-only design is more interesting if you buy your hardware from the vendors that love licensing games. Years ago some vendors wanted to sell you an extra license to give you the privilege of running BGP on access switches. That might no longer be the case, but you better check in advance. Finally, some low-end gear might not be able to run BGP at all.

**Long story short:** there's a reason we've been using IBGP+IGP combo for so long (and [keep recommending it](/2023/04/multi-vendor-evpn-fabric.html)) -- that's how BGP was designed to be used, and it's always messy to try to pound a square peg into a round hole.

[^RR]: Yeah, I know you could use route reflectors, but even that wouldn't help. The proof is left as an exercise for the reader.
