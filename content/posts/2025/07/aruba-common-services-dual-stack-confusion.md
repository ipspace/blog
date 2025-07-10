---
title: "Dual-Stack Common-Services VRF Confuses Aruba CX"
date: 2025-07-11 08:18:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
As I was running the _netlab_ pre-release integration tests, I noticed that ArubaCX failed the [IPv6 Common Services test](https://github.com/ipspace/netlab/blob/22bf9ec15aec8bbea8d43d6550aaf0bb18e9d729/tests/integration/vrf/32-vrf-common-hosts-ipv6.yml) (it worked before). Here's the gist of what that test does:

* It creates three VRFs (**red**, **blue**, and **common**)
* It imports routes from **red** and **blue** VRF into the **common** VRF and routes from the **common** VRF into the **red** and **blue** VRF (the schoolbook example of *common services VRF*)
* Just to be on the safe side, it imports **red** routes into the **red** VRF and so on.

Here's the relevant part of the *netlab* lab topology:
<!--more-->
```
vrfs:
  red:
    import: [ red, common ]
    links: [ dut-h1 ]
  blue:
    import: [ blue, common ]
    links: [ dut-h2 ]
  common:
    import: [ red, blue, common ]
    links: [ dut-srv ]
```

This is the *netlab*-generated ArubaCX config for the **blue** VRF:

```
vrf blue
    rd 65000:2
    address-family ipv4 unicast
        route-target import 65000:2
        route-target import 65000:3
        route-target export 65000:2
    exit-address-family
    address-family ipv6 unicast
        route-target import 65000:2
        route-target import 65000:3
        route-target export 65000:2
    exit-address-family
```

And this is what you'll find in the device configuration after the configuration playbook completes:

```
vrf blue
    rd 65000:2
    address-family ipv4 unicast
        route-target export 65000:2
        route-target import 65000:2
        route-target import 65000:3
    exit-address-family
    address-family ipv6 unicast
        route-target import 65000:2
        route-target import 65000:3
    exit-address-family
```

Can you spot the difference? Hint: the IPv6 **export** route target is missing. No wonder nothing works.

OK, let's try to add the route target manually. This is what happens:

```
dut# conf t
dut(config)# vrf blue
dut(config-vrf)# address-family ipv6 unicast
dut(config-vrf-ipv6-uc)# route-target export 65000:2
Export route-target 65000:2 exists in same VRF
```

WTA*? It's OK to enter the same *import* route target for IPv4 and IPv6, but not the same *export* route target? Don't these guys ever test their software?

Anyway, one would hope that the error message would trigger an error in the **aoscx_config** Ansible module, right? Well, it doesn't. The problem was reported half a year ago, and [nothing happened](https://github.com/aruba/aoscx-ansible-collection/issues/123) (one has to love open-source issues 😎). Configuration errors are obviously not important.

Back to the inter-VRF route leaking on ArubaCX. It works for an IPv4-only VRF and for an IPv6-only VRF, but fails miserably when you try to leak routes between dual-stack VRFs.

Now for a few fun facts:

* **Is this a recent bug?** No, I reproduced it with ArubaCX release 10.13, which is over a year old.
* **Why do most VRF tests work?** VRF route targets are relevant only when you're doing inter-VRF route leaking, or when you're running MPLS/VPN[^ERT]. They don't matter in simple single-device scenarios (and it looks like [the MPLS data plane doesn't work in ArubaCX VM anyway](https://community.arubanetworks.com/discussion/anyone-running-mpls-with-the-simulator))
* **Why did ArubaCX pass the same test in the past?** Because we checked single-protocol VRFs. Recently, we discovered that our configuration template for another device failed when faced with dual-stack VRFs, so we changed several VRF tests to be dual-stacked.
* **Would this work with EVPN?** I have no idea, and I don't work for the HPE QA department, so don't expect me to run those tests[^RTY]. You might want to ask your SE a few pointed questions, though.

[^ERT]: ArubaCX configures EVPN route targets on the VRF level, not on the VRF-AF level.
 
[^RTY]: You could mix [this topology](https://github.com/ipspace/netlab/blob/dev/tests/integration/evpn/30-cs-bridging.yml) with [this one](https://github.com/ipspace/netlab/blob/dev/tests/integration/evpn/22-ospf-ce-router.yml) to test that. Just don't forget to add IPv6 to the mix.
