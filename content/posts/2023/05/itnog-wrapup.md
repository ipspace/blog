---
title: "ITNOG 7 Wrap-up"
date: 2023-05-16 06:25:00
tags: [ worth reading ]
---
I attended [ITNOG 7 last week](https://www.itnog.it/itnog7/), and thoroughly enjoyed a [full day of interesting presentations](https://www.itnog.it/itnog7/), including *[how do you run Internet services in a war zone](https://www.itnog.it/itnog7/files/13-RETN%20Presentation_Olena%20Lutsenko%20and%20Milko%20Ilari_for%20ITNOG_final.pdf)* by Elena Lutsenko and Milko Ilari.

The morning was focused primarily on BGP:
<!--more-->
* Lefteris Manassakis described how [CodeBGP tools can detect route leaks](https://www.itnog.it/itnog7/files/4-BGP%20Security%20-%20ITNOG7.pdf), including an interesting story of an Indian ISP originating a prefix for a root DNS server under its own AS.
* Ben Cartwright-Cox [introduced bgp.tools](https://www.itnog.it/itnog7/files/5-IXP%20Route%20Collection%20on%20a%20dime%20(ITNOG).pdf), including the weirdest use of 1GE transceivers I've ever seen.
* Riccardo Stagni had a [brief update on RIPE RPKI tools](https://www.itnog.it/itnog7/files/6-rpki-updates-itnog7-2023.pdf). It was really nice to see they already have some rudimentary support for ASPA.

{{<note>}}Want to know more about RPKI and ASPA? Check out the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar, including the *additional information* links in the [webinar materials](https://my.ipspace.net/bin/list?id=BGPSec).{{</note>}}

* Nicola Modena continued his journey into [underappreciated BGP features](https://blog.modena.to/), this time talking about [service insertion using BGP FlowSpec](https://www.itnog.it/itnog7/files/7-202305_BGP_Flowspec_nmodena_ITNOG7.pdf).

No event would be complete without a presentation or two about out-of-this-world hyperscaler technologies. This time, Massimo Magnani introduced gRIBI (real-world I2RS twin using gRPC as the transport protocol), and Colin Whittaker talked about custom AWS switches[^NP].

Last but definitely not least, my friend Roman Dodin had a [lovely containerlab presentation](https://www.itnog.it/itnog7/files/11-containerlab-itnog-2023.pdf), giving me a few ideas how to do a better job introducing netlab 😉, and Paolo Lucente & Salvatore Cuzzilla introduced [yet-another next-generation streaming telemetry solution](https://www.itnog.it/itnog7/files/12-telemetryITNOG23.pdf) that made my head spin.

[^NP]: Their presentations weren't online when I wrote this blog post. Check the [event page](https://www.itnog.it/itnog7/) for more details.

Finally, ITNOG stands for *Italian* Network Operators Group, so unsurprisingly the presentations of Italian speakers were in Italian. I probably managed to get the gist of most of them from the slides, but then there were some presentations like the accelerated virtual networking presentation by Samuele Pilleri where based on the diagrams I would assume it wasn't bad, but even the slides were in Italian, so whatever.

Is it worth attending ITNOG? Absolutely if you're speaking Italian. Probably even if you're not fluent in Italian[^BNC]. Will I be back? You bet.

[^BNC]: Keeping in mind Bologna is a nice city, the food is great, and the Ferrari, Lamborghini, Ducati, and Maserati museums are not far away.