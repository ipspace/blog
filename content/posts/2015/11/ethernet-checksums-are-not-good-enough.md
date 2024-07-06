---
date: 2015-11-25 14:37:00+01:00
tags:
- data center
- SAN
title: Ethernet Checksums Are Not Good Enough for Storage 
url: /2015/11/ethernet-checksums-are-not-good-enough.html
---
A while ago I described why [some storage vendors require end-to-end layer-2 connectivity for iSCSI replication](/2013/03/does-dedicated-iscsi-infrastructure.html).

**TL&DR version**: among other things, they might have been too lazy to implement iSCSI checksums and rely on Ethernet checksums because TCP/IP checksums are not good enough.

It turns out even Ethernet checksums fail every now and then.
<!--more-->
TCP and IP checksums are simple [ones' complement sums](https://en.wikipedia.org/wiki/IPv4_header_checksum), and we know [they're weak](http://www.evanjones.ca/tcp-checksums.html). As Evan Jones [explained in his blog](http://www.evanjones.ca/tcp-and-ethernet-checksums-fail.html), you might expect that one in ~65000 corrupt packets won't be detected, which combined with pretty low error rates we see on Ethernet these days might be good enough... or not, if you're Twitter and dealing with petabytes of traffic.

Ethernet CRC is supposed to save the day. After all, a switch receiving a packet checks the CRC regardless of whether the packet is subsequently bridged or routed. Ethernet CRC should reliably detect transmission errors, and the TCP/IP checksums should detect extremely rare intra-device data corruption errors... or so the theory goes.

In practice:

* Store-and-forward switches drop packet with invalid CRC. Harm avoided.
* Cut-through switches (becoming yet again ever more popular due to reduced latency) [stomp the CRC](/2020/12/chasing-crc-errors-data-center-fabric.html) if the incoming CRC is invalid (see also [the excellent blog post by John Harrington](http://thenetworksherpa.com/cut-through-corruption-and-crc-stomping/))
* However, **layer-3 switches recalculate the CRC**[^RC], which thus no longer protects the integrity of Ethernet frame between end hosts.

[^RC]: They have to as they decrement TTL and change MAC address.

**Evan's conclusion**: if you care about data integrity, implement application-level checksum, preferably using CRC32C, which is implemented in hardware on recent CPUs.

**Also note**: Stretched VLAN is not a data protection feature for your iSCSI network, in particular if you use Ethernet-over-IP transport like VXLAN or OTV. If the iSCSI or NFS solution you're using doesn't support application-level checksums, your data is at risk no matter what.

Finally, how many application-level protocols apart from SSL/TLS and iSCSI (when implemented) implement an application-level checksum? Please write a comment!

### Revision History

2023-04-14
: Rewrote the "what really happens" bit, and added mention of Ethernet-over-IP transport

2015-12-06
: I misunderstood the main technical argument in Evan's post. The real problem is that switches recalculate CRC, so the Ethernet CRC is no longer end-to-end protection mechanism.

2015-11-15
: TCP/IP checksums are not XORs (thanks to [Andrew Yourtchenko](https://twitter.com/ayourtch/status/669535569207234560)).


