---
date: 2007-10-02 07:31:00+02:00
ospf_tag: config
tags:
- OSPF
title: OSPF Router-Id Does Not Change When the Interface IP Address Changes
url: /2007/10/ospf-router-id-does-not-change-when.html
---
The venerable rules used to establish OSPF router ID on Cisco IOS are all over the Internet:

-   Take the highest IP address of all loopback interfaces configured on the router when the OSPF process is started.
-   If there is no loopback interface, take the highest IP address of an operating interface.

In the old days, when Cisco believed that the router ID had to match an interface address, this also implied that the router ID would have changed if the interface IP address changed (and we told the students that you have to use loopback interfaces to make your network stable, as the OSPF process would restart if the interface giving the router ID went down).
<!--more-->
Most of these *"wisdoms"* are no longer true:

* The OSPF router ID is a 32-bit value that must be unique (that's all the OSPF RFC has ever asked for).
* It just happens to be taken from an interface address when the OSPF process is started.
* You can configure it to any value with the **router-id *A.B.C.D*** router configuration command.

The new behavior, while making your network more stable, can also bring unexpected side effects: if you don't use the **router-id** command and misconfigure an interface IP address (resulting in duplicate router IDs), correcting the interface IP address will not fix the problem. You must also reset the OSPF process with the **clear ip ospf *pid* process** command.
