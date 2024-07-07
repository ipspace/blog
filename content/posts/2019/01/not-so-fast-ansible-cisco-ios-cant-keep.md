---
cli_tag: challenge
date: 2019-01-29 08:44:00+01:00
series:
- cli
tags:
- Ansible
- MPLS VPN
title: Not So Fast Ansible, Cisco IOS Can’t Keep Up…
url: /2019/01/not-so-fast-ansible-cisco-ios-cant-keep/
---
Remember how earlier releases of Nexus-OS [started dropping configuration commands if you were typing them too quickly](/2017/04/lets-drop-some-random-commands-shall-we/) (and how it was declared a feature ;)?

[Mark Fergusson](https://nexthop.global/) had a similar experience on Cisco IOS. All he wanted to do was to use Ansible to configure a VRF, an interface in the VRF, and OSPF routing process on Cisco CSR 1000v running software release 15.5(3).

Here's what he was trying to deploy. Looks like a configuration straight out of an MPLS book, right?
<!--more-->
``` code
ip vrf Customer_A
 rd 65000:1
 route-target import 65000:1
 route-target export 65000:1
!
interface GigabitEthernet1.146
 ip vrf forwarding Customer_A
 ip address 155.1.146.1 255.255.255.0
 ip ospf 2 area 0

router ospf 2 vrf Customer_A
  router-id 155.1.146.1
  redistribute bgp 65000 subnets
```

Guess what... when he tried to push that configuration to his CSR 1000v with Ansible **ios_config** module the in-VRF OSPF router process refused to start claiming it cannot get a router ID (*%OSPF-4-NORTRID: OSPF process 2 failed to allocate unique router-id and cannot start*). The whole thing worked when he tried to configure OSPF a bit later -- looks like it takes some time to get a subinterface ready after it's been configured, and if you're typing too quickly you're out of luck.

{{<note info>}}Keep in mind that Ansible uses SSH session to configure a Cisco IOS device, so it's doing the exact same thing as if you'd be a really fast typist.{{</note>}}

I could see two immediate solutions to this problem:

-   Get a router that [has a decent API](/2016/10/network-automation-rfp-requirements/) and all-or-nothing commit mechanism;
-   Split the configuration in two parts and push them to the device using two **ios_config** calls. It takes Ansible long enough to work through its gazillion layers of abstraction for Cisco IOS to realize what just happened.

On a somewhat tangential note, a friend of mine [called the current state of network automation](https://github.com/nremeetup/talks/blob/master/December_2018/NRE_December_2018.pptx) "Unix Scripting in 1970s". Unfortunately he wasn't too far off...

---

To learn more about network automation with Ansible start with our [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar and when you're ready to move from writing playbooks to building solutions [enroll](https://www.ipspace.net/Building_Network_Automation_Solutions#register) into [Building Network Automation Solutions online course](https://www.ipspace.net/Building_Network_Automation_Solutions).
