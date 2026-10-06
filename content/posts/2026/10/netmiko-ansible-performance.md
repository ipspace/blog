---
title: "Netmiko vs Ansible: Does It Matter?"
date: 2026-10-08 08:10:00+0200
tags: [ netlab ]
netlab_tag: details
---
We launched [device configuration with Netmiko](https://netlab.tools/platforms/#platform-config-mode) in the [September 2026 netlab release](https://netlab.tools/release/26.09/) and made it [easier to use](https://netlab.tools/netlab/install/#installation-scripts) in the [October 2026 release](https://netlab.tools/release/26.10/). It will become the default configuration method for several popular platforms (Arista EOS, Cisco IOS, Cisco Nexus OS, Cisco IOS XR, FRRouting virtual machines) in a few months, but before doing that, I wanted to check whether the change matters.

**TL&DR:** Yes, it does.
<!--more-->
I did a very unscientific test:

* I started an EVPN lab because there's plenty to configure there ([configuration normalization](https://blog.ipspace.net/2025/03/stupid-bridges-strike-again/), initial configuration, VLANs, OSPF, BGP, VRFs, VXLAN, EVPN)
* I measured how long it takes to *start* the lab (Arista EOS and Linux containers) and how long it takes to *configure* it.
* The *configure the lab* part on Arista EOS was done with **bash** scripts, Netmiko and Ansible. netlab always configures Linux containers with **bash** scripts.

Here are the results:

| Operation | netlab CPU time[^NCP] | Elapsed time |
|-----------|----------------:|-------------:|
| Starting the lab | 1.6 s | 23.5 s |
| Configuration with **bash** scripts | 0.7 s | 4.3 s |
| Configuration with Netmiko | 0.9 s | 6.2 s |
| Configuration with Ansible | 9.8 s | 33.1 s |
{.fmtTable}

[^NCP]: Includes the CPU time spent in child processes, for example, **ansible-playbook**.

The difference between Netmiko and Ansible configuration time is significant, and while it doesn't matter much if you're using VMs (which [start much slower than containers](/2023/02/virtual-device-boot-times/)), just watching the Ansible playbook generating noise while slowly progressing through the configuration steps makes me cringe. 

Speaking of noise: here's the complete printout from a Netmiko-based configuration of a lab topology with two switches and four hosts; you really don't want to see the corresponding Ansible printout[^SCB].

[^SCB]: Yeah, I know Ansible has stdout callbacks, and some of them are pretty terse. However, I haven't found one that would produce the concise information *netlab* generates when used with Netmiko, and I definitely won't waste time writing my own.

{{<ascii>}}
┌──────────────────────────────────────────────────────────────────────────────────┐
│ CHECKING Are lab devices ready to be configured?                                 │
└──────────────────────────────────────────────────────────────────────────────────┘
[INFO]    Checking SSH server(s) on dut_s1,dut_s2
[SSH] Waiting for 1 devices (1.0 seconds)
┌──────────────────────────────────────────────────────────────────────────────────┐
│ CONFIG Normalizing device configurations                                         │
└──────────────────────────────────────────────────────────────────────────────────┘
[INFO]    Executing normalize configuration for node dut_s1
[INFO]    Executing normalize configuration for node dut_s2

┌──────────────────────────────────────────────────────────────────────────────────┐
│ CONFIG Deploying device configurations                                           │
└──────────────────────────────────────────────────────────────────────────────────┘
[INFO]    Executing initial configuration for node dut_s1
[INFO]    Executing initial configuration for node dut_s2
[INFO]    Executing initial configuration for node h1 (namespace clab-evpn-h1)
[INFO]    Executing initial configuration for node h2 (namespace clab-evpn-h2)
[INFO]    Executing initial configuration for node h3 (namespace clab-evpn-h3)
[INFO]    Executing initial configuration for node h4 (namespace clab-evpn-h4)
[INFO]    Executing routing configuration for node h1 (namespace clab-evpn-h1)
[INFO]    Executing routing configuration for node h3 (namespace clab-evpn-h3)
[INFO]    Executing routing configuration for node h4 (namespace clab-evpn-h4)
[INFO]    Executing routing configuration for node h2 (namespace clab-evpn-h2)
[INFO]    Executing vlan configuration for node dut_s1
[INFO]    Executing vlan configuration for node dut_s2
[INFO]    Executing ospf configuration for node dut_s1
[INFO]    Executing ospf configuration for node dut_s2
[INFO]    Executing bgp configuration for node dut_s1
[INFO]    Executing bgp configuration for node dut_s2
[INFO]    Executing vrf configuration for node dut_s2
[INFO]    Executing vrf configuration for node dut_s1
[INFO]    Executing vxlan configuration for node dut_s2
[INFO]    Executing vxlan configuration for node dut_s1
[INFO]    Executing evpn configuration for node dut_s2
[INFO]    Executing evpn configuration for node dut_s1

Results of non-Ansible configuration deployments
====================================================================================================================================
dut_s1           Script:   normalize,initial,vlan,ospf,bgp,vrf,vxlan,evpn
dut_s2           Script:   normalize,initial,vlan,ospf,bgp,vrf,vxlan,evpn
h1               Script:   initial,routing
h2               Script:   initial,routing
h3               Script:   initial,routing
h4               Script:   initial,routing


[SUCCESS] Lab devices configured
{{</ascii>}}

Finally, I prefer SSH-based configuration over hacks like the [FastCLI scripts](https://blog.ipspace.net/2026/02/netlab-eos-configuration/) that netlab can use with Arista EOS containers. The performance difference isn't huge, and we can use the same method with virtual machines and containers.

{{<next-in-series page="2026/10/netmiko-ansible-script-performance/" />}}