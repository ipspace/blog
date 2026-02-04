---
title: "Open-Source Network Simulators (2026 Edition)"
date: 2026-02-10 08:09:00+0100
tags: [ worth reading ]
---
Brian Linkletter published an updated [overview of open-source network simulators and emulators](https://opensourcenetworksimulators.com/2026/02/open-source-simulator-emulator-in-2026/).

_containerlab_ and _GNS3_ are clear leaders (no surprise there) with the original _vrnetlab_ becoming abandonware (fortunately, we have [Roman Dodin's fork](https://github.com/srl-labs/vrnetlab)), which makes me think we should focus on using _netlab_ primarily with _containerlab_ and slowly sunset the Vagrant support, particularly considering some people actively hate the license change.

Also, if anyone feels like writing an interface (provider module) between _netlab_ and _GNS3_, the pull request would be most welcome 😎

Any thoughts? Please leave a comment!
