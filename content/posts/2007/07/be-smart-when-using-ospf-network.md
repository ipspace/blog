---
date: 2007-07-12 08:07:00.001000+02:00
ospf_tag: config
tags:
- OSPF
title: Be Smart When Using the OSPF Network Statement
url: /2007/07/be-smart-when-using-ospf-network.html
---
For whatever reason, a lot of people have the impression that the wildcard bits in the OSPF network statement have to be the inverse of the interface subnet mask. For example, if you have configured **ip address 192.168.1.2 255.255.255.240** on an interface, they would enter **network 192.168.1.2 0.0.0.15** in the OSPF configuration (and use one network statement per interface).

In reality, the **network** statements work like simple IP **access-list**: whenever an interface IP address matches the **network** statement, the interface is put into the selected area. The Cisco IOS CLI [got better over the years](/2006/11/network-statements-in-ospf-process-are.html): the **network** statements are automatically sorted from most-specific to least-specific and (like with the access lists) the first match stops the search.
<!--more-->
In my network implementations, I use the network statements in three different ways:

-   If I have to assign a specific interface to an OSPF area, I would use the **ip ospf area** interface command. When forced to use the **network** statement, I would opt for **network *x.y.z.w* 0.0.0.0 area *n***;
-   If the area address ranges are nicely assigned (which also helps immensely when you have to start summarizing), you can use a single network statement to cover the whole area. If, for example, area 3 has address range 10.1.16.0/20, use **network 10.1.16.0 0.0.15.255 area 3**;
-   If the router has all interfaces in a single area, I would almost always use **network 0.0.0.0 255.255.255.255 area *area-id*** (unless there is an excellent reason that the OSPF process should not see some interfaces).
