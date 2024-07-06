---
date: 2010-08-19 07:04:00.008000+02:00
tags:
- firewall
- data center
- security
title: I Don’t Need no Stinking Firewall ... or Do I?
url: /2010/08/i-dont-need-no-stinking-firewall-or-do.html
---
Brian Johnson started a lively "[*I don't need no stinking firewall*](http://markmail.org/thread/fvordsbnuc74fuu2)" discussion on NANOG mailing list in January 2010. I wanted to write about the topic then, but somehow the post slipped through the cracks... and I'm glad it did, as I've learned a few things in the meantime, including the (now obvious) fact that no two data centers are equal (the original debate had to do with protecting servers in large-scale data center).

First let's rephrase the provocative headline from the discussion. The real question is: do I need a stateful firewall or is a stateless one enough?
<!--more-->
### Quick Overview

{{<figure src="FirewallsOrRouters.jpg" caption="Firewalls or routers with packet filters?">}}

Stateless firewalling is implemented quite easily with access lists on routers, switches, and virtual switches. It usually works at line speed. Stateful firewalls implemented in routers are usually suitable for low-speed remote offices; you should use dedicated firewall devices in data centers.

For more details read also *[The Spectrum of Firewall Statefulness](/2013/03/the-spectrum-of-firewall-statefulness.html)*.

### Technology issues

Stateful firewall is the only option if you're trying to tightly protect applications that use dynamic port numbers, including everything from peer-to-peer applications (including SIP) to RPC-based applications (let's try not to call them *broken* \... how about *unpredictable applications*).

{{<note>}}You can [limit the dynamic port range for some of these applications](/2010/05/update-make-ftp-server-slightly-more.html) and allow all ports in that range through the firewall... while hoping that some other service on your server won't grab one of those ports and expose itself unnecessarily.{{</note>}}

If your applications use only well-known fixed port numbers (let's call them *fixed-port applications*), you don't have to inspect the application data stream and can match the applications with access lists; stateless solutions seem appropriate.

However, some stateful firewalls can add value even in *fixed-port* environments: they can delay the commitment of server resources to TCP sessions with [TCP SYN cookies](http://en.wikipedia.org/wiki/SYN_cookies) (also available in numerous server operating systems) and check the validity of TCP sessions.

{{<note>}}You might think that there are no vulnerabilities left in TCP that could be exploited. A long while ago, everyone thought it was impossible to establish one-way spoofed TCP sessions even though there were known vulnerabilities in TCP sequence number generation... until Kevin Mitnick proved them wrong.{{</note>}}

Last but not least, stateful firewall in front of a server can block [TCP fingerprinting](http://en.wikipedia.org/wiki/TCP/IP_stack_fingerprinting) attempts. Sometimes you simply don't want the attacker to know too much about your infrastructure.

### Design choices

There are two extremes you can be facing in a data center:

**Unified large-scale infrastructure using fixed-port applications**, including Google, Yahoo, Facebook, Twitter and a few others. You would expect to see from tens to thousands of almost-identical servers with standardized and identically configured operating system in these environments. It's quite manageable to harden and patch these servers and combined with *fixed-port* applications these environments usually offer, it makes perfect sense to be satisfied with router ACLs (and that was the case the proponents of "get rid of the firewall" line of thinking were promoting in the NANOG discussion).

**Dynamic hodgepodge of servers, operating systems and application** encountered in a usual enterprise data center. Server hardening is mission impossible (as you have so many different operating systems and/or versions of the same operating system), patching is the responsibility of individual server administrators (and they might not even be a unified team) and the applications are a nightmare from the security perspective. 

For example, I was not able to find anything from Microsoft telling me how to configure my firewall to support OWA for Exchange Server 2010; the cynical response I got from a (non-Microsoft) security engineer a few days ago was "nobody can figure out which ports it uses".

### Now what?

Obviously you're the only one who can decide where your Data Center environment is and which measures you'd like to implement, but as a generic rule, the more exposed (and the worse managed) a server is, the more you should lean toward a stateful firewall in front of it -- no wonder most enterprise data centers make heavy use of stateful firewalls.
