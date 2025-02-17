---
title: "OSPFv3 on Bird Needs IPv6 LLA on the Loopback Interface"
date: 2025-01-07 07:58:00+0100
tags: [ IPv6, OSPF, netlab ]
netlab_tag: quirks
ospf_tag: details
---
_Wanted to share this "too weird to believe" SNAFU I found when running integration tests with the Bird routing daemon. It's irrelevant unless you want Bird to advertise the IPv6 prefix configured on the main loopback interface (`lo`) with OSPFv3._

Late last year, I decided to run [_netlab_ integration tests](https://tests.netlab.tools/) with the Bird routing daemon. It passed most [baseline _netlab_ OSPFv3 integration tests](https://tests.netlab.tools/_html/coverage.ospf.ospfv3) but failed those that checked the loopback IPv6 prefix advertised by the tested device ([test results](https://tests.netlab.tools/_html/bird-clab-ospf-ospfv3)).
<!--more-->
A quick Google search unearthed a *[Wisdom of the Ancients](https://xkcd.com/979/)* email from [someone facing the exact same problem](https://bird.network.cz/pipermail/bird-users/2012-August/003161.html), and the [replies](https://bird.network.cz/pipermail/bird-users/2012-August/007868.html) sent me deep into the "_you must be kidding_" territory. OSPFv3 requires IPv6 LLA to communicate, and if Bird does not find an LLA on an interface, it ignores the interface even when the interface is configured as a stub interface.

The proposed "solution": add a static LLA to the loopback interface. It works, but one would have hoped not to encounter this FAD[^FAD] in the Bird release shipping with Ubuntu 24.04.

[^FAD]: Functions As Designed

So, just in case you need to get Bird running in this particular scenario, and the loopback interface remains in the "Ignored" state: `ip addr add fe80::1/64 dev lo scope link` is what you're looking for. I added that to the Bird initial configuration template, and suddenly, most OSPFv3 tests (for the functionality _netlab_ supports on Bird) passed with flying colors.
