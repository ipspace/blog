---
title: "Sunsetting netlab Vagrant/libvirt provider"
date: 2026-09-17 07:51:00+0200
tags: [ netlab ]
netlab_tag: release
---
When I [started the _netlab_ project](/2020/12/build-labs-netsim-tools/), Vagrant was the go-to tool if you wanted to build a virtual environment described in a text configuration file (an idea popularized as *[infrastructure-as-code](https://blog.ipspace.net/series/niac/)*). It wasn't ideal for what we were doing, but a tool rarely does a great job when used far away from its intended use case.

*netlab* initially supported Vagrant with VirtualBox, quickly adding support for KVM/libvirt through the *[vagrant-libvirt](https://vagrant-libvirt.github.io/vagrant-libvirt/)* plugin. Life was good... until it wasn't.
<!--more-->
In 2023, HashiCorp [changed its Vagrant license](https://www.hashicorp.com/en/blog/hashicorp-adopts-business-source-license). I don't know whether that impacted the development of the *[vagrant-libvirt](https://github.com/vagrant-libvirt/vagrant-libvirt)* plugin, but the last release was published in June 2023, and the last PR was merged in December of the same year. Some of the bug fixes thus never made it into a release, and the project currently has over 30 open pull requests; the plugin looks like another sad case of abandonware.

The Vagrant license change obviously left a bad taste. For example, with release 24.04, Canonical [stopped publishing Ubuntu boxes](https://discourse.ubuntu.com/t/ubuntu-24-04-lts-noble-numbat-release-notes/39890) (we used Ubuntu as the base box for FRR). Still, there were third-party boxes one could use.

The other shoe dropped in July 2026: HashiCorp decided to [kill Vagrant Cloud](https://developer.hashicorp.com/hcp/docs/vagrant/hcp-vagrant-eol) (the public image repository) by the end of 2026. It was time to part ways; _netlab_ is sunsetting the **libvirt** provider and will rely primarily on *containerlab* for workload orchestration.

Don't panic if you're relying on the _netlab_ **libvirt** provider (and invested time in building a large collection of Vagrant boxes). It's not going anywhere, and we're not removing anything from the codebase (just yet). We'll fix any bugs that come up, but we won't add new **libvirt** features or run device integration tests with it. For the moment, **libvirt** tests will also remain part of the [platform integration tests](https://release.netlab.tools/#platform) to catch any breaking changes. I'll probably do a code cleanup a year or two from now, after checking that all the supported platforms work well with *vrnetlab*.

In the meantime, I'd encourage you to build *[vrnetlab](https://netlab.tools/labs/clab/#clab-vrnetlab)* containers for the devices you're using (it's usually a pretty straightforward process) and [report any potential problems](https://github.com/srl-labs/vrnetlab/issues/new) to the *vrnetlab* team; they are usually very responsive.