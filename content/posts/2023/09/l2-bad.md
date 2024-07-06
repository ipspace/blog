---
title: "Repost: L2 Is Bad"
date: 2023-09-22 06:19:00
tags: [ switching, data center, design ]
---
Roman Pomazanov documented his thoughts on the beauties of large layer-2 domains in a LinkedIn article and allowed me to repost it on ipSpace.net blog to ensure it doesn't disappear

---

First of all: **"L2 is a single failure domain"**, a problem at one point can easily spread to the entire datacenter.
<!--more-->
The most common problem is broadcast storms and malformed broadcast frames. As representative example of what it can lead to, recall a case from 2018 on the network of a large American provider Centurylink, when a problem in a single L2-domain suspended the 911 service in several states. More details can be found [in an FCC document](https://docs.fcc.gov/public/attachments/DOC-359134A1.pdf).

Single L2 makes scaling difficult, the larger the datacenter - the more of broadcast traffic on the network.

Yes, there are storm control mechanisms, but they drop everything indiscriminately. It is impossible to understand where legitimate traffic is and where it is not. ARP requests stop working, etc

Other than that, "problems" on L2 are hard to troubleshoot, and once something has happened it's usually too late.

Another disadvantage is the lack of spoofing protection mechanism, a MAC-address can be "accidentally" assigned to the one already used somewhere and we will get a situation with MAC-address flapping - and as a consequence disabling the MAC learning mechanism in a particular VLAN on modern datacenter switches.

### Is Using EVPN/VXLAN the Solution?

EVPN certainly reduces the amount of broadcast traffic and has some sort of loop protection mechanism, but nevertheless L2 remains L2. In addition:

-   EVPN will not protect against malformed broadcast packets;
-   Implementation of VXLAN/EVPN in the network operating system code is much more complex than the implementation of simple routing. As a consequence, it has a larger code base, and as a consequence, it increases the potential number of bugs;
-   When dealing with "new" vendors of network hardware, it is not clear in advance what difficulties in operation we will encounter;
-   In spite of the fact that EVPN is an open standard, all the leading companies refrain to interop vendors within the framework of a single vendor - it is not clear who to blame when the problem is "at the junction". Because of this, there is a lock-in to a single vendor within a single site. I'd love to hear stories about EVPN/VXLAN inter-vendor control-plane ;)
-   VXLAN is still "insecure", segmentation of what's inside is impossible at the switch level - we "can't see" what's in the tunnel. We need to strip VXLAN headers "somewhere" and filter traffic (if necessary).
-   Ethernet wrapped in UDP, wrapped in IP, wrapped in another Ethernet is complicated to troubleshoot. CRC errors in the original frame "fly" through the fabric, are not dropped anywhere and reach the destination in their original form. (Of course, if cut-through switches are used in the fabric).

### What Else Is on Offer?

Use pure L3 routing. No overlay in the fabric . All overlay should be inside the servers - in SDNs.

By only needing routing, we reduce the "complexity" of the network - thus reducing the number of potential problems. Fewer features means fewer places where problems can occur.

It is much easier to realize interaction between devices of different vendors using only routing than EVPN - we are not tied to the vendor.

The ideal scheme is generally L3 up to the server where the services are located. The scheme covers fault tolerance, bandwidth extensibility, and scalability - the service (e.g. web site) hangs on a dummy/loopback interface, IP-address is announced to the physical network by some dynamic routing protocol (BGP as a defacto standard) - through each link, for example, and the announcements go upstairs.

---

Unfortunately it's (still) [impossible to implement such a simple design with network virtualization software from a major enterprise vendor](/2020/02/do-we-need-complex-data-center-switches.html).
