---
title: "ArubaCX Decides When You're Done Changing a BGP Routing Policy"
date: 2025-08-05 08:16:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
When I was cleaning the "[set BGP MED](https://github.com/ipspace/netlab/blob/5aae878dff0da1ffb256a33532e0748d9ba7df56/tests/integration/bgp.policy/31-med.yml)" integration test, I decided that once a BGP prefix is in the BGP table of the BGP peer, there's no need for a further wait before checking its MED value. After all:

* We configure an outbound routing policy to change MED;
* We execute **do clear bgp \* soft out** at the end of most BGP policy configuration templates[^SRP]
* The device under test should thus immediately (re)send the expected BGP prefix with the target MED.

That approach failed miserably with ArubaCX; it was time to investigate the details.
<!--more-->
[^SRP]: Only a few platforms are smart enough to discover the outbound BGP policy has changed on their own

I started the lab, turned on BGP update debugging on the FRRouting device adjacent to the ArubaCX VM, and let _netlab_ configure the devices. This is what it pushed to ArubaCX:

```
route-map bp-probe-1-out-ipv4 permit seq 10
  set metric 42
!
route-map bp-probe-1-out-ipv6 permit seq 10
  set metric 42
!
router bgp 65000
!
! Work on weight first, which is out of the address family
!
 address-family ipv4 unicast
    neighbor 10.1.0.2 route-map bp-probe-1-out-ipv4 out
 address-family ipv6 unicast
    neighbor 2001:db8:3::2 route-map bp-probe-1-out-ipv6 out
!
do clear bgp all * soft out
do clear bgp all * soft in
```

And this is what the FRRouting BGP daemon observed. First, the BGP session with ArubaCX was established (that was at approximately the same time as _netlab_ configured the BGP policy on ArubaCX):

```
2025-07-10 12:50:48.068 [INFO] bgpd: [VTVCM-Y2NW3] Configuration Read in Took: 00:00:00
2025-07-10 12:50:48.068 [DEBG] bgpd: [G6NKK-8C6DV] end_config: VTY:0x7f767f397080, pending SET-CFG: 0
2025-07-10 12:50:49.071 [WARN] bgpd: [JG0WZ-7X009][EC 33554504] 2001:db8:3::1 unrecognized capability code: 128 - ignored
2025-07-10 12:50:49.071 [WARN] bgpd: [JG0WZ-7X009][EC 33554504] 10.1.0.1 unrecognized capability code: 128 - ignored
2025-07-10 12:50:49.071 [INFO] bgpd: [N9HHH-F8H1M] %ADJCHANGE: neighbor 2001:db8:3::1(Unknown) in vrf default Up
2025-07-10 12:50:49.072 [INFO] bgpd: [N9HHH-F8H1M] %ADJCHANGE: neighbor 10.1.0.1(Unknown) in vrf default Up
```

ArubaCX sent its IPv4 and IPv6 BGP prefixes with no MED, followed by end-of-RIB messages:

```
2025-07-10 12:50:49.115 [DEBG] bgpd: [T5AAP-5GA85] 2001:db8:3::1(Unknown) rcvd UPDATE w/ attr: , origin i, mp_nexthop 2001:db8:3::1(fe80::800:901:493:11f9), path 65000
2025-07-10 12:50:49.115 [DEBG] bgpd: [PCFFM-WMARW] 2001:db8:3::1(Unknown) rcvd UPDATE wlen 0 attrlen 71 alen 0
2025-07-10 12:50:49.115 [DEBG] bgpd: [YCKEM-GB33T] 2001:db8:3::1(Unknown) rcvd 2001:db8:42:1::1/128 IPv6 unicast
2025-07-10 12:50:49.115 [DEBG] bgpd: [PCFFM-WMARW] 2001:db8:3::1(Unknown) rcvd UPDATE wlen 0 attrlen 7 alen 0
2025-07-10 12:50:49.115 [INFO] bgpd: [M59KS-A3ZXZ] bgp_update_receive: rcvd End-of-RIB for IPv6 Unicast from 2001:db8:3::1 in vrf default
2025-07-10 12:50:49.115 [DEBG] bgpd: [T5AAP-5GA85] 10.1.0.1(Unknown) rcvd UPDATE w/ attr: nexthop 10.1.0.1, origin i, path 65000
2025-07-10 12:50:49.115 [DEBG] bgpd: [PCFFM-WMARW] 10.1.0.1(Unknown) rcvd UPDATE wlen 0 attrlen 20 alen 5
2025-07-10 12:50:49.115 [DEBG] bgpd: [YCKEM-GB33T] 10.1.0.1(Unknown) rcvd 10.0.0.42/32 IPv4 unicast
2025-07-10 12:50:49.115 [DEBG] bgpd: [PCFFM-WMARW] 10.1.0.1(Unknown) rcvd UPDATE wlen 0 attrlen 0 alen 0
2025-07-10 12:50:49.115 [INFO] bgpd: [M59KS-A3ZXZ] bgp_update_receive: rcvd End-of-RIB for IPv4 Unicast from 10.1.0.1 in vrf default
```

