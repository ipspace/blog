---
date: 2023-05-15 07:56:00+00:00
netlab_tag: release
series_title: libvirt Public Networks, containerlab 0.41.0 (Release 1.5.3)
tags:
- netlab
title: 'netlab Release 1.5.3: libvirt Public Networks'
---
*containerlab* [release 0.41.0](https://containerlab.dev/rn/0.41/) that came out a few days ago changed a few topology attributes with no backward compatibility, breaking *netlab* for anyone doing a new installation. The only way out of that conundrum was to push out a new *netlab* release that uses the new attributes and requires *containerlab* release 0.41.0 (more about that in a minute).

On a more positive note, _netlab_ [release 1.5.3](https://netlab.tools/release/1.5/#release-1-5-3) brings a few interesting features, including:

- Support for [public *libvirt* networks](https://netlab.tools/labs/libvirt/#libvirt-network-external) that can be used to [connect your labs to the outside world](https://netlab.tools/example/external/), and [reuse of existing libvirt networks](https://netlab.tools/labs/libvirt/#libvirt-network)
- [‘unknown’ device type](https://netlab.tools/platforms/#platform-unknown) that can be used to deploy devices not yet supported by *netlab*
- MPLS/VPN support on Nokia SR-OS
<!--more-->
I will cover the public *libvirt* networks in another blog post, today I want to explain how we're dealing with *containerlab* changes.

**Root cause:** *containerlab* release 0.41.0 [changed the name of management network attributes](https://containerlab.dev/rn/0.41/) from `mgmt_ipv4`/`ipv4_subnet` to `mgmt-ipv4`/`ipv4-subnet` with no backward compatibility or deprecation period. Old topologies no longer work, and new topologies don't work with older versions of *containerlab*.

**Mitigation:** The only safe way to deal with this change was to change the *netlab* containerlab topology template and enforce minimum *containerlab* version during **netlab up** virtualization provider tests. The **netlab install** installation scripts could use an older *containerlab* version, but that wouldn't help users installing *containerlab* manually (without reading the smallprint). It would also break *netlab* the moment someone would upgrade *containerlab*.

**Positive side effects:** **netlab up** and **netlab down** already executed a number of commands to check the virtualization provider installation. I modified those probes to return a hopefully-useful error message when the executed command fails. 

*containerlab* probes check the availability of `containerlab` command and *containerlab* version (using a **bash** command that [looks like line noise](https://github.com/ipspace/netlab/commit/beaa08d05ffb8d11870d9243f8de58f4c87ff04d#diff-ea1001a35add0b198fca60e861c6e67d54d7253c8015a5cb366ffa64956594eaR15)). *libvirt* probes are more extensive and check that:

* You installed KVM and KVM utilities like **kvm-ok**
* KVM works (for example, you haven't forgotten to turn on nested virtualization)
* You installed *libvirt* and made yourself a member of *libvirt* group
* You installed Vagrant and *vagrant-libvirt* plugin.

### Upgrading

To get more details and learn about additional features included in release 1.5.3, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-3). To upgrade, execute `pip3 install --upgrade networklab`. You will also have to upgrade *containerlab* with `sudo containerlab version upgrade`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a discussion or an issue in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.
