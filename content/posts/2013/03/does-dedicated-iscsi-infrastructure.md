---
date: 2013-03-21 07:30:00+01:00
tags:
- data center
- SAN
- FCoE
- high availability
title: Does dedicated iSCSI infrastructure make sense?
url: /2013/03/does-dedicated-iscsi-infrastructure/
---
[Chris Marget](http://www.fragmentationneeded.net) recently asked a really interesting question:

> I've encountered an environment where the iSCSI networks are built just like FC networks: Multipathing software in use on servers and storage, switches dedicated to "SAN A" and "SAN B" VLANs, and full isolation of paths (redundant paths) between server and storage. I understand creating a dedicated iSCSI VLAN, but why would you need two? Isn't the whole thing running on top of TCP? Am I missing something?

Well, it actually makes sense in some mission-critical environments.
<!--more-->
First, there's the [layer 8-10](http://en.wikipedia.org/wiki/Layer_8) part: Things you do will never fail (after all, you're doing them). Things that are far enough from you (and thus you're totally clueless about them) will never fail (after all, how could a unicorn-powered reality-distortion magic black box ever fail) -- see also [Fallacies of Distributed Computing](http://en.wikipedia.org/wiki/Fallacies_of_Distributed_Computing). Things that are adjacent to what you do are the scary part - after all, you know enough about them to know they could fail, and you are absolutely sure people running them can never be as good as you are ;) That's why programmers worry about server failures while ignoring the quality of their code, and remain completely oblivious to network failures.

Now for more realistic arguments.

Compared to networking, storage is serious business. If you drop a user session (or phone call), nobody but the affected user cares. If the user happens to be your boss or CEO (or you drop thousands of sessions for minutes or hours), you might feel the heat, otherwise everyone accepts that just-good-enough contains some elements of shit-happens.

Storage is a totally different beast. A SCSI failure arriving at just the right time could easily result in the famous colored screen (or some other panic), bringing down an application server or an operating system, not a session. If that server happens to be your database or SAP server, someone has to start polishing the resume.

Furthermore, we (= networking engineers) don't really care if user sessions experience data corruption. After all, if we would, we wouldn't use 8-bit checksum in IP and TCP; these checksums can fail [more often than one would think](http://conferences.sigcomm.org/sigcomm/2000/conf/paper/sigcomm2000-9-1.pdf).

Storage experts developing iSCSI realized that's not good enough and added application-level checksums to iSCSI to prevent data corruption on inter-subnet iSCSI sessions - you wouldn't want to store corrupted data into a database (or anywhere else) where it can stay for years, would you?

Someone from IBM published a great article explaining the need for iSCSI checksums a while ago (and of course I can't find it; [RFC 3385](http://tools.ietf.org/html/rfc3385) does contain some hints), and in case you wonder whether routers can actually corrupt packets, the answer is YES (and [someone managed to isolate a faulty router three AS-es down the road](http://mina.naguib.ca/blog/2012/10/22/the-little-ssh-that-sometimes-couldnt.html)). I have also seen cut-through switches helping broken NICs (that didn't check the checksum) corrupt the data (admittedly that was 20 years ago, but the history has a nasty circular habit).

Of course some vendors cutting corners launched crippled boxes that require layer-2 connectivity for iSCSI replication. The only explanation I can find for that abominable restriction is lack of iSCSI-level checksums[^RT]. Ethernet checksums are orders of magnitude better than IP/TCP ones, and actually comparable to iSCSI checksums, so if you're too lazy (or your hardware is too crappy) to do the proper thing, you [stomp on the complexity sausage](/2012/07/virtualized-squashed-complexity-sausage/) and push the hard work the other way. After all, [what could possible go wrong](/2012/10/if-something-can-fail-it-will/) with [long-distance STP-assisted layer-2 connectivity](/2011/06/stretched-clusters-almost-as-good-as/) (aka "the thing we don't understand at all, but it seems to work").

[^RT]: There's also the tiny problem of not having a decent routing stack. VMware finally fixed that around vSphere 6.

{{<note info>}}It turns out those vendors believe in CRC fairy. [Stretched VLAN is not a data protection measure](/2015/11/ethernet-checksums-are-not-good-enough/), and once you start transporting Ethernet frames over VXLAN all bets are off anyway. If your iSCSI vendor doesn't support application-level checksum, your data is at risk no matter what.{{</note>}}

Last but definitely not least, when the proverbial substance hits the rotating blades, it's usually not limited to a single box, particularly in layer-2 environments favored by the just-mentioned storage vendors. A single STP loop (or any other loop-generating bug, including some past vPC bugs) can bring down the whole layer-2 domain, including both server-to-storage paths.

With all this in mind, it makes perfect sense to have two airgapped iSCSI networks in some environments. Obviously some people (or their CFOs) don't care enough about data availability to invest in them, and prefer the [cargo cult](http://en.wikipedia.org/wiki/Cargo_cult) approach of using two iSCSI VLANs to pretend they have FC-like connectivity, reminding me of some other people who don't want to invest in proper application development (and use of DNS for IP address resolution), load balancers etc. Believing in fairies and unicorns is so much easier.

Finally, a storage protocol rant wouldn't be complete without a passing mention of FCoE. Every single vendor (ahem, both of them) is so proud of the A/B separation at server-to-ToR boundary (which, BTW, [violates IEEE 802.1ax and BB-5](/2011/12/fcoe-and-lag-industry-wide-violation-of/)) that they forget to mention the A/B separation at the edge of a single network doesn't help once you have a network-wide meltdown.

{{<figure src="/2013/03/s480-Sparks.png" caption="This is what happens when I start discussing FCoE and LAG (author: Jon Hudson)">}}

### More Information

* You might love the [Fallacies of Distributed Computing](https://my.ipspace.net/bin/list?id=Net101#FALLACIES) videos
* We [discussed iSCSI infrastructure design](https://my.ipspace.net/bin/get/Design/22.03.02%20-%20Integrating%20Storage%20in%20Leaf-and-Spine%20Fabrics.mp4?doccode=Design) in [March 2022](https://my.ipspace.net/bin/list?id=Design#2022_03) Design Clinic.

### Revision History

2023-04-14
: Cleanup, added VXLAN transport considerations
