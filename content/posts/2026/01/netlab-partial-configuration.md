---
title: "Deploy Partially-Configured Training Labs with netlab"
date: 2026-01-26 07:53:00+0100
tags: [ netlab ]
netlab_tag: guidelines
---
Imagine you want to use _netlab_ to build training labs, like the [free BGP labs](https://bgplabs.net/) I created. Sometimes, you want to give students a device to work on while the other lab devices are already configured, just waiting for the students to get their job done.

{{<note info>}}
My BGP labs were designed for self-study. You might also want to listen to how [Sander Steffann uses _netlab_ in classroom training](/2025/11/using-netlab-ipv6-training/).
{{</note>}}

For example, in the [initial BGP lab](https://bgplabs.net/basic/1-session/), I didn't want any BGP-related configuration on RTR while X1 would already be fully configured -- when the student configures BGP on RTR, everything just works.
<!--more-->
{{<figure src="https://bgplabs.net/basic/topology-session.png" width="400" caption="A picture is worth a thousand words, they say. Well, you get the idea ;)">}}

_netlab_ wasn't designed to handle this scenario; I used it to build baseline configurations that the user would then expand. However, there's always another nerd knob. There were three tricks one could use in the past to get the job done:

* Use a custom configuration template that would deconfigure BGP on RTR and save the modified configuration.
* Use a plugin that would remove **bgp** from the list of modules on RTR at the end of the lab topology transformation (so we'd still get the BGP neighbor on X1)
* [A dirty trick](https://github.com/bgplab/bgplab/blob/02da26ab058613ede78afb963057d17b515ea19c/basic/1-session/topology.yml#L6) that I don't want to explain in any detail. Of course, I used this one.

Release 26.01 gives you a clean option: you can use the **[skip_config](https://netlab.tools/nodes/#node-attributes)** node (or group) attribute to tell **netlab initial** which parts of the device configuration to skip. Using that attribute, the lab topology for the initial BGP lab becomes much simpler ([original topology](https://github.com/bgplab/bgplab/blob/02da26ab058613ede78afb963057d17b515ea19c/basic/1-session/topology.yml)):

{{<printout>}}
plugin: [ bgp.session ]

version: 26.01
module: [ bgp ]

groups:
  external:
    members: [ x1 ]

nodes:
  rtr:
    bgp.as: 65000
    skip_config: [ bgp ]
  x1:
    bgp.as: 65100
    id: 10

links:
- rtr:
  x1:
    bgp.default_originate: True
{{</printout>}}

**Notes:**

* The minimum _netlab_ version this lab topology works with is 26.01 (line 3)
* The BGP configuration module is used on all devices (line 4)
* However, _netlab_ should not configure BGP on RTR (line 13)
