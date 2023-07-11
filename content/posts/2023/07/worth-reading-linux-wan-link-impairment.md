---
title: "Configuring Linux Traffic Control in a Sane Way"
date: 2023-07-11 09:42:00
tags: [ WAN ]
---
Smart engineers were forever using Linux (in particular, its [traffic control/queue discipline](https://man7.org/linux/man-pages/man8/tc.8.html) functionality) to simulate WAN link impairment. Unfortunately, there's a tiny hurdle you have to jump across: the **tc** CLI is even worse than **iptables**.

A long while ago someone [published a **tc** wrapper](https://github.com/tylertreat/comcast) that *simulates shitty network connections* and (for whatever reason) decided to call it Comcast. It probably does the job, but I would prefer to have something in Python. Daniel Dib found just that -- [tcconfig](https://github.com/thombashi/tcconfig) -- and used it to 
[simulate WAN link behavior on VMware vSphere](https://lostintransit.se/2023/07/05/building-a-wan-impairment-device-in-linux-on-vmware-vsphere/).
