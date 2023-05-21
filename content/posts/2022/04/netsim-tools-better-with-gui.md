---
date: 2022-04-19 06:53:00+00:00
lastmod: 2023-04-27 09:00:00
netlab_tag: overview
tags:
- netlab
title: Everything Is Better with a GUI (even netlab)
---
Some people think that [everything is better with Bluetooth](https://www.youtube.com/watch?v=0KXoBcQER_0) (or maybe it's AI these days). They're clearly wrong; according to the ancient wisdom of product managers working for networking vendors, everything is better with a GUI.

Now imagine adding network topology visualizer and GUI-based device access with in-browser SSH to an intent-based infrastructure-as-code virtual network function labbing tool. How's that for a Bullshit Bingo winner[^A1]?
<!--more-->
[^A1]: This would have been an awesome April 1st post; unfortunately Stefano created this functionality a few weeks too late.

On a more serious note, [Stefano Sasso](http://stefano.dscnet.org/about/) figured out the configuration file format of [Graphite](https://github.com/netreplica/graphite) (Web UI/graphing tool used with *containerlab*) and created an output module that [generates a Graphite configuration file from *netlab* lab topology](https://netlab.tools/extool/graphite/).

{{<figure src="/2022/04/Graphite-anycast-lab.png" caption="BGP anycast lab displayed by Graphite">}}

Adding a GUI to a *netlab* lab is as easy as 1-2-3:

* Install Docker on your Linux host (Graphite works with *libvirt* or *containerlab* [virtualization providers](https://netlab.tools/providers/)).
* Add the *graphite* external tool to your lab topology -- it's just two extra lines:

```
tools:
  graphite:
```

* Start the lab with **[netlab up](https://netlab.tools/netlab/up/)**

As the last step in the lab startup process, **netlab up** command will:

* Create Graphite configuration files
* Start the Graphite container
* Print the URL to use to access the GUI.

**Notes:**

* The functionality described in this blog post works with [*netlab* release 1.5.2 or higher](https://netlab.tools/release/1.5/#release-1-5-2).
* If you want to access the GUI from another host, replace the loopback IP address in the URL with the physical IP address of your lab host.

### Revision History

2023-04-27
: Rewrote the blog post to describe the new *[external tools](https://netlab.tools/extools/)* functionality.
