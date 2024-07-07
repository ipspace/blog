---
date: 2015-01-21 07:44:00+01:00
tags:
- SDN
- data center
- fabric
title: Lock-In Is Inevitable – Get Used to It!
url: /2015/01/lock-in-is-inevitable-get-used-to-it/
---
For whatever reason (subliminal messages from vendor marketing departments?), I'm constantly brooding about the vendor lock-in, its inevitability, and the way supposedly disruptive companies try to use the fear of lock-in to persuade naive customers to buy their products.
<!--more-->
OpenFlow controllers are just one of the examples that come to mind. Sure, you can use them to control a fabric of cheapest switches you could get at eBay (ignoring for the moment that no two switch vendors offer the same set of OpenFlow capabilities), but you've just replaced hardware lock-in with software lock-in -- try replacing NEC's ProgrammableFlow controller with Big Switch controller or Open Daylight controller.

Umbrella orchestration products like Tail-f (now Cisco) NCS and Anuta Networks NCX are no different (see also the excellent [A-B-C of Lock-In](http://it20.info/2012/02/the-abc-of-lock-in/) post by Massimo Re Ferre).

Other areas of IT fare no better. Try moving from Ubuntu to CentOS, or from Oracle to MySQL -- the consumers of these products (application developers) rely on subtle discrepancies between the products to make their job easier (example: stored SQL procedures), inevitably locking themselves into a single product.

The only way forward is to go through the five stages of grief, accept the inevitability of lock-in, stop fighting against it (because you can't win) and figure out ways to cope with it. The ancient Romans knew one of them: divide and conquer.

For example, don't complain about the lock-in effect of vendor fabrics (Brocade VCS Fabric, Cisco ACI or DFA, Juniper Virtual Chassis Fabric, HP IRF, Plexxi ring ... you get the idea), use them in designs where lock-in won't hurt you -- build a modular data center infrastructure where you use proprietary vendor fabrics within a single availability zone, and link availability zones with boring age-old technologies: IP routing and OSPF or BGP.

On the other hand, if you design your data center as a single vendor-specific fabric, and link multiple data centers built with this approach with vendor-specific layer-2 extension technology, stop complaining about the lock-in you deserve.

### From Theory to Practice

Want to know more about data center technologies? Watch [ipSpace.net data center webinars](https://www.ipspace.net/Roadmap/Data_center_webinars). Honing your design skills? [Data Center Design Case Studies](http://www.ipspace.net/Data_Center_Design_Case_Studies) or [ipSpace Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic) might give you additional ideas.
