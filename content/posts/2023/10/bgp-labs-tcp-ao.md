---
title: "BGP Labs: TCP-AO Protection of BGP Sessions"
date: 2023-10-12 06:05:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: edu
---
A few days after I published the [EBGP session protection](https://bgplab.github.io/bgplab/basic/6-protect/) lab, [Jeroen van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) submitted a pull request that [added TCP-AO support to _netlab_](https://netlab.tools/plugins/ebgp.utils/). Now that the [release 1.6.3 is out](https://netlab.tools/release/1.6/#release-1-6-3), I could use it to build the [Protect BGP Sessions with TCP Authentication Option (TCP-AO)](https://bgplab.github.io/bgplab/basic/9-ao/) lab exercise.
<!--more-->
{{<figure src="https://bgplab.github.io/bgplab/basic/topology-ao.png">}}

**Note:** TCP-AO is not yet supported by the Linux kernel, so you cannot use Cumulus Linux, FRR, or Arista cEOS for the external BGP routers. You will have to use virtual machines to run the lab, and you could choose between Arista EOS VM, Cisco CSR 1000v, or Nokia SR-OS (virtual machine running in a container).
