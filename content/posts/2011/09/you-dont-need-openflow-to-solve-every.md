---
comment: "Networking engineers’ reactions to OpenFlow were easy to predict – from\
  \ “this will never work” to “here’s how I can solve my problem with OpenFlow.” It\
  \ turns out we can solve many problems without involving OpenFlow; the traditional\
  \ networking protocols are often good enough. \n"
date: 2011-09-13 06:29:00+02:00
openflow_101_tag: ugly
series:
- openflow_101
series_weight: 180
tags:
- SDN
- switching
- OpenFlow
title: You Don’t Need OpenFlow to Solve Every Age-Old Problem
url: /2011/09/you-dont-need-openflow-to-solve-every/
---
I read two great blog posts on Sunday: evergreen [*Fallacies of Distributed Computing*](http://lonesysadmin.net/2011/09/10/fallacies-of-distributed-computing/) from Bob Plankers and forward-looking [*Understanding Hadoop Clusters and the Network*](https://bradhedlund.com/2011/09/10/understanding-hadoop-clusters-and-the-network/) from Brad Hedlund. Read them both before continuing (they are both great reads) and try to figure out why I'm mentioning them in the same sentence (no, it's not the fact that Hadoop uses distributed computing).
<!--more-->
OK, here's the quote that ties them together. While describing *rack awareness* Brad wrote:

> What is NOT cool about Rack Awareness at this point is the manual work required to define it the first time, continually update it, and keep the information accurate. If the rack switch could auto-magically provide the Name Node with the list of Data Nodes it has, that would be cool. Or vice versa, if the Data Nodes could auto-magically tell the Name Node what switch they're connected to, that would be cool too. Even more interesting would be a OpenFlow network, where the Name Node could query the OpenFlow controller about a Node's location in the topology.

The "only" problem with Brad's reasoning is that we already have the tools to do exactly what he's looking for. The magic acronym is [LLDP (802.1AB)](http://standards.ieee.org/getieee802/download/802.1AB-2005.pdf).

**LLDP has been standardized years ago** and is available on numerous platforms, including Catalyst and Nexus switches, and Linux operating system (for example, [lldpad](http://www.open-lldp.org/open-lldp) is part of the standard Fedora distribution). Not to mention that every [DCB](/tag/dcb/)-compliant switch must support LLDP as the DCBX protocol uses LLDP to advertise DCB settings between adjacent nodes.

**The LLDP MIB is standard** and allows anyone with SNMP read access to discover the exact local LAN topology -- the connected port names, adjacent nodes (and their names), and their management addresses (IPv4 or IPv6). The management addresses that should be present in LLDP advertisements can then be used to expand the topology discovery beyond the initial set of nodes (assuming your switches do include it in LLDP advertisement; for example, NX-OS does but Force10 doesn\'t).

Building the exact network topology from LLDP MIB is a very trivial exercise. Even a [somewhat reasonable API](http://search.cpan.org/~emiller/SNMP-Info-2.00/Info/LLDP.pm) is available (yeah, having an API returning a network topology graph would be even cooler). Mapping the Hadoop Data Nodes to TOR switches and Name Nodes can thus be done on existing gear using existing protocols \... or maybe someone already did it? Tell me in the comments.

Would OpenFlow bring anything to the table? Actually not, it also needs packets exchanged between adjacent devices to discover the topology and the easiest thing for OpenFlow controllers to use is \... ta-da \... [LLDP \... oops, OFDP](http://groups.geni.net/geni/wiki/OpenFlowDiscoveryProtocol), because LLDP just wasn't good enough. The "only" difference is that in the traditional network the devices would send LLDP packets themselves, whereas in the OpenFlow world the controller would use *Packet-Out* messages of the OpenFlow control session to send LLDP packets from individual controlled devices and wait for *Packet-In* messages from other device to discover which device received them.

The Linux configuration wouldn't change much. If you want the switches to see the hosts, you still have to run LLDP (or OFDP or whatever you call it) daemon on the hosts.

Last but definitely not least, you could use well-defined SNMP protocol with a number of readily-available Linux or Windows libraries to read the LLDP results available in the SNMP MIB in the "old world" devices. I'm still waiting to see the high-level SDN/OpenFlow API; everything I've seen so far are OpenFlow virtualization attempts (multiple controllers accessing the same devices) and [discussions indicating standard API isn't necessarily a good idea](http://networkheresy.wordpress.com/2011/08/09/what-might-an-sdn-controller-api-look-like-and-should-we-standardize-it/). Really? Haven't you learned anything from the database world?

So, why did I mention the two posts at the beginning of this article? Because Bob pointed out that "those who cannot remember the past are condemned to fulfill it." At the moment, OpenFlow seems to fit the bill perfectly.
