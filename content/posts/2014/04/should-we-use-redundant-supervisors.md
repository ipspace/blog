---
date: 2014-04-08 07:19:00+02:00
high-availability_tag: ignore
series:
- ha-switching
tags:
- data center
- fabric
- high availability
title: Should We Use Redundant Supervisors?
url: /2014/04/should-we-use-redundant-supervisors.html
---
I had a nice chat with Doug Gourlay from Arista during the Interop Las Vegas and he made an interesting remark along the lines of "in leaf-and-spine fabrics it doesn't make sense to use redundant supervisors in switches -- they cause more problems than they solve."

As always, in the end it all depends on your environment and use case, but he definitely has a point; good engineering always works [better than a heap of kludges](https://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html).
<!--more-->
### Going Back 20 Years

In early 90s we didn't have redundant supervisors (or CPU boards or route processors or whatever they were called). Each box had a single CPU and if you wanted to build a resilient network you did a proper network design -- for each function you needed in the network (example: core or aggregation layer) you used two (or more) boxes connected with reasonably fast-converging routing protocol. Problem solved.

We started [building Internet using those principles](http://www.ietf.org/rfc/rfc3439.txt), and [smart people still do that](https://blog.ipspace.net/2013/11/deutsche-telekom-terastream-designed.html). Surprisingly, Internet worked (and continues to work) without intra-box redundancy mechanisms.

### Carrier Grade Marketing

Are you old enough to remember the original Internet (and dot.com) bubble? In those days every telecom thought they could find gold nuggets lying in plain sight on the magical plains of planet Internet. Unfortunately, they forgot to leave their old mentality at home when joining the gold rush.

Voice switches (the gear telecom engineers were used to deal with in those days) had all sorts of redundancy. After all, you cannot connect a dumb phone to two voice switches, so you better have a switch that can never crash. Internet is slightly different -- good IP-based architectures always relied on [smart edge and simple core](https://blog.ipspace.net/2011/05/complexity-belongs-to-network-edge.html) (virtualization vendors [needed more than 10 years](http://blog.ipspace.net/2012/07/vmware-buys-nicira-hypervisor-vendor.html) to [figure that out](http://blog.ipspace.net/2012/05/virtual-networks-skype-analogy.html), but that's beyond the point).

Regardless of proven facts and working best practices, telecoms wanted to have box-level feature parity between what they knew and what they planned to buy, and networking vendors delivered what the customer wanted -- more and more complex boxes with built-in hardware redundancy and all sorts of failover mechanisms, including [SSO](/2021/09/stateful-switchover.html), [NSF](/2021/09/non-stop-forwarding.html) and [ISSU](http://www.cisco.com/c/en/us/products/ios-nx-os-software/in-service-software-upgrade-issu/index.html).

With all the great redundancy features being implemented to improve vendors' chances in carrier market, it was time to reap the benefits of that investment. Next stop: enterprise networks.

### Is It All Just Hype?

It depends. You can always implement *redundant* or *resilient* solutions. Resilient is usually better than redundant, but there are cases where boxes with redundant internal architecture come handy due to the tradeoffs you might have to make to implement a resilient design.

**Example: campus networks**. In campus networks you cannot afford to lose a whole building, but it might be OK to lose half a floor.

A resilient design would use two core switches and an access switch (or more) per floor. Ideally they'd run a fast-converging routing protocol.

In reality, you're often asked to implement bridging across a whole building, and as there are no standard layer-2 fabric solutions, you have to use spanning tree (and lose half the uplink bandwidth in the process) or [MLAG](/series/mlag.html) (which increases the complexity of your design). Also, managing tons of small switches manually (because the network management software almost never does everything its vendor has promised) becomes a royal pain.

A core switch with redundant architecture definitely seems like a better option, but do keep in mind that you've just traded visible complexity that you understand and are thus able to troubleshoot, with hidden complexity.

### Data Center Environments

Data center networks are always considered to be mission critical, and it makes perfect sense to buy an insurance policy in form of redundant hardware architecture, right? Well, no.

Unless you're Google or Facebook and can afford to lose 50 servers on a ToR switch reload you probably have dual-homed servers connected to two ToR switches, right? Losing one of those switches hurts (you lose half the bandwidth), but not too much. No wonder no ToR switches have redundant supervisors (Juniper's QFX 5100 is an interesting semi-exception: [they can run two copies of Junos as virtual machines on the same CPU](/2015/06/so-you-need-issu-on-your-tor-switch.html)).

Losing one of two core switches is a major disaster -- half the core switching bandwidth is lost. How do you cope with that? You buy switches with two supervisor boards and hope the internal hardware and software redundancy works as expected.

{{<note warn>}}I've seen data center network designs with a single core switch ("we don't need two because we bought a fully redundant box"). Don't ever do that, you'll end up with a redundantly engineered single point of failure.{{</note>}}

Now imagine you replace two humongous core switches with a [spine layer having 4 or 8 fixed](https://blog.ipspace.net/2012/11/building-leaf-and-spine-fabrics-with.html) or [modular switches](http://blog.ipspace.net/2012/05/are-fixed-switches-more-efficient-than.html). All of a sudden losing a spine switch doesn't hurt that much. Welcome to the wonderful world of proper network design ;)

### More Details

Want to know how to design a modern data center fabric? Watch these webinars:

* [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
* [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics)
* [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
