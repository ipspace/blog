---
kb_section: MH_SOHO
minimal_sidebar: true
title: Not-so-Very-Static Routes
alt_section: posts
---
Numerous network devices can combine static routes with Bidirectional Forwarding Detection (BFD) and remove them from the routing table if the BFD session with the next-hop router fails. Unfortunately, that works only if the upstream network supports BFD on its customer-facing interfaces[^UBFD]; we need a more generic solution that does not rely on the functionality of the upstream router[^ECHO].

[^UBFD]: An [RFC published in March 2025](https://www.rfc-editor.org/rfc/rfc9747.html) specifies yet another twist in the BFD saga: the ability to run BFD with yourself without the BFD control session with the next-hop router.

[^ECHO]: So far, I haven't found a router from a major vendor that would implement the most straightforward idea: send a packet to yourself using the MAC address of the next-hop router. Instead, they love to start a quest to boil the ocean with solutions like BFD and then modify them further with things like *Unaffiliated BFD*.

Cisco IOS includes *Enhanced Object Tracking* functionality, which, together with *Reliable Static Routing Using Object Tracking*, solves the "Is the next hop reachable?" problem without relying on the adjacent router's cooperation.

*Enhanced Object Tracking* introduces a generic **track** object that can track the state of an interface (layer-2 or layer-3 state), the presence or metric of an IP route, the state of an SLA measurement, or even the availability of Mobile IP home agent or GPRS nodes. You can also combine various track objects (including weighing them) into a compound object.

The *Reliable Static Routing Using Object Tracking* feature ties a **track** object to a static route – whenever the **track** object’s state is *down*, the static route is removed from the routing table; precisely what you would need to support reliable multi-homing. To configure a static route based on the state of the next-hop router, you need to:

* Configure an **ip sla** (previously known as Response Time Reporter – **rtr**) object pinging the next-hop router on the primary Internet link. The polling **frequency** you specify (in seconds) depends on the reliability requirements, but don't exaggerate. Anything below a few seconds would unnecessarily burden the next-hop router (as you might not be the only one tracking its availability).

{{<cc>}}Pinging next-hop router{{</cc>}}
```
ip sla 100
 icmp-echo 172.16.1.2 source-interface GigabitEthernet0/2
 threshold 500
 timeout 1000
 frequency 3
ip sla schedule 100 life forever start-time now
```

{{<note>}}
You cannot change the parameters of an SLA object once you’ve scheduled it. To change the target IP address, timeouts, or polling frequency, you must delete and recreate the SLA object.
{{</note>}}

* Create a **track** object monitoring the reachability of the SLA target.
* As you probably don’t want to respond to a single lost ICMP packet, you should use the **delay** option of the **track** object to specify how long the next-hop router should remain unreachable before it’s declared lost.
* The **down** delay should be at least three times the SLA polling frequency
* To deal with intermittent connectivity, the **up** delay should be even longer than the **down** delay. For example, a router can temporarily respond to pings while it boots.

{{<cc>}}Tracking the state of the next-hop router{{</cc>}}
```
track 100 ip sla 100 reachability
 delay down 10 up 20
```

* After configuring the **track** object, attach it to the primary static default route to ensure that the default route is removed if the next-hop router is not reachable:

{{<cc>}}Conditional static default route{{</cc>}}
```
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2 172.16.1.2 10 name ISP_A track 100
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/3 172.17.3.2 251 name ISP_B_FB
```

{{<note info>}}
The complete configuration of the gateway router is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/gw-reliable-static-routes.cfg).
{{</note>}}

You can check the proper operation of the reliable static routing with the **show ip route** command. The following listings display:

* The IP routing table on the GW router when the primary next-hop router is available
* The modified state of the IP routing table after the primary next-hop router failure.

{{<note info>}}
You can shut down the GW-PE_A link on PE_A with the `netlab config ifdown -l pe_a` command if you're using _netlab_ topology to recreate this setup.

Use `netlab config ifup -l pe_a` to reenable the link.
{{</note>}}

{{<cc>}}IP routing table with operational primary next-hop router{{</cc>}}
```
gw#show ip route | begin Gateway
Gateway of last resort is 172.16.1.2 to network 0.0.0.0

S*    0.0.0.0/0 [10/0] via 172.16.1.2, GigabitEthernet0/2
      10.0.0.0/32 is subnetted, 1 subnets
C        10.0.0.1 is directly connected, Loopback0
      172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
C        172.16.1.0/30 is directly connected, GigabitEthernet0/2
L        172.16.1.1/32 is directly connected, GigabitEthernet0/2
      172.17.0.0/16 is variably subnetted, 2 subnets, 2 masks
C        172.17.3.0/30 is directly connected, GigabitEthernet0/3
L        172.17.3.1/32 is directly connected, GigabitEthernet0/3
      192.168.0.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.0.0/24 is directly connected, GigabitEthernet0/1
L        192.168.0.1/32 is directly connected, GigabitEthernet0/1
```

{{<cc>}}IP routing table after the next-hop router failure{{</cc>}}
```
gw#show ip route | begin Gateway
Gateway of last resort is 172.17.3.2 to network 0.0.0.0

S*    0.0.0.0/0 [251/0] via 172.17.3.2, GigabitEthernet0/3
      10.0.0.0/32 is subnetted, 1 subnets
C        10.0.0.1 is directly connected, Loopback0
      172.16.0.0/16 is variably subnetted, 2 subnets, 2 masks
C        172.16.1.0/30 is directly connected, GigabitEthernet0/2
L        172.16.1.1/32 is directly connected, GigabitEthernet0/2
      172.17.0.0/16 is variably subnetted, 2 subnets, 2 masks
C        172.17.3.0/30 is directly connected, GigabitEthernet0/3
L        172.17.3.1/32 is directly connected, GigabitEthernet0/3
      192.168.0.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.0.0/24 is directly connected, GigabitEthernet0/1
L        192.168.0.1/32 is directly connected, GigabitEthernet0/1
```

### Revision History

2025-03-31
: * Mentioned BFD as an alternative to IP SLA
  * Mentioned RFC 9747 as a potential BFD-based solution if the upstream router doesn't want to participate in BFD (HT: Erik Auerswald)
  * Recreated the router configurations and printouts with IOSv release 15.6(1)T.
  * Added the command to shut down the PE_A interface when using _netlab_
