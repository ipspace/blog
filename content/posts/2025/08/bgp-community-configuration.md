---
title: "Configuring BGP Community Propagation is Confusing"
date: 2025-08-21 08:02:00+0200
tags: [ BGP ]
---
A large number of vendors claim to use *industry-standard CLI*, which means "*something that looks like Cisco IOS, but we can't say that in public*." The implementations of that "standard" are full of quirks; as I was [making fun of Cisco IOS last week](/2025/08/cisco-ios-community-propagation/), it's only fair to look at how others deal with BGP community propagation.

_netlab_ has BGP configuration templates for [14 different platforms](https://netlab.tools/module/bgp/#platform-support)[^MD], including these implementations that look like Cisco IOS from a distance if you squint just right[^SH]: Arista EOS, Aruba CX, and FRRouting. You can check the [configuration templates](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/templates/bgp) if you wish; here's the TC&DB[^TCDB] overview:
<!--more-->
[^MD]: Where a single *platform* could cover multiple devices. The Cisco IOS template is used on Cisco IOSv, IOSvL2, Cisco CSR 1000v, Cisco Catalyst 8000v, Cisco IOS-on-Linux (IOL), and IOL Layer-2, and the Junos template is used on vMX, vSRX, vPTX, vJunos-evolved, vJunos-switch, and vJunos-router.

[^SH]: And happen to be short-sighted 😜

[^TCDB]: Too cumbersome, didn't bother

* Arista EOS has a **neighbor send-community** command with numerous arguments. You can control the propagation of standard, extended, or large communities *in a single command*. Using the same command twice overrides the previous settings. For some extra fun, the keywords must be specified in an exact order -- *standard* before *extended* before *large*. However, Arista EOS gets bonus points for **add** and **remove** keywords, making writing a configuration template a breeze[^RA].

```
dut(config-router-bgp-af)#neighbor 10.1.0.6 send-community ?
  add             Add community attributes to send to this neighbor
  extended        Send extended community attribute to this neighbor
  large           Send large community attribute to this neighbor
  link-bandwidth  Send link-bandwidth community attribute to this neighbor
  remove          Remove community attributes to send to this neighbor
  standard        Send standard community attribute to this neighbor
  <cr>

dut(config-router-bgp-af)#neighbor 10.1.0.6 send-community large ?
  <cr>

dut(config-router-bgp-af)#neighbor 10.1.0.6 send-community standard ?
  extended  Send extended community attribute to this neighbor
  large     Send large community attribute to this neighbor
  <cr>
```

[^RA]: It looks like they added the **add** and **remove** keywords after I created the configuration template a few years ago. In those days, I was still struggling with the order of keywords.

* ArubaCX behaves like the hard-core Cisco IOS: the **neighbor send-community** command takes one argument (**standard**, **extended**, or **both**), and the last value you specify is used.
* Cisco IOS allowed you to specify individual keywords using multiple commands. If you specified **standard** and **extended** in multiple commands, they were merged into **both**. The hardcore 90s behavior returned with the release 17.16.01; now, the latest value is used. There is still no way to control the propagation of *large* communities[^NTS].
* FRRouting **neighbor send-community** command treats **standard**, **large**, and **extended** as binary values. You can set or remove one of them per configuration command. The **neighbor send-community** command also accepts the **both** keyword (for hard-core Cisco fans) and the **all** keyword (meaning *standard*, *large*, and *extended*). For extra fun, propagation of all communities is enabled as part of the **datacenter** defaults; you have to remove the communities you don't want to propagate with the **no neighbor send-community _something_**.

[^NTS]: I never tested whether they treat *large* communities as a variant of *standard* ones or just pass them because they're transitive optional BGP attributes.

*netlab* also supports two platforms that configure BGP options within the **neighbor** hierarchy (not exactly the *industry standard*, but close).

* Dell OS10 **send-community** command treats **standard** and **extended** as binary values that can be set and removed independently.
* Cisco Nexus OS **send-community** command also treats **standard** and **extended** as binary values -- you can set or remove either one of them independently. However (because where's fun in being consistent and straightforward), the **standard** keyword is accepted but does not appear in the configuration (all you see is **send-community**, and you have to know it means "standard"). There's also the **both** keyword that is *expanded* into *nothing* (OK, *standard*) and **extended** -- you add **send-community both** configuration command, and get two **send-community** commands in the device configuration for the price of one. What a great deal ;)

**Long story short:** We know Cisco Parser Police[^RT] was disbanded a long time ago, and it looks like a similar concept never appealed to most other vendors.

[^RT]: Yes, that's a real thing. ChatGPT did an excellent job finding several references, including a [mention in a mailing list](https://lists.bufferbloat.net/starlink/CAHb6LvoN2bJdgcOAW-NmxzHpFVNE91Hhfgwc2_iWNbF%3DNoYjpg%40mail.gmail.com/), [court filings](https://www.casemine.com/judgement/us/59145ac5add7b049341d92a5?utm_source=chatgpt.com) in the Cisco vs. Arista case, and a [mention in a Cisco Live presentation](https://blog.ipspace.net/2025/01/cisco-vrrp3-ipv6-configuration/#2513).

Oh, and then there's Junos, and it Has to Be Different&trade;. You cannot configure community propagation; if you don't want to propagate them, you have to remove them with a routing policy.
