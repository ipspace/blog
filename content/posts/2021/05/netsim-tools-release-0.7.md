---
title: "netsim-tools release 0.7: Cumulus VX, EIGRP, and BGP IPv6 AF"
date: 2021-05-31 06:58:00
tags: [ automation ]
series: netsim-tools
---
*netsim-tools* [release 0.7](https://github.com/ipspace/netsim-tools/releases/tag/release_0.7) is published, bringing you the following goodies (including stuff published a week ago as release 0.6.3):

* [Cumulus VX support](https://netsim-tools.readthedocs.io/en/latest/platforms.html) on *libvirt* and *virtualbox*.
* [EIGRP configuration module](https://netsim-tools.readthedocs.io/en/latest/module/eigrp.html)
* [BGP IPv6 address family](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html#ipv6-support)
* [Controlled BGP community propagation](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html#bgp-communities-propagation)

Other changes include:
<!--more-->
* [More control over BGP prefix advertisements](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html#advertised-bgp-prefixes)
* [OSPF reference bandwidth](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html#global-parameters)
* [Completely rewritten documentation](https://netsim-tools.readthedocs.io/en/latest/index.html)
* Typing hints in Python code and **mypy** tests (contributed by [Leo Kirchner](https://blog.kirchne.red/)).

As it looks like most network engineers interested in network automation use the Network2Code Slack team, I also created a [#netsim-tools channel](https://networktocode.slack.com/archives/C022DQHK8BH) there.

This is probably the last *netsim-tools* release before the traditional ipSpace.net summer break. Here are some ideas for future improvements, please feel free to work on them and submit a pull request ;)

* Create a Python package to simplify the installation process
* Package the Ansible playbooks and templates together with the Python source tree to minimize the pollution created by the installation process
* Use a search path to find your own configuration templates (example: implementing unnumbered BGP session on Cumulus VX) during the initial configuration
* [Create a graph/diagram out of the lab topology](https://github.com/ipspace/netsim-tools/issues/21)
* VLAN- and EVPN configuration modules

Potential new devices:

* Nokia might release their SR Linux in container format;
* Someone already mentioned vASA in #netsim-tools channel, and it looks like it should be relatively easy to create a Vagrant box... but [there's way more work to be done](https://networktocode.slack.com/archives/C022DQHK8BH/p1622272039029800).

{{<jump>}}[Download the new release](https://github.com/ipspace/netsim-tools)\
[Read the docs](https://netsim-tools.readthedocs.io/){{</jump>}}