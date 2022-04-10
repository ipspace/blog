---
title: "Everything Is Better with a GUI (even netsim-tools)"
date: 2022-04-18 06:53:00
tags: [ automation ]
series: netsim
netsim_tag: overview
---
Some people think that [everything is better with Bluetooth](https://www.youtube.com/watch?v=0KXoBcQER_0). They're clearly wrong; according to the ancient wisdom of product managers working for networking vendors, everything is better with a GUI.

Now imagine adding network topology visualizer and GUI-based device access with in-browser SSH to an intent-based infrastructure-as-code virtual network function labbing tool. How's that for a Bullshit Bingo winner[^A1]?
<!--more-->
[^A1]: Imagine Stefano creating this functionality a few weeks ago -- this would have been an awesome April 1st post.

On a more serious note, Stefano Sasso figured out the configuration file format of [Graphite](https://github.com/netreplica/graphite) (Web UI/graphing tool used with *containerlab*) and created an output module that [generates a Graphite configuration file from *netsim-tools* lab topology](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html).

{{<figure src="/2022/04/Graphite-anycast-lab.png" caption="BGP anycast lab displayed by Graphite">}}

Adding a GUI to a *netsim-tools* lab is as easy as 1-2-3:

* Create Graphite configuration file with **netlab create -o graphite**
* Start the lab with **netlab up**
* [Start the Graphite container](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html#graphite-topology-output-module).

At the moment, the solution works only with *libvirt*-based lab ([more details](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html#ssh-access-to-lab-devices)). We'll ship it in *netsim-tools* release 1.2.1; to use it now, upgrade *netsim-tools* with `pip3 install --upgrade --pre netsim-tools`.
