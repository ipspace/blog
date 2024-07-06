---
comment: 'Assuming we forget the [ONF-promoted definition of SDN](/2014/01/what-exactly-is-sdn-and-does-it-make.html)
  and define SDN as “network programmed from a central controller”, it’s obvious we
  had SDN for decades, starting (at least) from the early 1990s.

  '
date: 2013-11-28 07:56:00+01:00
sdn_101_tag: extra
series:
- sdn_101
series_weight: 150
tags:
- SDN
title: We Had SDN in 1993 … and Didn’t Know It
url: /2013/11/we-had-sdn-in-1993-and-didnt-know-it.html
---
I had three [SDN 101](http://www.ipspace.net/SDN,_NFV_and_OpenFlow_for_Skeptics) presentations during last week's visit to South Africa and had tried really hard to overcome my grumpy skeptic self and find the essence of SDN while preparing for them. As I've been thinking about controllers, central visibility and network device programmability, it struck me: we already had SDN in 1993.
<!--more-->
In 1993 we were (among other things) an Internet Service Provider offering dial-up and leased line Internet access. Being somewhat lazy, we hated typing the same commands in every time we had to provision a new user (in pre-TACACS+ days we had to use local authentication to have **autocommand** capability for dial-up users) and developed a solution that automatically changed the router configurations after we added a new user. Here's a high-level diagram of what we did:

{{<figure src="/2013/11/s1600-SDN_1993.png" caption="Internet service provisioning architecture from 1993">}}

HTML user interface (written in Perl) gave the operators easy access to user database (probably implemented as a text file -- we were true believers in [NoSQL](http://en.wikipedia.org/wiki/NoSQL) movement in those days), and a back-end Perl script generated router configuration commands from the user definitions and downloaded them (probably through *rcp* -- the details are a bit sketchy) to the dial-up access servers.

Next revision of the software included support for leased line users -- the script generated interface configurations and static routes for our core router (it was actually an MGS, but I found no good MGS images on the Internet) or one of the access server (for users using asynchronous modems).

How is that different from all the shiny new stuff vendors are excitedly talking about? Beats me, I can't figure it out ;) ... and as I said before, you don't always [need new protocols](/2013/04/the-many-paths-to-sdn.html) to [solve old problems](/2011/09/you-dont-need-openflow-to-solve-every.html).
