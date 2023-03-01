---
date: 2022-04-19 06:53:00+00:00
netlab_tag: overview
tags:
- netlab
title: Everything Is Better with a GUI (even netlab)
---
Some people think that [everything is better with Bluetooth](https://www.youtube.com/watch?v=0KXoBcQER_0). They're clearly wrong; according to the ancient wisdom of product managers working for networking vendors, everything is better with a GUI.

Now imagine adding network topology visualizer and GUI-based device access with in-browser SSH to an intent-based infrastructure-as-code virtual network function labbing tool. How's that for a Bullshit Bingo winner[^A1]?
<!--more-->
[^A1]: This would have been an awesome April 1st post; unfortunately Stefano created this functionality a few weeks too late.

On a more serious note, [Stefano Sasso](http://stefano.dscnet.org/about/) figured out the configuration file format of [Graphite](https://github.com/netreplica/graphite) (Web UI/graphing tool used with *containerlab*) and created an output module that [generates a Graphite configuration file from *netlab* lab topology](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html).

{{<figure src="/2022/04/Graphite-anycast-lab.png" caption="BGP anycast lab displayed by Graphite">}}

Adding a GUI to a *netlab* lab is as easy as 1-2-3:

* Create Graphite configuration file with **netlab create -o graphite**[^TI]
* Start the lab with **netlab up**
* [Start the Graphite container](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html#graphite-topology-output-module).

While you can use Graphite to create lab topology regardless of the virtualization provider, SSH access works only with *libvirt*-based lab ([more details](https://netsim-tools.readthedocs.io/en/dev/outputs/graphite.html#ssh-access-to-lab-devices)).

[^TI]: Tighter integration "[is on the roadmap](https://etherealmind.com/poster-eight-levels-vendor-acceptance/)".
