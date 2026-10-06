---
title: "Configuring SRv6 on Junos (Locator and IGP)"
date: 2026-09-30 08:14:00+0200
tags: [ SRv6 ]
srv6_tag: config
---
I wanted to make my [SRv6 lab examples](https://github.com/ipspace/srv6-examples) usable with more platforms. Adding _netlab_ Junos SRv6 support (included in the 26.10 release) was relatively easy; here's what I learned while working on the [pull request](https://github.com/ipspace/netlab/pull/3889):
<!--more-->
* I decided to use micro-SIDs and used the excellent SRv6 Micro-SID (uSID) Basics article[^CJN] by [Krzysztof Szarkowicz](https://www.ipspace.net/Author:Krzysztof_Grzegorz_Szarkowicz) (of the [EVPN-with-MPLS](https://my.ipspace.net/bin/list?id=EVPN#SP) fame) as the starting point.
* Krzysztof recommended using SRv6 **block** configuration. I was too lazy to calculate it from the SRv6 locator (which was already part of the data structure), so I used only the **locator** configuration. Everything worked fine without SRv6 **block** anyway (but maybe I'm missing something important).

[^CJN]: The article was published on community.juniper.net, and a few days after this blog post was published, someone in HPE marketing managed to bork that website; the last time I checked, the original link either ended on a generic HPE webpage or returned a DNS server error. I don't care whether it's a temporary glitch or not (it's not the first time someone has had a DNS problem with that domain); if HPE doesn't like inbound traffic, we can fix that.

{{<printout caption="SRv6 uSID locator configuration on Junos">}}
routing-options {
  source-packet-routing {
    srv6 {
      locator dut {
        5f00:0:1::/48;
        micro-sid;
      }
    }
  }
}
{{</printout>}}

* Adding the SRv6 SID to IS-IS was trivial. All I had to do was tell the IS-IS protocol to get a node uSID from the already-configured locator:

{{<printout caption="SRv6 IS-IS configuration on Junos">}}
protocols {
  isis {
    source-packet-routing {
      srv6 {
        locator dut micro-node-sid;
      }
    }
  }
}
{{</printout>}}

Have I missed anything? Would you have done it differently? Please write a comment.

### Why Do We Need SRv6 Locator in IS-IS?

Even if you plan to use SRv6 solely for layer-3/VPN services, you have to add the SRv6 locator to the IS-IS configuration to get the SRv6 TLVs and the locator prefix into the IS-IS LSP. The locator prefix is inserted into the IPv6 routing tables on other IS-IS routers and enables forwarding of SRv6-encapsulated packets.

{{<printout caption="SRv6 IS-IS LSP advertised by a Junos router configured with SRv6" highlight="yes">}}
pe2# show isis database detail dut.00-00
Area Gandalf:
IS-IS Level-2 link-state database:
LSP ID                  PduLen  SeqNumber   Chksum  Holdtime  ATT/P/OL
dut.00-00                 328   0x00000004  0x9652    1191    0/0/0
  Protocols Supported: IPv4, IPv6
  Area Address: 49.0001
  MT Router Info: ipv4-unicast
  MT Router Info: ipv6-unicast
  Hostname: dut
  TE Router ID: 10.0.0.1
  IPv6 TE Router ID: 2001:db8:0:1::1
  Router Capability: 10.0.0.1 , D:0, S:0
    SR Algorithm:
      0: SPF
      1: Strict SPF
    SRv6: O:0
  MT Reachability: 0000.0000.0007.00 (Metric: 10) ipv6-unicast
    Link Local  ID: 345
    Link Remote ID: 1
    Local Interface IPv6 Address(es): 2001:1::1
    Remote Interface IPv6 Address(es): 2001:1::2
  IPv4 Interface Address: 10.0.0.1
  IPv6 Interface Address: 2001:db8:0:1::1
  <b>MT IPv6 Reachability: 5f00:0:1::/48 (Metric: 0) ipv6-unicast</b>
  MT IPv6 Reachability: 2001:1::/64 (Metric: 10) ipv6-unicast
  MT IPv6 Reachability: 2001:db8:0:1::1/128 (Metric: 0) ipv6-unicast
  MT IPv6 Reachability: 2001:db8:0:1::/64 (Metric: 0) ipv6-unicast
  <b>SRv6 Locator: 5f00:0:1::/48 (Metric: 0) ipv6-unicast</b>
    Sub-TLVs:
      SRv6 End SID Endpoint Behavior: uN PSP/USD, SID value: 5f00:0:1::
        Sub-Sub-TLVs:
          SRv6 SID Structure Locator Block length: 32, Locator Node length: 16, Function length: 0, Argument length: 80,
{{</printout>}}



