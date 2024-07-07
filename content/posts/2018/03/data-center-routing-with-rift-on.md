---
date: 2018-03-30 09:33:00+02:00
dcbgp_tag: newrp
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_88-RIFT.mp3
series:
- dcbgp
series_title: Data Center Routing with RIFT with Dr. Tony Przygienda
series_weight: 900
tags:
- podcast
- data center
- IP routing
- Software Gone Wild
title: Data Center Routing with RIFT on Software Gone Wild
url: /2018/03/data-center-routing-with-rift-on/
---
Years ago Petr Lapukhov decided that it's a waste of time to try to make OSPF or IS-IS work in large-scale data center leaf-and-spine fabrics and figured out how to [use BGP as a better IGP](/2016/02/using-bgp-in-data-center-fabrics/).

In the meantime, old-time routing gurus started designing routing protocols targeting a specific environment: highly meshed leaf-and-spine fabrics. First in the list: Routing in Fat Trees (RIFT).
<!--more-->
In Software Gone Wild [Episode 88](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_88-RIFT.mp3) we sat down with [Dr. Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501), author of [RIFT](https://tools.ietf.org/html/draft-przygienda-rift-05), and Jeff Tantsura, chair of the [RIFT IETF working group](https://datatracker.ietf.org/wg/rift/about/).

We started with tons of background topics:

-   Do we even have a problem?
-   Why is BGP not good enough, and why do we need another routing protocol?
-   What are the big players doing?
-   Why can't we use OSPF or IS-IS in large highly meshed fabrics?
-   Do we really need (transport) policies and traffic engineering in data centers, or is it better to buy more bandwidth?
-   Is it worth solving the problems in the network, or should they be solved on the hosts?

After wasting 20 minutes on describing the problem we finally got to the interesting stuff:

-   What is RIFT? What environments is it supposed to be working in?
-   How can you combine the benefits of link-state and distance-vector technologies in the same routing protocol?
-   How RIFT uses automatic deaggregation to avoid black holes caused by aggressive summarization
-   What has RIFT borrowed from other routing protocols and what's unique?
-   RIFT is schema-based (not TLV-based) protocol. What does it mean and why does it matter?
-   Why is RIFT running on top of UDP and not using a separate Ethertype like IS-IS
-   How is flooding implemented in RIFT and what are flooding scopes? 
-   Why is directionality (east-west versus north-south) so important to RIFT?
-   What happens when your data center fabric has leaf-to-leaf shortcuts?
-   How does RIFT figure out the position of an individual switch (leaf or spine) within the fabric?
-   How can you use key-value store embedded in RIFT to implement zero-touch provisioning?

Interested? You'll find all the details in [Episode 88](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_88-RIFT.mp3) of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild).

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_88-RIFT.mp3)
{{</jump>}}
