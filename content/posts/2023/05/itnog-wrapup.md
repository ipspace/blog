---
title: "ITNOG 7 Wrap-up"
date: 2023-05-30 19:43:00
draft: True
tags: [ worth reading ]
---
I attended ITNOG 7 I early May 2023, and thoroughly enjoyed a [full day of interesting presentations](https://www.itnog.it/itnog7/), including *how do you run Internet services in a war zone* by Elena Lutsenko and Milko Ilari.

The morning was focused primarily on BGP:
<!--more-->
* Lefteris Manassakis described how CodeBGP tools can detect route leaks, including an interesting story of an Indian ISP originating a prefix for a root DNS server.
* Ben Cartwright-Cox introduced bgp.tools, including the weirdest use of 1GE transceivers I've ever seen.
* Riccardo Stagni had a brief update on RIPE RPKI tools. It was really nice to see they already have some rudimentary support for ASPA.

{{<note>}}Want to know more about RPKI and ASPA? Check out the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar, including the *additional information* links in the [webinar materials](https://my.ipspace.net/bin/list?id=BGPSec).{{</note>}}

* Nicola Modena continued his journey into underappreciated BGP features, this time talking about service insertion using BGP FlowSpec.

No event would be complete without someone a presentation or two about out-of-this-world hyperscaler technologies. This time, Massimo Magnani introduced gRIBI -- real-world I2RS twin using gRPC as the transport protocol -- and Colin Whittaker talked about custom AWS switches.

ITNOG stands for "Italian Network Operators Group", so unsurprisingly the presentations were in Italian, and while I managed to get the gist of most of them, sometimes I got lost. Paolo Lucente & Salvatore Cuzzilla probably did a good job describing next-generation network telemetry, and based on the diagrams the I would assume the accelerated virtual networking presentation by Samuele Pilleri was also good, but as he was the only one with Italian slides I really can't tell you ;)

Last but definitely not least, my friend Roman Dodin had a lovely containerlab presentation, giving me a few ideas how to do a better job introducing netlab ;)