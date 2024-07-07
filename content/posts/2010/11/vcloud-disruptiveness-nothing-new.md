---
date: 2010-11-15 06:52:00.004000+01:00
tags:
- data center
- virtualization
title: 'vCloud Disruptiveness: Nothing New'
url: /2010/11/vcloud-disruptiveness-nothing-new/
lastmod: 2020-12-27 17:54:00
---
The [*vCloud Director: hand the network over to server admins*](/2010/11/vcloud-director-hand-network-over-to/) post received several fantastic well-reasoned comments that you should read in their entirety. [Jónatan Natti correctly pointed out](/2010/11/vcloud-director-hand-network-over-to/#2027997548220886932) (among other things) that we've often heard "*And now a networking vendor is trying to persuade people with limited exposure to \[...\] issues to rebuild \[...\]*\" where \[...\] could stand for Voice/PBX, SNA or storage.

---

**Update 2020-12-27**: The original blog post was written in 2010 when vCloud Director and the weird MAC-in-MAC encapsulation it used was all the craze in some circles (and in particular in vendor slide decks). 

The hype I was making fun of didn't last long. The encapsulation quickly got replaced by VXLAN, the whole product died a few years later, and now VMware NSX-T and VMware on AWS are the new miracle technologies.
<!--more-->
Regardless, some of us learned a few lessons, including how much you could trust a vendor marketecture, which is why I left the original blog post intact when I was cleaning up the old stuff... not that I would expect anyone to listen or to learn from our mistakes. It's so much fun to make your own.

---

Unfortunately, in a retrospective, although a lot of that noise was FUD (or resulted from excessive complexity of legacy technology), the core of those claims was often spot-on. [Ronan McGurn underestimated voice](/2010/11/vcloud-director-hand-network-over-to/#4101521757484393753) (he was part of a very large crowd, including a certain five-letter vendor) and I also have a few personal Voice/SNA campfire stories to share.
<!--more-->
When Cisco started the push to integrate SNA with IP, they knew they weren't ready (that was also the last time I've seen a vendor documenting a long-term integration strategy) and approached the subject cautiously. We were also fortunate: I knew a bit about SNA (I wrote a 3174 control unit emulator and 3270 terminal emulator a long time ago), we had an engineer who was working with SNA for years... and even then we encountered numerous unexpected problems. They ranged from buffer overflows (and SNA session resets) on low-end boxes to scalability and resilience issues with RSRB/DLSw. It took Cisco years to fix the DLSw+ TCP code, not to mention the fun we had with the Channel Interface Processor.

Voice was no different: we decided to kick out our own PBX (we were sick and tired of calling the vendor technician every time we wanted to implement a simple configuration change) and use VoIP internally (still with E1 uplink). Half of the features we had on a stupid low-cost PBX simply weren't available in the Call Manager at that time (at least CM was stable). Implementing SIP trunking with service providers was another nightmare, more so due to plethora of competing SIP standards and incompatible SIP implementations (if implementation A supports only RFC X and implementation B supports only RFC Y you have a problem).

As for SS7 (which Jónatan also mentioned), it remains as complex as it ever was and it's quite hard to get an expert when you need one. Luckily (for the VoIP people), it turned out that you don't need to use SS7 everywhere it's been used before, so you rarely see it anyway.

In both cases the networking team tried to implement changes in someone else's domain and thus had to persuade the "owner" of that domain to go along (or you'd see the vendors/system integrators trying to get CIO access to bypass the "problematic" team), so we had to do lots of field testing to prove the technology works before being allowed to implement it.

When you have the opportunity to kick out an old technology you hate and install a new one, you tend to be less cautious. A relevant example is probably MPLS/VPN -- router vendors persuading service providers that they should kick out Frame Relay/ATM gear and implement MPLS/VPN. Even when the gear was ready (and baseline MPLS/VPN was working quite well at the time the majority of the providers were trying to implement it), some service providers implementing the technology weren't.

As a result, some of our enterprise customers regularly practiced "let's wait a few years" (or "let's make sure our backup works") attitude toward any new SP offering -- they stayed on channelized E1 a few years after Frame Relay became available and stuck with Frame Relay long after MPLS/VPN services became available... just because they couldn't trust their service provider to do the job properly.

Is this relevant to the vCloud discussion? It probably is -- I'm positive many server administrators are well aware of the underlying complexities and the game VMware is playing and will tread cautiously (and if I helped them a little bit, that's more than enough).

In an ideal situation, the server administrators will sit down with the networking engineers and figure out how to make the whole thing work once the product becomes stable (as I wrote, the architecture is not necessarily bad). And then (as Odd Stoltenberg nicely explained) there will be those that will decide this is an ideal opportunity to get rid of the troublesome networking people... and a few of them will experience unexpected results.

[Matthew Lodge also made an excellent point](/2010/11/vcloud-director-hand-network-over-to/#2367370681251890125): we need to solve the problem of integrating private and public clouds. I just fail to see how a technology that has MAC-in-MAC encapsulation at its pinnacle serves that need -- if they had decided to use IP encapsulation, I would have applauded, as that would have nicely solved underlying transport scalability (not to mention that it would get rid of inter-DC layer-2 madness we have to deal with today).

Last but maybe not least -- just in case you're wondering how far off the mark I was when I wrote the whole thing goes beyond a technology solution, [read this tweet](https://twitter.com/OVHcloud_US/status/2445278263123968).
