---
kb_section: MH_SOHO
minimal_sidebar: true
title: Not-so-Very-Static Routes
alt_section: posts
---
Cisco IOS Release 12.3(4)T introduced *Enhanced Object Tracking*, which, together with *Reliable Static Routing Using Object Tracking* introduced in IOS release 12.3(8)T, solves the problem. *Enhanced Object Tracking* introduces a generic **track** object that can track the state of an interface (layer-2 or layer-3 state), the presence or metric of an IP route, the state of an SLA measurement, or even the availability of Mobile IP home agent or GPRS nodes. You can also combine various track objects (including weighing them) into a compound object.

The *Reliable Static Routing Using Object Tracking* feature ties a **track** object to a static route – whenever the **track** object’s state is *down*, the static route is removed from the routing table; precisely what you would need to support reliable multi-homing. To configure a static route based on the state of the next-hop router, you need to:

* Configure an **ip sla** (previously known as Response Time Reporter – **rtr**) object pinging the next-hop router on the primary Internet link. The polling **frequency** you specify (in seconds) depends on the reliability requirements, but don't exaggerate. Anything below a few seconds would unnecessarily burden the next-hop router (as you might not be the only one tracking its availability).

{{<cc>}}Pinging next-hop router{{</cc>}}
```
ip sla 100
 icmp-echo 172.16.1.2 source-interface Serial0/0/0
 timeout 500
 frequency 3
!
ip sla schedule 100 life forever start-time now
```

{{<note>}}You cannot change the parameters of an SLA object once you’ve scheduled it. To change the target IP address, timeouts, or polling frequency, you must delete and recreate the SLA object.{{</note>}}

* Create a **track** object monitoring the reachability of the SLA target. As you probably don’t want to respond to a single lost ICMP packet, you should use the **delay** option of the **track** object to specify how long the next-hop router should remain unreachable before it’s declared to be lost (the **down** delay should be approximately three times the SLA polling frequency and the **up** delay should be even longer).

{{<note>}}When calculating the **up** delay, remember that a router can temporarily respond to pings during the bootstrap process.{{</note>}}

{{<cc>}}Tracking the state of the next-hop router{{</cc>}}
```
track 100 rtr 100 reachability
 delay down 10 up 20
```

* After configuring the **track** object, attach it to the primary static default route to ensure that the default route is removed if the next-hop router is not reachable:

{{<cc>}}Conditional static default route{{</cc>}}
```
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A track 100
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 251 name ISP_B_FB
```

You can check the proper operation of the reliable static routing with the **show ip route** command. The following listings display:

* The IP routing table on the GW router when the primary next-hop router is available
* The modified state of the IP routing table after the primary next-hop router failure.

{{<cc>}}IP routing table with operational primary next-hop router{{</cc>}}
```
GW#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP

Gateway of last resort is 0.0.0.0 to network 0.0.0.0

     172.17.0.0 255.255.255.252 is subnetted, 1 subnets
C       172.17.3.0 is directly connected, Serial0/0/1
     172.16.0.0 255.255.255.252 is subnetted, 1 subnets
C       172.16.1.0 is directly connected, Serial0/0/0
C    192.168.0.0 255.255.255.0 is directly connected, FastEthernet0/0
S*   0.0.0.0 0.0.0.0 is directly connected, Serial0/0/0
```

{{<cc>}}IP routing table after the next-hop router failure{{</cc>}}
```
GW#show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP

Gateway of last resort is 0.0.0.0 to network 0.0.0.0

     172.17.0.0 255.255.255.252 is subnetted, 1 subnets
C       172.17.3.0 is directly connected, Serial0/0/1
     172.16.0.0 255.255.255.252 is subnetted, 1 subnets
C       172.16.1.0 is directly connected, Serial0/0/0
C    192.168.0.0 255.255.255.0 is directly connected, FastEthernet0/0
S*   0.0.0.0 0.0.0.0 is directly connected, Serial0/0/1
```