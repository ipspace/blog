---
title: "Reliable ECMP with Static Routing"
date: 2023-09-10 11:00:00
tags: [ IP routing ]
draft: True
---
I'm trying to find information about "eibgp". I found something in your website but the video link is broken (https://blog.ipspace.net/2013/06/eibgp-load-balancing.html).
<!--more-->
I'm interested about that because still in my DC, I would like to load balance outgoing trafic to my both wan routers.
Remember you my design :
- I have few pub subnets with community/local pref configured on nexus to prioritize some on one nexus and some on other so in input
- 2x nexus9k as wan router connected between us with a Po
- these 2x nexus9k are connected in ebgp to the same provider
- these 2x nexus9k have an ibgp link between them
- there is a VRRP on inside
- no VPC

under these nexus (so internal side), I have a firewall cluster (forcepoint) with static routing : gateway points to the VRRP VIP Nexus

My issue is : 
- ingest trafic is Ok as it is dispatched between both nexus
BUT
- for output trafic, as trafic goes to VIP, it outputs from the nexus primary VRRP only.. so we use only one link to go out our DC instead of using all the bandwidth available

I thought to a solution in changing settings in firewall => ECMP to physical interfaces (IP) of nexus (so no VIP at all as gateway). We checked it and it seems easy but need to be tested.
Or maybe with eiBGP, but I'm not sure about this solution and where to put it and how + I read some comments about possible loop issue...

Do you have any advice for me about this ?

---

Using static routes pointing to physical IP addresses is not so good from the resiliency perspective.

I would use two VRRP groups (each one “owned” by one of the switches) and have to static routes pointing to the two VRRP addresses.

Ideally one would run OSPF with the firewall (even better: EBGP) and advertise the default route from both switches.

---

The primary EIBGP use case is in MPLS/VPN WAN networks, and Cisco would like to use segment routing and Egress Peer Engineering anyway.