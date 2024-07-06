---
title: "Automated Validation of BGP Labs"
series_title: "Automated Lab Validation"
date: 2024-06-18 08:22:00+02:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
---
In late 2023, I started playing with the idea of having automated validation in _netlab_. The early implementation was used in BGP labs, and a user liked it so much that he opened an issue saying:

> I would suggest providing **netlab validate** for each lab.

Numerous rounds of yak-shaving later, I merged a humongous commit that adds automated validation to these lab exercises:
<!--more-->
* [Redistribute IGP Information Into BGP](https://bgplabs.net/basic/5-redistribute/)
* [Select Preferred EBGP Peer with Weights](https://bgplabs.net/policy/1-weights/)
* [Filter Transit Routes](https://bgplabs.net/policy/2-stop-transit/)
* [Filter Advertised Prefixes](https://bgplabs.net/policy/3-prefix/)
* [Minimize the Size of Your BGP Table](https://bgplabs.net/policy/4-reduce/)
* [Select Preferred Uplink with BGP Local Preference](https://bgplabs.net/policy/5-local-preference/)
* [Use MED to Influence Incoming Traffic Flow](https://bgplabs.net/policy/6-med/)
* [Use AS-Path Prepending to Influence Incoming Traffic Flow](https://bgplabs.net/policy/7-prepend/)
* [Attach BGP Communities to Outgoing BGP Updates](https://bgplabs.net/policy/8-community-attach/)
* [Use BGP Communities in Routing Policies](https://bgplabs.net/policy/9-community-use/)
* [BGP Route Server in an Internet Exchange Point](https://bgplabs.net/session/5-routeserver/)
* [Dynamic BGP Peers](https://bgplabs.net/session/9-dynamic/)

The automated validation can be used on Arista EOS, Cumulus Linux, and FRR[^OP] and requires validation plugins included in [_netlab_ release 1.8.3](/2024/06/netlab-1-8-3-rip-bgp.html).

Some other lab exercises already supported automated validation:

* [Configure a Single EBGP Session](https://bgplabs.net/basic/1-session/)
* [Configure Multiple EBGP Sessions](https://bgplabs.net/basic/2-multihomed/)
* [Advertise IPv4 Prefixes to BGP Neighbors](https://bgplabs.net/basic/3-originate/)
* [Configure BGP for IPv6](https://bgplabs.net/basic/4-ipv6/)
* [Advertise Default Route in BGP](https://bgplabs.net/basic/c-default-route/)
* [EBGP Sessions over IPv6 LLA Interfaces](https://bgplabs.net/basic/d-interface/)
* [Reuse a BGP AS Number Across Multiple Sites](https://bgplabs.net/session/1-allowas_in/)
* [Fix AS-Path in Environments Reusing BGP AS Numbers](https://bgplabs.net/session/2-asoverride/)
* [Use Multiple AS Numbers on the Same Router](https://bgplabs.net/session/3-localas/)
* [BGP Session Templates](https://bgplabs.net/session/6-templates/)

[^OP]: Want to run validation on other platforms? Please implement the BGP and OSPF validation plugins (they have to pass all the [validation plugin integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration/validate)) and submit a PR. Being a realist, I'm not holding my breath ;)

{{<jump>}}[Explore the BGP labs](https://bgplabs.net/){{</jump>}}
