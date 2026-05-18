---
title: "Goodbye, Ubuntu 20.04 (netlab 26.05)"
series_title: "Goodbye, Ubuntu 20.04"
date: 2026-05-18 07:43:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.05 is out. I'll write about its [highlights](https://netlab.tools/release/26.04/) tomorrow; today, I want to focus on one of its breaking changes: _netlab_ no longer works with Python 3.8 (which reached end-of-life in October 2024), so you can no longer install it on a vanilla Ubuntu 20.04 (which reached end of standard support a year ago).

We wanted to get rid of old Python versions for ages, but never did because Ubuntu 20.04 shipped with Python 3.8, and many _netlab_ early adopters installed it on Ubuntu 20.04 (and the last thing a networking engineer wants is wasting time with upgrades, right?).
<!--more-->
However, the latest _containerlab_ release (0.75.0) [stopped working on ancient container software](https://github.com/ipspace/netlab/issues/3350), and that was the last nudge we needed to rip off that bandaid.

The *networklab* package in release 26.05 is thus defined to run on Python 3.10 and above. You might be able to continue using _netlab_ with Ubuntu 20.04 if you manage to install Python 3.10 on that system. If you decide to do that, disable the *containerlab* version check with `netlab defaults 'providers.clab.probe=[]'` to continue working with older *containerlab* releases that run on Ubuntu 20.04 (at least until *containerlab* developers fix [this issue](https://github.com/srl-labs/containerlab/issues/3182)).

However, don't rush with upgrading your old ancient _netlab_ servers. We're still discovering quirks in Ubuntu 24.04 (primarily [different QEMU defaults](https://github.com/ipspace/netlab/pull/3406) and [edge cases](https://github.com/ipspace/netlab/issues/3403)) and ironing them out. On the other hand, we'd love to have more people reporting those quirks, so if you don't mind [opening an issue or two](https://github.com/ipspace/netlab/issues/new/choose), please do the upgrade ;)

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
