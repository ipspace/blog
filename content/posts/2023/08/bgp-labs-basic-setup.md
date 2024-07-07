---
title: "BGP Labs: The Basics"
series_title: "The Basics"
date: 2023-08-24 06:40:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
---
The first [BGP labs](/2023/08/bgp-hands-on-labs/) are online. They cover the basic stuff (one has to [start with the basics](/2015/03/you-must-understand-fundamentals-to-be/), right?):

* [Configuring an EBGP session](https://bgplabs.net/basic/1-session/)
* [Connecting to multiple upstream ISPs](https://bgplabs.net/basic/2-multihomed/)
* [Advertise your prefixes](https://bgplabs.net/basic/3-originate/)
* [Configure BGP for IPv6](https://bgplabs.net/basic/4-ipv6/)

The labs are supposed to be run on virtual devices, but if you're stubborn enough it's possible to make them [work with the physical gear](https://bgplabs.net/external/). In theory, you could use any system you like to set up the virtual lab (including GNS3 and CML/VIRL), but your life will be way easier if you use [netlab](https://netlab.tools/) -- it [supports BGP on almost 20 different devices](https://netlab.tools/platforms/#platform-routing-support). For more details, read the [Installation and Setup](https://bgplabs.net/1-setup/) documentation.