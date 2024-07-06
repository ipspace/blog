---
comment: 'While the original SDN idea (centralized control plane will solve all networking
  challenges) failed miserably, SDN became a must-use keyword, and vendors started
  calling _network management systems_ or _service provisioning systems_ SDN controllers.

  '
date: 2022-05-18 06:55:00+00:00
sdn_hype_tag: back
series:
- sdn_hype
tags:
- SDN
title: SDN Controller Taxonomy
---
Even though Gartner declared SDN _obsolete before plateau_ in their 2021 [Networking Hype Cycle](https://blogs.gartner.com/andrew-lerner/2021/10/11/networking-hype-cycle-2021/), most vendor marketers never got the memo. Anything that interacts with network devices in any way[^ANS] is called an SDN controller. Let's try to throw some minimal amount of taxonomy into that mess based on how these controllers interact with network elements (physical or virtual).
<!--more-->
[^ANS]: Even when it's using an Ansible playbook with screen scraping over an SSH session

**Centralized control plane solutions** are what Gartner considered to be SDN. Apart from a few well-architected niche solutions[^FAUCET], the laws of physics won. [Centralized control plane](/2014/01/what-exactly-is-sdn-and-does-it-make.html) was always a bad idea, and most people involved in the SDN orthodoxy eventually realized that after sobering up from a [hype-induced trip](/2021/07/openflow-realities.html)[^HEADACHE]. Nothing much to see here.

[^FAUCET]: Including a surprisingly-stable and working [SDN controller](https://faucet.nz/).

[^HEADACHE]: Some of them with an enormous headache, in particular when they worked for a vendor that bet the farm on OpenFlow.

**Controllers interacting with the control plane**. Most SD-WAN controllers are in this category. At the very minimum, they have  to act as BGP route reflectors: [collect reachability information from the SD-WAN appliances](/2015/06/software-defined-wanwell-orchestrated.html) and distribute it to other appliances.

Network virtualization controllers[^PC] are often in this category as well. Many of them use a control plane protocol (often EVPN) to interact with the outside world... although I wonder whether that's a good idea. It's interesting to see the gradual move away from the control plane interactions in VMware NSX Controller[^NSXM] -- as the product is built on ideas that came from one of the early proponents of centralized control plane, they must have hit some interesting scaling problems to move in that direction.

[^PC]: Including most large-scale public cloud implementations.

[^NSXM]: Now part of NSX Manager

**Orchestration systems**. Why would you want to call a system that provisions a service by configuring the network elements in the background an SDN controller? Oh, it's like [*bridge* and *switch*](/2011/02/how-did-we-ever-get-into-this-switching.html) -- the marketing needed a flashy new name for an old idea, and SDN was all the rage when they made the decision.

Even in this segment, there are solutions that provide true abstraction of services. A prime example is probably Cisco ACI with its endpoint groups and contracts.

Then there are solutions provisioning group policies and network services across a range of network elements. For example, you could configure a VLAN segment implemented with VXLAN and EVPN (or LISP) on all edge switches in your fabric, or an SSID across a set of wireless access points. Cisco SD-Access, Pluribus Unified Cloud Fabric, and Ubiquity UniFi SDN Controller are probably in this category.

Finally, you might encounter someone rebranding a traditional device-focused network management system into an SDN controller, proving that the marketing shenanigans are indeed limitless.

### Have I missed something?

Your comments (preferably including links to documentation) would be most welcome, including further examples of products in each category.

In case you want to send me a private message, you already have my email address if you have an [ipSpace.net subscription](https://www.ipspace.net/Subscription/), or if you're subscribed to my [SDN/automation mailing list](https://www.ipspace.net/Subscribe/Five_SDN_Tips), and there's the [Contact Us form](https://www.ipspace.net/Contact) for everyone else.
