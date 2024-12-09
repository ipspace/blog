---
title: "Netlab Is Four Years Old"
date: 2024-12-09 09:19:00+0100
tags: [ netlab ]
netlab_tag: overview
---
On December 9th, 2020, I created a new GitHub repository and pushed the [first commit](https://github.com/ipspace/netlab/commit/5e01d23307b3bdcd37fcbe5bed89b6d79d898c43) of my "_[I hate creating Vagrantfiles by hand](https://blog.ipspace.net/2020/12/build-labs-netsim-tools/)_" tool. It could create Vagrantfile and Ansible inventory from a (very rudimentary) network topology and deploy handcrafted device configurations on Cisco IOS and Arista EOS.
<!--more-->
Over 2100 commits from [25 contributors](https://github.com/ipspace/netlab/graphs/contributors) and over 650 issues and 800 pull requests brought us to where _netlab_ is today: a versatile virtual lab deployment tool[^GC] that supports [most networking control-plane protocols](https://netlab.tools/platforms/#supported-configuration-modules) (apart from MPLS-TE and IP multicast), [popular data plane encapsulations](https://netlab.tools/platforms/#platform-dataplane-support), and over [two dozen platforms](https://netlab.tools/platforms/#supported-virtual-network-devices) from a dozen vendors.

Thanks a million to all contributors and everyone who took their time to submit a bug report, asked a question that pushed us in the right direction, or spread the word. _netlab_ development still runs on karma points, and our total marketing budget is zero[^SDP] (not that I would want to have it any other way), so anything you can do to help us make _netlab_ better or make more networking engineers aware of what it can do is highly appreciated.

[^GC]: Some overly nice souls called it "a gamechanger"

[^SDP]: Down to at least a dozen decimal places
