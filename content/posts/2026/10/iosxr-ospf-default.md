---
title: "Crazy Delay: IOS XR OSPFv2 Default Route Origination"
date: 2026-10-13 08:41:00+0200
tags: [ OSPF, netlab ]
netlab_tag: quirks
ospf_tag: details
---
I decided to make Netmiko the default configuration deployment method netlab uses for Cisco IOS XR. It works great, and I don't have to worry about whether the user runs IOS XRd control-plane (in which case scripts work) or vRouter (in which case there's a VM inside the container, so no luck).

After fixing the initial glitches (more on that another time), all integration tests passed *except the OSPFv2 default origination test*. It turns out the default waiting time (30 seconds) is way too low; Cisco IOS XR needs almost 90 seconds (after its reboot completes) to originate the OSPFv2 default route.
<!--more-->
Here are the related OSPF logs. Note the long delay between "OSPF is up and running" and "Let's advertise the default route":

```
 16:34:44.252 UTC: ospf[1035]: %ROUTING-OSPF-5-HA_NOTICE_START : Starting OSPF
 16:34:44.366 UTC: ospf[1035]: %ROUTING-OSPF-6-HA_INFO : Process 1: OSPF process initialization complete
 16:34:44.377 UTC: ospf[1035]: %ROUTING-OSPF-5-HA_NOTICE : Process 1: Signaled PROC_AVAILABLE
 16:34:44.424 UTC: config[66603]: %MGBL-CONFIG-6-DB_COMMIT : Configuration committed by user 'clab'. Use 'show configuration commit changes 1000000004' to view the changes.
 16:34:44.457 UTC: config[66603]: %MGBL-SYS-5-CONFIG_I : Configured from console by clab on vty0 (192.168.121.1)
 16:34:45.684 UTC: ssh_syslog_proxy[1188]: %SECURITY-SSHD_SYSLOG_PRX-6-INFO_GENERAL : sshd[5062]: Connection closed by 192.168.121.1 port 48960
 16:34:48.062 UTC: ssh_syslog_proxy[1188]: %SECURITY-SSHD_SYSLOG_PRX-6-INFO_GENERAL : sshd[5218]: Accepted authentication/pam for clab from 192.168.121.1 port 43990 ssh2
 16:34:50.155 UTC: ospf[1035]: %ROUTING-OSPF-5-ADJCHG : Process 1, Nbr 10.0.0.3 on GigabitEthernet0/0/0/0 in area 0.0.0.0 from LOADING to FULL, Loading Done, vrf default vrfid 0x60000000
 16:36:14.380 UTC: ospf[1035]: op_defer_default_info_orig 0 vrfid 0x60000000
 16:36:14.380 UTC: ospf[1035]: Redist default check: default_route (nil)  event 0x1
 16:36:14.380 UTC: ospf[1035]:  Generate external LSA 0.0.0.0, mask 0.0.0.0, type 5, age 0, metric 40, seq 0x80000001, origin: redistributed
 16:36:20.391 UTC: ospf[1035]:  Build router LSA for area 0.0.0.0, router ID 10.0.0.1, seq 0x80000003 vrfid 0x60000000
```

Now for the crazy part: OSPFv3 works like a charm. The delay happens only with OSPFv2.

FWIW, here's the relevant IOS XR OSPFv2 configuration. If you have an idea how to tweak it to reduce that delay, please leave a comment. Thank you!

{{<printout caption="Cisco IOS XR OSPFv2 configuration">}}
router ospf 1
 ! These throttle timers are probably too aggressive for a production network but
 ! make labs run better ;)
 log adjacency changes
 router-id 10.0.0.1
 loopback stub-network enable
 timers throttle lsa all 10 20 100
 timers throttle spf 10 20 100
 default-information originate always metric 40 metric-type 2
 area 0.0.0.0
  interface Loopback0
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
{{</printout>}}
