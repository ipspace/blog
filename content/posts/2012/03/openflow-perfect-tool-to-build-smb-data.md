---
date: 2012-03-08 08:53:00.001000+01:00
tags:
- SDN
- switching
- data center
- workshop
- OpenFlow
- virtualization
title: 'OpenFlow: A perfect tool to build SMB data center'
url: /2012/03/openflow-perfect-tool-to-build-smb-data/
---
When I was [writing about the NEC+IBM OpenFlow trials](/2012/02/necibm-enterprise-openflow-you-can/), I figured out a perfect use case for OpenFlow-controlled network forwarding: SMB data centers that need less than a few hundred physical servers -- be it bare-metal servers or hypervisor hosts (hat tip to [Brad Hedlund](http://bradhedlund.com/) for nudging me in the right direction a while ago)

{{<note>}}As I wrote before, [OpenFlow-controlled network forwarding](/2011/11/big-switch-networks-might-actually-make/) (example: NEC, BigSwitch) [experiences a totally different set of problems](/2012/01/fib-update-challenges-in-openflow/) than OpenFlow-controlled edge (example: Nicira or [XenServer vSwitch Controller](http://support.citrix.com/article/CTX130423)).{{</note>}}
<!--more-->
### The Dream

As you can imagine, it's extremely simple to configure an OpenFlow-controlled switch: configure its own IP address, management VLAN, and controller's IP address, and let the controller do the rest.

Once the networking vendors figure out "the fine details", they could use dedicated management ports for out-of-band [OpenFlow control plane](/2011/04/what-is-openflow/) (similar to what [QFabric is doing today](/2011/09/qfabric-part-1-hardware-architecture/)), DHCP to assign an IP address to the switch, and a new DHCP option to tell the switch where the controller is. The DHCP server would obviously run on the OpenFlow controller, and the whole control plane infrastructure would be completely isolated from the outside world, making it pretty secure.

The extra hardware cost for significantly reduced complexity (no per-switch configuration and a single management/SNMP IP address): two dumb 1GE switches (to make the setup redundant), hopefully running MLAG (to get rid of STP).

Finally, assuming server virtualization is the most common use case in a SMB data center, you could tightly couple OpenFlow controller with VMware's vCenter, and let vCenter configure the whole network:

-   CDP or LLDP would be used to discover server-to-switch connectivity;
-   OpenFlow controller would automatically download port group information from vCenter and automatically provision VLANs on server-to-switch links.
-   Going a step further, OpenFlow controller could automatically configure static port channels based on load balancing settings configured on port groups.

**End result**: decently large layer-2 network with no STP, automatic multipathing, and automatic adjustment to VLAN changes, with a single management interface, and the minimum number of moving parts. How cool is that?

{{<figure src="http://upload.wikimedia.org/wikipedia/en/a/a3/Escher%27s_Relativity.jpg" caption="Auto-configured data center with no spanning tree? Sure, why not ([Relativity by M.C.Escher](http://en.wikipedia.org/wiki/File:Escher%27s_Relativity.jpg)">}}

### Scenario\#1 -- GE-attached servers

If you decide to use GE-attached servers, and run virtual machines on them, it would be wise to use four to six uplinks per hypervisor host (two for VM data, two for kernel activities, optionally additional two for iSCSI or NFS storage traffic).

You could easily build a GE Clos fabric using switches from NEC America: [PF5240](http://www.necam.com/PFlow/doc.cfm?t=PFlowPF5240Switch) (ToR switch) as leaf nodes (you'd have almost no oversubscription with 48 GE ports and 4 x 10GE uplinks), and [PF5820](http://www.necam.com/Docs/?id=ba0dadc4-f253-4a8a-b27a-a791378f9acf) (10 GE switch) as spine nodes and interconnection point with the rest of the network.

Using just two PF5820 spine switches you could get over 1200 1GE server ports -- enough to connect 200 to 300 servers (around 5000 VMs).

You\'d want to keep the number of switches controlled by the OpenFlow controller low to avoid scalability issues. NEC claims they can control up to 50 ToR switches with a controller cluster; I would be slightly more conservative.

### Scenario\#2 -- 10GE attached servers

Things get hairy if you want to use 10GE-attached servers (or, to put it more diplomatically, IBM and NEC are not yet ready to handle this use case):

-   If you want true converged storage with DCB, you have to use IBM's switches (NEC does not have DCB), and even then I'm not sure how DCB would work with OpenFlow.
-   PF5820 (NEC) and G8264 (IBM) have 40GE uplinks, but I have yet to see a 40GE OpenFlow-enabled switch with enough port density to serve as the spine node. At the moment, it seems that bundles of 10GE uplinks are the way to go.
-   It seems (according to data sheets, but I could be wrong) NEC supports 8-way multipathing, and we'd need at least 16-way multipathing to get 3:1 oversubscription.

Anyhow, assuming all the bumps eventually do get ironed out, you could have a very easy-to-manage network connecting a few hundred 10GE-attached servers.

### Will it ever happen?

I remain skeptical, mostly because every vendor seems obsessed with cloud computing and [zettascale](/2011/04/new-data-center-switches-from-force10/) data centers, ignoring [mid-scale market](http://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/) ... but there might be silver lining. This idea would make most sense if you'd be able to buy a prepackaged data center (think VCE block) at a reasonably low price (to make it attractive to SMB customers).

A few companies have all the components one would need in a SMB data center (Dell, HP, IBM), and Dell just might be able to pull it off (while HP is telling everyone how they'll [forever change the networking industry](http://searchnetworking.techtarget.com/news/2240037298/HP-Discover-Wheres-the-core-networking-evolution)). And now that I've mentioned Dell: how about configuring your data center through a user-friendly web interface, and have it shipped to your location in a few weeks.

### More information

If you need to know more about data centers, network virtualization, and OpenFlow, you might find these webinars relevant:

-   Start with [Introduction to Virtualized Networking](http://www.ipspace.net/Introduction_to_Virtualized_Networking);
-   Generic data center technologies and designs are described in [Data Center 3.0 for Networking Engineer](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers), large-scale network designs (including leaf & spine and Clos network architectures) in the [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) webinar.
-   To find more about OpenFlow, watch our [OpenFlow Deep Dive](https://www.ipspace.net/OpenFlow_Deep_Dive) webinar
-   Learn everything there is to know about VMware's vSwitch and other VMware-related networking solutions in [VMware Networking Deep Dive](http://www.ipspace.net/VMware_Networking_Deep_Dive).

And don't forget: you get access to all these webinars (and numerous others) if you buy the [yearly subscription](http://www.ipspace.net/Subscription).
