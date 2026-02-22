---
title: "Configuring 6PE Route Reflector on Cisco IOS"
subtitle: Or How Ansible Did It Again
date: 2026-02-26 08:19:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
Imagine you want to deploy a BGP route reflector for MPLS 6PE or L3VPN service. Both services run over MPLS LSPs, use IPv4 BGP sessions, and use IPv4 next hops for BGP routes. There's absolutely no reason to need IPv6 routing on a node that handles solely the control-plane activity (it never appears as a BGP next hop anywhere), right? Cisco IOS disagrees, as I discovered when running [route reflector integration tests](https://tests.netlab.tools/_html/coverage.mpls) for _netlab_ [6PE and (MPLS) L3VPN functionality](https://netlab.tools/module/mpls/).

Most platforms failed those tests because we forgot to configure **route-reflector-clients** in labeled IPv6 and VPNv4/VPNv6 address families[^EOSRR]. That was easy to fix, but the IOS-based devices were still failing the tests, with nothing in the toolchain ever complaining about configuration problems.

[^EOSRR]: Arista EOS was one of the few exceptions because it configures BGP route reflector clients in the (academically speaking) [suboptimal layer](/2022/10/arista-route-reflector-woes/) in the BGP configuration hierarchy.

Looking more closely at what was going on, I discovered something weird: BGP **ipv6 labeled-unicast** and **vpnv6** address families appeared to be configured without a hitch with Ansible's **ios_config** module, but they did not subsequently appear in the BGP configuration.

Logging into the route reflector and copy-pasting the commands quickly identified the culprit:

```
dut(config)#router bgp 65001
dut(config-router)#address-family ipv6
% IPv6 routing not enabled
dut(config-router)#address-family vpnv6 unicast
% IPv6 routing not enabled
```

Adding **ipv6 unicast-routing** to a BGP route reflector that did not have a single IPv6 address configured or IPv6 enabled on a single interface fixed the problem.

After adding that command, the integration tests were passing without a hitch, but I was still wondering why Ansible reported no configuration errors. Fortunately, Ansible collections are available on GitHub, and I've been down this road before, so it wasn't hard to find what the Ansible **ios_config** module [considers to be a configuration error](https://github.com/ansible-collections/cisco.ios/blob/fd0c28fe22658f79ca73bb1371692b6b7c015f8c/plugins/terminal/ios.py#L36). Instead of "every response to a configuration command that starts with a percent sign is an error", they have a nice collection of whatever error messages they've seen in the past. Any error message they haven't seen before is quietly ignored[^OAI].

[^OAI]: And before you ask: yes, I [opened an issue](https://github.com/ansible-collections/cisco.ios/issues/1301).

And that's why it would be much better to use a configuration mechanism like NETCONF or REST API that consistently reports the completion status, rather than the CLI to configure network devices. If only they would be as easy to use as the CLI 🤷‍♂️.
