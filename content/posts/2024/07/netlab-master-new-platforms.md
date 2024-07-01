---
title: "Master New Platforms and Technologies with netlab"
date: 2024-07-03 07:27:00+0200
tags: [ netlab ]
netlab_tag: use
---
One of my readers sent me this remark (probably while trying to work on the [EBGP Sessions over the IPv6 LLA Interfaces](https://bgplabs.net/basic/d-interface/) lab):

> I did attempt some of your labs, like IPv6 link-local-only BGP with FRR hosts, but FRR seemed not to play ball, or I was just doing it wrong.

As he was already using *[netlab](https://netlab.tools/)*, I could send him a cheat code:
<!--more-->
> _netlab_ supports interface EBGP sessions, and we tested them with FRR, so we know they work. Create the corresponding topology, start the lab, and explore ;)

Let's unpack this:

* How could I know if I could use _netlab_ to try something new? Check the [supported platforms](https://netlab.tools/platforms/), [supported technologies](https://netlab.tools/module-reference/), and whether the feature you want to test is supported on the platform you're interested in. For example, the [BGP configuration module](https://netlab.tools/module/bgp/) implements interface EBGP sessions, and they seem to be [supported on FRR](https://netlab.tools/module/bgp/#platform-support).

{{<note info>}}As always, the documentation could lag behind the implemented features (or we could overpromise and underdeliver). Whenever in doubt, explore the [list of tested features](https://release.netlab.tools/). For example, [these are the BGP features that were tested to work on FRR](https://release.netlab.tools/_html/frr-clab-bgp).{{</note>}}

* What topology could I use? The *netlab-examples* repository includes a [BGP Unnumbered](https://github.com/ipspace/netlab-examples/tree/master/BGP/Unnumbered) topology -- precisely what we need.
* How do I start the lab? As we're discussing FRR, you could [open the *netlab-examples* repository in GitHub codespaces](/2024/07/netlab-examples-codespaces.html), change the working directory, and start the lab.

But wait, it gets better: you can generate the configurations for any device supported by _netlab_ without having the virtualization environment or the device images installed:

* Create the desired topology.
* Transform the topology with **netlab create**
* Create the initial device configurations with **netlab initial -o**

As before, you don't have to install *netlab* (or any software) to get that done; use GitHub codespaces or start the [prebuilt *netlab* container](https://github.com/ipspace/netlab/pkgs/container/netlab%2Fdevcontainer).
