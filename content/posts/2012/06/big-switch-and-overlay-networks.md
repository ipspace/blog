---
date: 2012-06-14 08:09:00+02:00
tags:
- SDN
- data center
- OpenFlow
- overlay networks
- virtualization
title: Big Switch and Overlay Networks
url: /2012/06/big-switch-and-overlay-networks/
---
A few days ago Big Switch announced they'll [support overlay networks in their upcoming software release](http://www.bigswitch.com/PressReleases/big-switch-announces-openflow-based-overlays-in-corona-beta-release/). After a brief "[told you so](/2012/05/virtual-networks-skype-analogy/)" moment (because [virtual networks in physical devices don't scale all that well](/2012/01/fib-update-challenges-in-openflow/)) I started wondering whether they simply gave up and decided to become a [Nicira](/2011/10/what-is-nicira-really-up-to/) copycat, so I was more than keen to have a brief chat with Kyle Forster (graciously offered by Isabelle Guis).
<!--more-->
#### The Background

Big Switch is [building a platform](/2012/02/nicira-bigswitch-nec-openflow-and-sdn/) that would allow you to create virtual networks out of any combination of physical or virtual devices. Their API or CLI allows you to specify which VLANs or MAC/IP addresses belong to a single virtual network, and their OpenFlow controller does the rest of the job. 

{{<note info>}}To see their software in action, watch their [Networking Field Day](https://techfieldday.com/companies/big-switch-networks/) presentations.{{</note>}}

#### The Shift

When I had a brief chat with Kyle during the [OpenFlow symposium](http://techfieldday.com/2011/openflow-symposium/), I mentioned that (in my opinion) they were [trying to reinvent MPLS](/2011/11/big-switch-networks-might-actually-make/) \... and he replied along the lines of "if only DC switches would have MPLS support, our life would be much easier".

Because most vendors still think [MPLS has no life in the Data Center](/2011/04/vcloud-architects-ever-heard-of-mpls/) (and [Derick Winkworth forcefully disagrees with that](http://packetpushers.net/secure-mtsz-with-vmware-vgw-and-vlan-normalization/)), Big Switch had to implement all sorts of [kludges to emulate virtual circuits with OpenFlow](/2012/02/virtual-circuits-in-openflow-10-world/) \... and faced the hard reality of real life.

Most switches installed in today's data centers don't support OpenFlow in GA software (HP Procurve series and IBM's G8264 are obvious exceptions with a tiny market share); on top of that, some customers are understandably reluctant to deploy OpenFlow-enabled switches in their production environment. Time to take a step back and refocus on the piece of the puzzle that is easiest to change -- [the hypervisor](/2011/08/imagine-ruckus-when-hypervisor-vendors/), combined with [L2 or L3 tunneling](/2011/12/decouple-virtual-networking-from/) across the network core.

Not surprisingly, they decided to use Open vSwitch with their own OpenFlow controller in Linux-based hypervisors (KVM, Xen) and they claim they have a solution for VMware environment, but Kyle was a bit tight-lipped about that one.

#### The Difference?

Based on the previous two paragraphs, it does seem that Big Switch is following Nicira's steps \... only a year or two later. However, they claim there are significant technical differences between the two approaches:

{{<figure src="/2012/06/s200-Unicorns.png" caption="Warning: we\'re entering the land of unicorns">}}

-   Using Big Switch's OpenFlow controller, you can mix-and-match physical and virtual switches. Kyle claimed we'll see switches supporting OpenFlow-controlled tunneling encap/decap in Q3/Q4 of this year. That would be a real game-changer, but I'll believe when I see this particular unicorn.
-   Nicira is focused primarily on the hypervisor environments, Big Switch can create virtual networks out of a set of hypervisors, a set of physical switches, or a combination of both (currently without tunneling).

And finally, as expected, there's a positioning game going on. According to Big Switch, all alternatives (VXLAN from Cisco, NVGRE from Microsoft and STT/GRE/OpenFlow from Nicira) expect you to embrace a fully virtually integrated stack, whereas Big Switch's controller creates a platform for integration partners. If they manage to pull this off, they just might become another [6WIND](/2012/02/6wind-solving-virtual-appliance/) or [Tail-F](http://packetpushers.net/show-81-tail-f-network-configuration-management-sponsored/) -- not exactly a bad position to be in, but also not particularly exciting to the investors. Whatever the case might be, we will definitely live in interesting times in the next few years, and I'm anxiously waiting for the moment when Big Switch decides to make its product a bit more public.
