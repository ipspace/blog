---
date: 2015-03-12 08:43:00+01:00
dmvpn_tag: routing
tags:
- SNMP
- DMVPN
- BGP
title: Reducing BGP SNMP Traps in DMVPN Networks
url: /2015/03/reducing-bgp-snmp-traps-in-dmvpn.html
---
One of my readers decided to [build a large DMVPN network with BGP as the WAN routing protocol](https://blog.ipspace.net/2014/03/scaling-bgp-based-dmvpn-networks.html) (good choice!) and configured BGP SNMP traps with **snmp-server enable traps bgp** command on the hub router to detect spoke router failures. Turns out that's not exactly a good idea.
<!--more-->
While the recent implementation of BGP on Cisco IOS limit the amount of syslog messages generated when a BGP neighbor is not reachable (a router would generate a logging message when the BGP neighbor is lost and when the BGP session is reestablished). BGP SNMP traps are generated more often -- every time the BGP session state machine changes state -- resulting in hundreds if not thousands of unnecessary SNMP traps.

The easiest way to get rid of this nuisance is to use dynamic BGP neighbors on the hub router -- once a BGP session with the spoke router is lost, the hub router removes the associated BGP neighbor data structures from the BGP routing process and stops caring about the lost neighbor. Unfortunately some environments abhor dynamic neighbors because someone thinks dynamic BGP neighbors pose a security risks (but dynamic OSPF neighbors are OK or what?).

Fortunately there's always yet another nerd knob to turn, in this case the **neighbor transport connection-mode passive** BGP configuration command. Once you configure a passive transport connection on a neighbor, a BGP router stops the attempts to establish a BGP session with the neighbor (and stops cycling between ACTIVE and IDLE session state); when the BGP neighbor reestablishes the TCP session, the BGP session state goes straight from IDLE to CONNECT.

### More about DMVPN

I wrote [dozens of blog posts on various aspects of DMVPN](https://blog.ipspace.net/tag/dmvpn.html), created [three webinars](http://www.ipspace.net/DMVPN_trilogy) (and a [few short videos](https://my.ipspace.net/bin/list?id=DMVPN#FREE)), and included DMVPN in [ExpertExpress case studies](http://www.ipspace.net/ExpertExpress_Case_Studies). Happy exploring!
