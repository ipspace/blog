---
date: 2008-04-23 07:29:00.002000+02:00
tags:
- IP routing
- WAN
- ADSL
title: Almost-Dynamic Routing over ADSL Interfaces
url: /2008/04/almost-dynamic-routing-over-adsl.html
---
Recently I had to implement Internet access using ADSL as the primary link and ISDN as the backup link. Obviously the most versatile solution would use the techniques described in my [Small Site Multi-homing articles](/kb/Internet/), but the peculiarities of Cisco IOS implementation of the ADSL technology resulted in a much simpler solution.

IOS implementation of PPPoE links uses dialer interfaces. However, the "dialing" on these interfaces is activated as soon as the underlying PPPoE session is active (before the first *interesting* packet is routed to the interface). When the simulated dial-out occurs, the router starts PPP negotiations including the IPCP handshake, which usually results in an IP address assigned to the dialer interface. Net result: if the dialer interface has an IP address, the PPPoE session is obviously active (and vice versa).
<!--more-->
As my ADSL link and the ISDN backup used the same service provider (and very probably the same Radius servers), it made no sense to define additional IP SLA measurements to figure out if the service provider\'s network is operational; the IP route to the primary dialer interface is installed as soon as the interface is ready to route IP packets. The relevant parts of the router\'s configuration are included below.

``` {.code}
interface FastEthernet0
 description outside LAN
 no ip address
 ip virtual-reassembly
 duplex auto
 speed auto
 pppoe enable group global
 pppoe-client dial-pool-number 3
!
interface BRI0
 description ISDN line
 encapsulation ppp
 dialer pool-member 1
 isdn switch-type basic-net3
!
interface Dialer0
 description ADSL primary uplink
 ip address negotiated
 ip mtu 1492
 ip nat outside
 encapsulation ppp
 dialer pool 3
!
interface Dialer1
 description ISDN backup
 ip address negotiated
 ip nat outside
 dialer pool 1
!
track 100 interface Dialer0 ip routing
 delay down 10 up 10
!
ip route 0.0.0.0 0.0.0.0 Dialer0 10 track 100
ip route 0.0.0.0 0.0.0.0 Dialer1 250
```
