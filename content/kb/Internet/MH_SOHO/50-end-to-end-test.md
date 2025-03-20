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
 icmp-echo 172.29.0.1 source-interface Serial0/0/0
 timeout 200
 frequency 10
ip sla schedule 100 life forever start-time now
```

In most cases, that’s all you have to do. As the ICMP echoes sent to the central site come from an IP address belonging to ISP A (the IP address configured on Serial 0/0/0 in the example), it’s improbable that you would get a return packet if ISP A has problems. However, the return packet might still reach your router under rare circumstances (misconfigured access lists or one-way connectivity in ISP A). The results are astonishing:

* When the pings through ISP A (the primary default route) fail, the router removes the primary default route and installs the backup default route through ISP B.
* Pings are now sent from an IP address belonging to ISP A onto a path going through ISP B.
* If there is a return path from the central site to the IP address sending the ICMP packets, the central site will again appear reachable, and the primary default route will be reinstalled (resulting in connectivity loss).
* Due to renewed connectivity loss, the router keeps oscillating between the two default routes.

{{<cc>}}Oscillating routing{{</cc>}}
```
GW#debug track
07:15:09: Track: 100 Change #32 rtr 100, reachability Up->Down
07:15:09: %HA_EM-6-LOG: ISP_1_down: ping to 172.29.0.1 from Serial 0/0/0 failed
07:15:19: Track: 100 Up change delayed for 20 secs
07:15:39: Track: 100 Up change delay expired
07:15:39: Track: 100 Change #33 rtr 100, reachability Down->Up
07:15:39: %HA_EM-6-LOG: ISP_1_up: 172.29.0.1 is reachable
07:15:49: Track: 100 Change #34 rtr 100, reachability Up->Down
07:15:49: %HA_EM-6-LOG: ISP_1_down: ping to 172.29.0.1 from Serial 0/0/0 failed
07:15:59: Track: 100 Up change delayed for 20 secs
```

To fix this (admittedly rare) problem you have to configure a local policy routing (as the **ip sla** packets originate within the router, they are only affected by the **ip local policy**) that matches ICMP packets being sent from the Serial0/0/0 interface (based on their IP address; the *PingISP\_A* access list) and forces them to be sent out through the same interface with the **set interface** configuration command:

{{<cc>}}Fix the oscillating routing with local PBR policy{{</cc>}}
```
ip local policy route-map LocalPolicy
!
ip access-list extended PingISP_A
 permit icmp host 172.16.1.1 host 172.29.0.1
!
route-map LocalPolicy permit 10
 match ip address PingISP_A
 set interface Serial0/0/0
```

If you want to, you can extend the concepts presented in this section even further. For example, if the central site is not reachable through either ISP (it might be down), retaining ISP A as the primary ISP could make more sense. You would thus need to track the central site’s availability through both ISPs and configure a reliable static default route for both of them (the backup one with a higher administrative distance, of course) with a third (last-resort) default route pointing to ISP A. The complete configuration is included in the following listing, and its interpretation is left as an exercise for the reader.

{{<cc>}}GW router tracking central site availability through both ISPs{{</cc>}}
```
hostname GW
!
ip cef
!
ip dhcp pool LAN
   network 192.168.0.0 255.255.255.0
   default-router 192.168.0.1
!
ip sla 100
 icmp-echo 172.29.0.1 source-interface Serial0/0/0
 timeout 200
 frequency 3
ip sla schedule 100 life forever start-time now
!
ip sla 101
 icmp-echo 172.29.0.1 source-interface Serial0/0/1
 timeout 500
 frequency 3
ip sla schedule 101 life forever start-time now
!
track 100 rtr 100 reachability
 delay down 10 up 20
!
track 101 rtr 101 reachability
 delay down 10 up 20
!
interface FastEthernet0/0
 ip address 192.168.0.1 255.255.255.0
 ip nat inside
!
interface Serial0/0/0
 description *** Link to ISP 1 ***
 ip address 172.16.1.1 255.255.255.252
 ip nat outside
!
interface Serial0/0/1
 description *** Link to ISP 2 ***
 ip address 172.17.3.1 255.255.255.252
 ip nat outside
!
ip local policy route-map LocalPolicy
!
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A track 100
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 11 name ISP_B track 101
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 250 name ISP_A_FB
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 251 name ISP_B_FB
!
!
ip nat inside source route-map ISP_A interface Serial0/0/0 overload
ip nat inside source route-map ISP B interface Serial0/0/1 overload
!
ip access-list extended PingISP_A
 permit icmp host 172.16.1.1 host 172.29.0.1
ip access-list extended PingISP_B
 permit icmp host 172.17.3.1 host 172.29.0.1
!
route-map ISP_A permit 10
 match interface Serial0/0/0
!
route-map ISP_B permit 10
 match interface Serial0/0/1
!
route-map LocalPolicy permit 10
 match ip address PingISP_A
 set interface Serial0/0/0
!
route-map LocalPolicy permit 20
 match ip address PingISP_B
 set interface Serial0/0/1
!
!
event manager applet ISP_A_down
 event track 100 state down
 action 1.0 syslog msg "ping to central site from Serial 0/0/0 failed"
event manager applet ISP_A_up
 event track 100 state up
 action 1.0 syslog msg "central site is reachable"
event manager applet ISP_B_down
 event track 101 state down
 action 1.0 syslog msg "ping to central site from Serial 0/0/1 failed"
event manager applet ISP_B_up
 event track 101 state up
 action 1.0 syslog msg "central site is reachable"
!
end
```