Twelve seconds later, ArubaCX woke up, realized it had a route map configured on a BGP neighbor, and resent the updates, this time with MED:

```
2025-07-10 12:51:02.028 [DEBG] bgpd: [T5AAP-5GA85] 2001:db8:3::1(Unknown) rcvd UPDATE w/ attr: , origin i, mp_nexthop 2001:db8:3::1(fe80::800:901:493:11f9), metric 42, path 65000
2025-07-10 12:51:02.028 [DEBG] bgpd: [PCFFM-WMARW] 2001:db8:3::1(Unknown) rcvd UPDATE wlen 0 attrlen 78 alen 0
2025-07-10 12:51:02.028 [DEBG] bgpd: [YCKEM-GB33T] 2001:db8:3::1(Unknown) rcvd 2001:db8:42:1::1/128 IPv6 unicast
2025-07-10 12:51:03.028 [DEBG] bgpd: [T5AAP-5GA85] 10.1.0.1(Unknown) rcvd UPDATE w/ attr: nexthop 10.1.0.1, origin i, metric 42, path 65000
2025-07-10 12:51:03.028 [DEBG] bgpd: [PCFFM-WMARW] 10.1.0.1(Unknown) rcvd UPDATE wlen 0 attrlen 27 alen 5
2025-07-10 12:51:03.028 [DEBG] bgpd: [YCKEM-GB33T] 10.1.0.1(Unknown) rcvd 10.0.0.42/32 IPv4 unicast
```

The updates were **not** triggered by the **do clear bgp all \* soft out** command (regular readers [already know why](/2025/07/aruba-bgp-soft-reconfiguration/)). They happen so late that the validation test  (run immediately after the device configuration had completed) kept failing until I extended the wait time to 15 seconds (ten would probably do; I wanted to be on the safe side). Also, we set the **neighbor advertisement-interval** to one second, so the behavior should not be caused by delayed updates, and I found no other timers to tweak.

To recap:

* Some platforms (Junos, SR-OS, Arista EOS, IOS-XR) allow you to edit a candidate device configuration and *commit* the changes once you're done. It's easy for these platforms to resend BGP updates when they figure out that the routing policies have changed in the candidate configuration.
* Platforms that immediately apply changes to the running configuration usually don't dare to resend BGP updates after every tiny little change to the routing policy. That would be a nightmare; imagine generating BGP updates all the time you're fixing a prefix list by hand[^SBA].

ArubaCX developers evidently decided to take a more "creative" approach: they obviously detect changes to routing policies and automatically resend the updates a while later. That wouldn't be such a bad idea if:

* I could turn off that feature when I know I'm making plenty of changes.
* I could tweak the wait timer.
* I could send the modified BGP updates manually with the **clear bgp soft out** command.

Sadly, I found no way to control that "feature," and the [outbound soft reconfiguration is a no-op](/2025/07/aruba-bgp-soft-reconfiguration/). The only thing missing is an overzealous product manager claiming they implemented AI-driven BGP policy changes.

[^SBA]: Yeah, I know that should be automated, but like COBOL, manual changes will not go away any time soon.