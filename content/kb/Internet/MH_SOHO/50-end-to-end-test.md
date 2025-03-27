---
kb_section: MH_SOHO
minimal_sidebar: true
title: End-to-End Connectivity Test
alt_section: posts
---
After you’ve successfully implemented the tracking of the primary next-hop router’s availability, you might be tempted to improve the solution to track end-to-end connectivity through ISP A and switch to the backup ISP whenever your central site is not reachable through the primary ISP. In theory, the required configuration change should be minimal – you only have to change the destination IP address in the IP SLA definition:

{{<cc>}}Pinging a remote host{{</cc>}}
```
hostname GW
!
ip sla 100
 icmp-echo 172.18.0.6 source-interface GigabitEthernet0/2
 threshold 500
 timeout 1000
 frequency 3
ip sla schedule 100 life forever start-time now
```

Unfortunately, there's a serious problem with this setup when the path between GW and PE_A fails in a way that is not detected by the GW router (for example, there's a problem in an intermediate layer-2 switch):

* IP SLA fails, and the default route to PE_A is removed
* GW installs the default route to PE_B
* Pings are now sent from an IP address belonging to the ISP-A uplink onto a path going through the ISP-B.
* The redirected pings go through a NAT translation.
* You'll get an oscillating default route if the reverse NAT works and the ICMP responses reach the IP SLA measurement code. Otherwise, the IP SLA test will keep failing, and the default route to ISP A will not be installed even when the connectivity with PE A is restored.

To fix this problem, you have to configure a local policy routing (as the **ip sla** packets originate within the router, they are only affected by the **ip local policy**) that matches ICMP packets being sent from the GigabitEthernet0/2 interface (based on their IP address; the *PingISP\_A* access list) and forces them to be sent out through the correct interface toward the expected next hop:

{{<cc>}}Fix the oscillating routing with local PBR policy{{</cc>}}
```
ip local policy route-map LocalPolicy
!
ip access-list extended PingISP_A
 permit icmp host 172.16.1.1 host 172.18.0.6
!
route-map LocalPolicy permit 10
 match ip address PingISP_A
 set ip next-hop 172.16.1.2
 set interface GigabitEthernet0/2
```

{{<note info>}}
The complete configuration of the gateway router is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/gw-local-policy.cfg).
{{</note>}}

### Coping with the Central Site Failure

You can extend the concepts presented in this section even further if you want to. For example, if the central site is not reachable through either ISP (it might be down), retaining ISP A as the primary ISP could make more sense. You would thus need to:

* Track the central site’s availability through both ISPs.
* Configure a reliable static default route for both ISPs (using a higher administrative distance on the backup one).
* Add a third (last-resort) default route pointing to ISP A.
* Add an even worse default route pointing to ISP B (in case the interface toward ISP A fails).

The relevant parts of the router configuration are included in the following listing (the [complete configuration is on GitHub](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/gw-dual-sla.cfg)), and its interpretation is left as an exercise for the reader.

{{<cc>}}GW router tracking central site availability through both ISPs{{</cc>}}
```
hostname gw
!
ip dhcp pool LAN
 network 192.168.0.0 255.255.255.0
 default-router 192.168.0.1 
!
track 100 ip sla 100 reachability
 delay down 10 up 20
!
track 101 ip sla 101 reachability
 delay down 10 up 20
!
interface GigabitEthernet0/1
 description gw -> [h1,h2] [stub]
 ip address 192.168.0.1 255.255.255.0
 ip nat inside
!
interface GigabitEthernet0/2
 description gw -> pe_a
 ip address 172.16.1.1 255.255.255.252
 ip nat outside
!
interface GigabitEthernet0/3
 description gw -> pe_b
 ip address 172.17.3.1 255.255.255.252
 ip nat outside
!
ip local policy route-map LocalPolicy
!
ip nat inside source route-map ISP_A interface GigabitEthernet0/2 overload
ip nat inside source route-map ISP_B interface GigabitEthernet0/3 overload
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2 172.16.1.2 10 name ISP_A track 100
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/3 172.17.3.2 11 name ISP_B track 101
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2 172.16.1.2 250 name ISP_A_FB
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/3 172.17.3.2 251 name ISP_B_FB
!
ip access-list extended PingISP_A
 permit icmp host 172.16.1.1 any
ip access-list extended PingISP_B
 permit icmp host 172.17.3.1 any
!
ip sla 100
 icmp-echo 172.18.0.6 source-interface GigabitEthernet0/2
 threshold 500
 timeout 1000
 frequency 3
ip sla schedule 100 life forever start-time now
ip sla 101
 icmp-echo 172.18.0.6 source-interface GigabitEthernet0/3
 threshold 500
 timeout 1000
 frequency 3
ip sla schedule 101 life forever start-time now
!
route-map ISP_A permit 10
 match interface GigabitEthernet0/2
!
route-map ISP_B permit 10
 match interface GigabitEthernet0/3
!
route-map LocalPolicy permit 10
 match ip address PingISP_A
 set ip next-hop 172.16.1.2
!
route-map LocalPolicy permit 20
 match ip address PingISP_B
 set ip next-hop 172.17.3.2
```

### Surviving Multiple Failures

The above solution survives the failure of:

*  A single uplink (one of the IP SLA measurements fails)
*  The central site (both IP SLA measurements fail, but we have backup floating static routes)
*  The physical link between GW and PE-A (the interface on GW goes down, and even the floating static route is removed)

It does not, however, survive the failure of the central site and the path between GW and PE-A. If you want to make your solution even more reliable[^JST], you could combine IP SLA checks of central site reachability with IP SLA checks of next-hop reachability and use the following hierarchy of default routes:

* Route to PE-A based on reachability of the central site
* Route to PE-B based on reachability of the central site
* Route to PE-A based on next-hop reachability (using IP SLA or BFD)
* Route to PE-B based on next-hop reachability (using IP SLA or BFD)
* Floating static route to PE-A based on interface state
* Floating static route to PE-B as the absolute last resort

[^JST]: Keeping in mind we're leaving the sane world and slowly entering the Job Security territory

### Revision History

2025-03-31
: * Recreated the router configurations and printouts with IOSv release 15.6(1)T.
  * Added the _surviving multiple failures_ scenario at the end of this section. 