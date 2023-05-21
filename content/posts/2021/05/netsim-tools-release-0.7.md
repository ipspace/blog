---
date: 2021-05-31 06:58:00+00:00
netlab_tag: archive
series_title: Cumulus VX, EIGRP, and BGP IPv6 AF
tags:
- netlab
title: 'netsim-tools release 0.7: Cumulus VX, EIGRP, and BGP IPv6 AF'
---
*netsim-tools* release 0.7 is published, bringing you the following goodies (including stuff published a week ago as release 0.6.3):

* [Cumulus VX support](https://netlab.tools/platforms/) on *libvirt* and *virtualbox*.
* [EIGRP configuration module](https://netlab.tools/module/eigrp/)
* [BGP IPv6 address family](https://netlab.tools/module/bgp/#ipv6-support)
* [Controlled BGP community propagation](https://netlab.tools/module/bgp/#bgp-communities-propagation)

Other changes include:
<!--more-->
* [More control over BGP prefix advertisements](https://netlab.tools/module/bgp/#advertised-bgp-prefixes)
* [OSPF reference bandwidth](https://netlab.tools/module/ospf/#global-parameters)
* [Completely rewritten documentation](https://netlab.tools/)
* Typing hints in Python code and **mypy** tests (contributed by [Leo Kirchner](https://blog.kirchne.red/)).

As it looks like most network engineers interested in network automation use the Network2Code Slack team, I also created a [#netsim-tools channel](https://networktocode.slack.com/archives/C022DQHK8BH) there.

This is probably the last *netsim-tools* release before the traditional ipSpace.net summer break. Here are some ideas for future improvements, please feel free to work on them and submit a pull request ;)

* Create a Python package to simplify the installation process
* Package the Ansible playbooks and templates together with the Python source tree to minimize the pollution created by the installation process
* Use a search path to find your own configuration templates (example: implementing unnumbered BGP session on Cumulus VX) during the initial configuration
* [Create a graph/diagram out of the lab topology](https://github.com/ipspace/netlab/issues/21)
* VLAN- and EVPN configuration modules

Potential new devices:

* Nokia might release their SR Linux in container format;
* Someone already mentioned vASA in #netsim-tools channel, and it looks like it should be relatively easy to create a Vagrant box... but [there's way more work to be done](https://networktocode.slack.com/archives/C022DQHK8BH/p1622272039029800).

{{<jump>}}[Read the docs](https://netlab.tools/){{</jump>}}
