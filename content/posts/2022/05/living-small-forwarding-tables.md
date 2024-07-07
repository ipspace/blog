---
title: "Living with Small Forwarding Tables"
date: 2022-05-09 06:46:00
tags: [ IP routing, switching ]
---
A friend of mine working for a mid-sized networking vendor sent me an intriguing  question:

> We have a product using an old ASIC that has 12K forwarding entries, and would like to extend its lifetime. I know you were mentioning some useful tricks, would you happen to remember what they were?

This challenge has no perfect solution, but there are at least three tricks I've encountered so far (as always, comments are most welcome):
<!--more-->
* Conversational learning
* Virtual aggregation
* Selective route download

### Conversational Learning

Conversational learning is what you use when you failed to learn the [packet forwarding history lessons](/series/forwarding/):

* Build a forwarding table (Forwarding Information Base -- FIB) in software
* Start with empty hardware FIB, and punt all forwarded packets to the CPU
* Whenever a new packet arrives to the CPU, find corresponding forwarding entry in the software FIB and install it in the hardware FIB

Congratulations, you reinvented [cache-based forwarding](/2022/02/cache-based-forwarding/), and you'll have to deal with cache coherence, cache aging and eviction, and you'll fail miserably when someone starts scanning the address space. It's also a bit hard to implement a default route in hardware FIB. The proof is left as an exercise for the reader.

All that obviously doesn't stop the networking vendors from retrying to reinvent this particular broken wheel whenever their hardware designers mess up (see also: Nexus 7000 F1 linecard), or whenever they have a bit of hardware they're desperate to sell (see also: [SmartSwitches](https://www.theregister.com/2021/10/19/aruba_puts_dpus_in_a_switch/)).

### Virtual Aggregation

Conversational learning or any other cache-based forwarding *might* work within a small network where the number of potential destinations is comparable to the hardware FIB size. Trying to use the same trick with the Internet Default Free Zone (DFZ) is a recipe for disaster as Cisco discovered ages ago when their *fast switching*  mechanism caused severe brownouts in large ISPs.

Here's another idea from the MacGyver & Co:

* Imagine an edge router connected to two ISPs that happens to have small FIB and full DFZ BGP table (because whatever crazy reason).

``` diagram
┌────────────┐      ┌────────────┐
│   ISP-A    │      │   ISP-B    │
└────────────┘      └────────────┘
        ▲                ▲
        │                │
        │ ┌────────────┐ │
        └─┤    EDGE    ├─┘
          └────────────┘
```

* Now assume that one of the ISPs is the transit ISP, and use a default route toward it. Bonus points if the default points to 1.1.1.1 or 8.8.8.8 to cope with ISP's bad hair day[^HIST]
* Once you have a more-specific and a less-specific prefix *pointing to the same next hop* in your routing table, you don't have to install the more-specific prefix in the hardware FIB[^CAVEAT]

Obviously you're trading FIB size for convergence time. For example, you cannot use [Prefix Independent Convergence](/2012/01/prefix-independent-convergence-pic/). You could also get into a situation where a particular failure scenario explodes the hardware FIB size beyond its capabilities. An example might be the primary ISP losing most of the DFZ BGP table while still announcing prefix toward the IP address you use as the next hop of the default route.

### Selective Route Download

DFZ BGP table has almost a million entries, but you could safely ignore most of those prefixes. After all, do you really care about clients in Fiji or Madagascar trying to reach your e-commerce server when you don't even ship to those countries? It turns out that in most cases a few thousand prefixes cover more than 90% of your Internet traffic. Combine that with the a reliable default route and you're done. Now for the tricky question: how do you select those prefixes?

You could rely on a good network design. For example, if you're peering at an Internet Exchange Point (IXP) and use an upstream ISP, the you don't care about any prefix not advertised from the IXP peers:

* Set up a default route pointing to the upstream ISP
* Filter out all other prefixes received from the upstream ISP
* Set a limit on the number of prefixes accepted from every IXP peer[^FFI]
* Go have a well-deserved beer[^BEER].

[^FFI]: You don't want them to dump the whole DFZ BGP table into your lap due to a fat-finger incident.

Unfortunately it's a bit hard to package that idea into a shipping product when you know your customers will try to misuse your software in every imaginable way (and a gazillion others). That's when it's time to fall back to traffic monitoring:

* Using the forwarding table, and whatever traffic monitoring technology you have available, identify the "hot" prefixes
* Create a prefix list and use it as a filter between routing table and hardware forwarding table.
* Periodically update the prefix list to cope with shifts in traffic patterns.

The *selective route download*[^SRD] functionality is available in (at least) Arista EOS, Junos, and Cisco IOS XE. If your favorite box supports it, please leave a comment.

[^SRD]: *Selective Route Download* usually works as a filter between BGP table and routing table (RIB), not between routing table and FIB. If that's the case on your platform, you can only use it for BGP routes.

For more details: 

* Listen to the [SDN Router @ Spotify](/2015/01/sdn-router-spotify-on-software-gone-wild/) chat with David Barroso, and follow the related links.
* In a [follow-up episode](/2015/10/sdn-internet-router-is-in-production-on/), David described the operational experience (spoiler : it turned out in most cases they didn't have a problem at all).
* I also covered the idea in the _[SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases)_ webinar.

[^HIST]: I wrote a ton of blog posts [dealing with similar scenarios](/2007/11/bgp-default-route/) ages ago. Search for [BGP blog posts](/tag/bgp/) written between 2006 and 2010.

[^CAVEAT]: With a few caveats left for the reader to figure out. You could cheat and use [RFC 6769](https://www.rfc-editor.org/rfc/rfc6769.html) as an inspiration.

[^BEER]: Or another beverage of your choice. You can even make it a non-alcoholic beer.