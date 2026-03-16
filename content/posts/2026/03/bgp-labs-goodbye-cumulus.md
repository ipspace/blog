---
title: "BGP Labs: Goodbye, Cumulus Linux"
date: 2026-03-18 07:30:00+02:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
netlab_title: Goodbye, Cumulus Linux
BGP_tag: lab
---
When I [started the Online BGP Labs project](https://bgplabs.net/99-about/) in mid-2023, Cumulus Linux still seemed like a good platform to use. You could run devices as virtual machines (we were still supporting VirtualBox) or in containers (containerlab was improving with every release), and it looked more polished than bare-bones FRRouting.

Things only went downhill from there (from the perspective of offering a free and easy-to-use solution with a CLI resembling commonly-used devices):
<!--more-->
* Cumulus Linux containers were a hobby project that stopped the moment the engineer maintaining them left the company. Even worse (from a personal perspective), they occasionally crashed my Linux server.
* Cumulus started focusing on an [alternate user interface](/2022/09/cumulus-nclu/) (called [NVUE](/2022/10/cumulus-linux-nvue/) after the NVIDIA acquisition), which made those devices way less enticing from an educational perspective.
* [Making the community Vagrant boxes useless](/2025/02/goodbye-cumulus-community/), regwalling the Vagrant boxes and [finally dropping them](https://blog.ipspace.net/2025/06/cumulus-linux-gone/) were the last straws.

In the meantime, the FRRouting containers were becoming an easy-to-use option with an "industry standard" CLI, with Arista cEOS containers being a nice alternative if you don't mind registering to download them.

While we made the decision to stop supporting Cumulus Linux containers in _netlab_ a while ago, and later moved the [Cumulus Linux VMs](https://netlab.tools/platforms/#supported-virtual-network-devices) into the end-of-life/minimal-support tier, I never cleaned up the BGP labs. It took me ages to find the energy (and a bit of AI help :) to go through that process and clean up all 50+ lab exercises, which (I hope) now look a bit less antiquated.
