---
date: 2012-03-21 09:24:00+01:00
tags:
- SDN
- data center
- OpenFlow
- virtualization
title: Scalable, Virtualized, Automated Data Center
url: /2012/03/scalable-virtualized-automated-data.html
lastmod: 2020-12-25 18:17:00
---
Matt Stone sent me a great set of questions about the emerging Data Center technologies (the headline is also his, not mine) together with an interesting observation "it seems as though there is a lot of reinventing the wheel going on". Sure is -- read [Doug Gourlay's OpenFlow article for a skeptical insider view](http://www.networkworld.com/community/blog/will-openflow-solve-financial-crisis). Here\'s a lovely tidbit:

> So every few years the networking industry invents some new term whose primary purpose is to galvanize the thinking of IT purchasers, give them a new rallying cry to generate budget, hopefully drive some refresh of the installed base so us vendor folks can make our quarter bookings targets.

But I'm digressing, let's focus on Matt's questions. Here are the first few.
<!--more-->
> It seems that when you boil it down people are looking for a way to automate network configuration. (VM-aware of course) So that an administrator from either the service provider or tenant can make a few clicks and the network does what it is supposed to do.

Absolutely. I'm just not sure any more that you should be doing those changes in the networking devices (I hope you aren't reconfiguring your network every time you add a new application or a new IP phone). The final solution should be [a total decoupling](/2011/12/decouple-virtual-networking-from.html) -- network provides IP transport and the virtualized servers and appliances do whatever they like over it. The more I think about it, the more it looks like we need something like the kernel/user space split in operating systems, not an [EVB-like](/2011/05/edge-virtual-bridging-evb-8021qbg-eases.html) ever-tighter coupling between the network core and the edge.

> I don\'t have a problem with automation at all; in fact I think it would be brilliant, but why isn\'t anyone trying to attack that problem simply.

Until we make the virtual networks into applications running on top of IP, automation will remain a hard problem. You know that every data center's design (or at least the way it's wired together) is unique (which doesn't necessarily mean it's useful). Writing automation scripts that would generate network device configurations for unknown topology is a tough exercise.

I was involved with an IT-as-a-Service product that did exactly what Matt is asking for: you'd add a new user or company and the provisioning script would configure the switches and firewalls, Cisco's Call Manager (if the user has an IP phone), create user's account in Windows AD, create a new VDI VM for the user (and associated disk), install the software in VDI VM, and a few other things.

It [worked really well](/2014/11/flipit-cloud-orchestrating-it-as.html) because the underlying infrastructure was tightly controlled -- you couldn't just slap that automation tool on top of a spaghetti hodgepodge of switches, firewalls, load balancers and servers from multiple vendors (because [Gartner told you mix-and-match will automagically lower your TCO](http://h30507.www3.hp.com/t5/HP-Networking/Mythbusting-with-Gartner-The-multi-vendor-network/ba-p/83559)) and expect it to work. It's not a problem to handle multi-vendor environments, but there has to be at least some order in the chaos.

> Netconf would enable you to write the correct configuration to a switch given a set of changes from a front end. This doesn\'t seem like it would be too difficult to implement into a management suite.

Netconf is just a transport mechanism (RPC over SOAP or SSH) and a slightly more convenient encoding format (XML instead of text). It simplifies the implementation details (you don't have to write expect scripts), but not the hard part of the problem (generating device configurations).

> If the management suite is aware of virtual machines, the ACL\'s you have assigned to a given interface/VM can follow the VM where it goes too.

Absolutely, but solving the packet filtering/firewalling problem in the ToR switch is an architecturally flawed approach. It's a kludge that circumvents the lack of functionality of VMware [vSwitch](/2011/12/vmware-vswitch-baseline-of-simplicity.html). 

{{<note update>}}Please allow the late-2020 version of me to interrupt this blog post. Xen is mostly dead, OpenFlow is a fringe technology not a world-dominating miracle, vShield is dead (NSX-T is the current cool kid on the block), and I haven't heard from NEC in a long long while. Just so you know how fast things change when you're dealing with "emerging" ideas. In the meantime, VMware vSwitch remained a kludge. Some things never change.{{</note>}}

You can apply packet filters directly to VM interfaces if you use Xen or KVM and [use OpenFlow](http://blogs.citrix.com/2011/05/16/how-openflow-is-changing-networking-and-xenserver/) to download the filters to the hypervisor hosts if your distribution includes Open vSwitch. XenServer distribution includes [vSwitch Controller](http://docs.vmd.citrix.com/XenServer/6.0.0/1.0/en_gb/dvs_controller.html), an OpenFlow controller for the Open vSwitch.

VMware is solving the same problem with vShield Zones/App that has ["slightly" lower performance than kernel-based packet filters](/2011/11/junipers-virtual-gateway-virtual.html) because all VM traffic has to travel through firewall's userland.

Finally, it's just a step from what [NEC demonstrated at last Networking Tech Field Day](/2012/01/fib-update-challenges-in-openflow.html) to a [fully-automated data center network setup](/2012/03/openflow-perfect-tool-to-build-smb-data.html) that uses vCenter data to auto-provision VLANs needed by VMs. When will we see a tool like that? Who knows, it might not be sexy enough to get funding, even though it would be extremely useful to mid-range customers (but they are [usually the ones getting ignored by the vendors](http://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/)).

## More information

I talked about these topics in a [CloudCast Episode 34](http://www.thecloudcast.net/2012/03/cloudcast-eps34-new-networks-for-cloud.html), and you can find more details in ipSpace.net [virtualization](http://www.ipspace.net/Roadmap/Virtualization_webinars) and [data center](http://www.ipspace.net/Roadmap/Data_center_webinars) webinars.