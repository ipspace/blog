---
date: 2012-04-03 07:37:00.001000+02:00
tags:
- VXLAN
- switching
- data center
- overlay networks
- LISP
- virtualization
title: 'Networking Tech Field Day #3: First Impressions'
url: /2012/04/networking-tech-field-day-3-first.html
---
Last week [Stephen Foskett](http://blog.fosketts.net/about/stephen-foskett/) and [Greg Ferro](http://etherealmind.com/) brought back their merry crew of geeks (and a [network security princess](http://twitter.com/MrsYisWhy)) for the [third Networking Tech Field Day](http://techfieldday.com/2012/nfd3/). We've met some exciting new vendors (Infineta and Spirent) and a few long-time friends (Arista, Cisco, NEC and Solarwinds).

Infineta gave us a fantastic deep-dive into deduplication math, and Spirent blew our socks off with their testing gear. As for the generic state of the networking industry, [William R. Koss](http://about.me/billtrap) nicely summarized my feelings in a [blog post published last Friday](http://siwdt.com/2012/03/31/notebook-03-13-12-datacenter-equities-and-hpc-for-wall-street/):
<!--more-->
> I really did not see anything new, just more of the same. Presenters should be banned if they reuse an old presentation. Innovation seems dormant and no amount of science projects and Crossing the Chasm buttering will take the place of bold innovation.

To make matters worse, some vendors seem to promote ["monkey wiring" design](https://blog.ipspace.net/2012/04/monkey-design-still-doesnt-work-well.html) along the lines of "our fabrics are so versatile you can just wire switches together and everything will work". Not sure why I remain skeptical -- maybe I've seen too many such designs in the past explode in their owner's face (after the "architect" had been long paid and gone).

However, all is not bleak. Here are the (positive) highlights:

**We haven't seen too many rainbow fields and dancing unicorns**. Apart from the idea to transport VXLAN between data centers over an OTV tunnel to solve the lack of end-to-end multicast, nobody presented a solution that I would disagree with from the architectural perspective.

Some products are lacking badly-needed features (and don't worry, I'll write about them), but that's not something that couldn't be fixed with proper amount of programming elbow grease.

**The VM mobility ideas are experiencing soft landing**. While we'll undoubtedly continue to see cloud-sailing consultants (and an occasional vendor or two) selling stupidities that work only in PowerPoint, some (vendor) engineers totally get it.

The presentation from Victor Moreno (Cisco) was fantastic -- he clearly understands all use cases, the viability of each one of them (from clustering to cold and hot VM migration) and their technical requirements. A proper combination of VXLAN, LISP and OTV might actually work reliably once it's implemented (current status: it's on the roadmap) and properly tested (my expectations: 18 months from now).

**We just might get rid of boring details**. Arista is clearly on a mission to make our life easier with small, focused and (most importantly) useful features. The ones we've heard about this time:

-   XMPP client in Arista EOS allows you to execute the same command in a group of switches (similar to what you can do with QFabric);
-   Using Zero-touch configuration, a switch passes a list of its LLDP neighbors to a web server when asking for configuration. You can use that list to build dynamic ToR switch configurations that adapt to the actual data center wiring.

Don't know about you, but I would always prefer spending my time tweaking a cool web app that would auto-provision switches than typing the almost-the-same list of CLI commands in a SSH session.

**Interesting combos**. [Arista added FPGA to some of their switches](http://www.networkcomputing.com/next-gen-network-tech-center/232700283?queryText=arista%20networks), allowing their customers to program high-speed applications. Obviously that's not something you'd do at home (and Doug Gourlay was very clear about that), but the possibilities are mind-blowing: from trading floor applications (that he mentioned) to video transcoding and deep packet inspection.


### Disclosure

You probably know by now how Tech Field Days work: we're not paid to be there or write about what we've seen, but vendors indirectly pay for our expenses (travel, food, and lodging). Also, we're never asked to write about a vendor or a product (I always skip a vendor or two as they're not up my alley), and the only way vendors can influence what I write about them is through their presentations and (more importantly) answers to my questions.

In case you need something slightly more formal, read what [Tony Bourke](http://datacenteroverlords.com/2011/10/31/brace-yourself-networking-field-day-posts-are-coming/), [Matt Simmons](http://www.standalone-sysadmin.com/blog/2011/10/brocade-ethernet-fabric-races/) and [Tom Hollingsworth](http://networkingnerd.net/2012/02/27/network-field-day-the-third/) wrote.
