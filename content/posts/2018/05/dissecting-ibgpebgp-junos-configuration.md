---
date: 2018-05-22 08:31:00+02:00
dcbgp_tag: rant
evpn_tag: details
series:
- dcbgp
tags:
- design
- BGP
- EVPN
title: Dissecting IBGP+EBGP Junos Configuration
url: /2018/05/dissecting-ibgpebgp-junos-configuration.html
---
Networking engineers familiar with Junos love to tell me how easy it is to configure and operate IBGP EVPN overlay on top of EBGP IP underlay. Krzysztof Szarkowicz was kind enough to send me the (probably) simplest possible configuration (here's [another one by Alexander Grigorenko](http://jncie.tech/2018/01/28/bgp-design-options-for-evpn-in-data-center-fabrics/))

{{<note info>}}To learn more about EVPN technology and its use in data center fabrics, watch the [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.{{</note>}}
<!--more-->
``` code
routing-options {
 router-id 192.168.0.1;
 autonomous-system 65000;  global AS used for BGP Overlay (EVPN) and for RT autogeneration
}
protocols {
 bgp {
  group IBGP-OVERLAY {
   type internal;  IBGP (local AS used from routing-options section) 
   local-address 192.168.0.1;
   family evpn {
    signaling;
   }
   neighbor 192.168.0.4 {
    description Spine-4-Loopback;
   }
   neighbor 192.168.0.5 {
    description Spine-5-Loopback;
   }
  }
  group EBGP-UNDERLAY {
   type external;                        EBGP
   local-as 65001 no-prepend-global-as;  local AS used for EBGP underlay
   neighbor 10.0.0.1 {                   Spine 4 physical interface
    peer-as 65004;
   }
   neighbor 10.0.0.3 {                   Spine 5 physical interface
    peer-as 65005;
   }
  }
 }
}
```

Most BGP implementations (including Junos) have a single BGP routing process with a single BGP AS number, so it's hard to see how you could easily use IBGP and EBGP with the same neighbor (spine switch). Let's dissect the configuration to see how it's done:

* The overlay group of BGP neighbors is easy to understand: we're running IBGP with them (assuming their AS number matches our AS number). All leaf switches use the same AS number configuring in the **routing-options** section. Currently you cannot use different AS numbers for leaf switches with Junos if you want to use automatic route targets.

{{<note>}}See [Alexander's example](http://jncie.tech/2018/01/28/bgp-design-options-for-evpn-in-data-center-fabrics/) for more details on what needs to happen on the spine switches.{{</note>}}

* Underlay sessions use EBGP -- the remote AS number is supposed to be different from local AS number. Somewhat hard to do when you want all switches to be in the same autonomous system (for EVPN reasons).

{{<note>}}At this point you should probably ask yourself "*why don't they just use IBGP everywhere if they're so keen on having IBGP for EVPN*". Yep, good question...{{</note>}}

There are a few tricks you can use to make this work:

-   If you don't run EVPN on the spine switches but use virtual routers as IBGP route reflectors, use the same AS number on all leaf switches, and disable the AS-path checks. If I got it right you'd need to use **loops** on leaf switches and **advertise-peer-as** on spine switches.
-   Alternatively, the leaf switches could pretend to be in a different AS number. You could use **local-as** to achieve that... but that would result in weird AS-paths containing both local AS number (65001) and global AS number (65000). Needless to say, you'd need **loops** configured on remote leaf switch to get the BGP path accepted (because the local AS is already in the AS-path).
-   Krzysztof used another trick: **no-prepend-global-as** removes the global AS number (65000) from the advertised AS-path, resulting in what seems to be a perfect EBGP underlay... until you have to troubleshoot it at 2AM on a Sunday morning (see also: [troubleshooting models](https://rule11.tech/troubleshooting-models/) by Russ White).

Last question: is this capability unique to Junos? Of course not. You have to use **local-as \<asn\> no-prepend replace-as** on Nexus OS (and something very similar on Cisco IOS) to get exactly the same behavior.

Is the *industry-standard CLI* (read: Cisco IOS) equivalent of Junos configuration as confusing as some people claim? Of course not -- use BGP neighbor templates. The only difference between Junos and Cisco IOS (or Nexus-OS) configuration is that in Junos you split neighbors into groups and define group parameters next to list of neighbors, whereas in Cisco IOS you define neighbor templates, and then apply them to individual neighbors.

What you should really ask yourself though is: Why the \*\*\*\* are we discussing this pile of \*\*\*\* - why don't we use a simple design that everyone has a chance of understanding and that works reasonably well at scale we need... like IBGP-over-IGP? Glad you asked -- I get called all sorts of names when [saying that out loud](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics), or pointing out that [IGP is probably good enough](/2018/05/is-ospf-or-is-is-good-enough-for-my.html) for what you need. Maybe it\'s time to step back and ask \"*What problem are we trying to solve?*\"

### Master EVPN and Data Center Fabrics

You can use these ipSpace.net webinars (all of them available with [standard ipSpace.net subscription](http://www.ipspace.net/Subscription)) to learn more about EVPN and data center fabrics:

-   [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) will tell you all you need to know about EVPN technology;
-   [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) describes typical fabric designs, including using EVPN to build mixed L2+L3 fabrics;
-   [Data Centers for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) and [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) should be the first steps in your journey if you know nothing about data center networking;

Finally, if you're looking for a guided and mentored tour with plenty of peer- and instructor support, check out the [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
