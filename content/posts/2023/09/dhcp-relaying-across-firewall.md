---
title: "DHCP Relaying Across a Firewall"
date: 2023-09-12 06:36:00
tags: [ DHCP, firewalls ]
series: dhcp-relay
---
Chinar Trivedi wanted to know what happens when you insert a firewall in the DHCP data path ([original question](https://blog.ipspace.net/2023/05/dhcp-redundant-vrf-relay.html#1833).

**TL&DR:** Nothing much, but that does not mean you should.

Now for the details:
<!--more-->
-   DHCP communication between a client and a relay (or a directly connected server) is somewhat weird from the firewall's session-tracking perspective. You might get it to work, but it's probably not worth the hassle. Insert a DHCP relay in the forwarding path to protect the DHCP server.
-   [DHCP communication between a DHCP relay and a DHCP server](/2023/03/dhcp-relay-process.html) is a UDP transaction using the BOOTP port. You should be fine if your firewall rules allow the DHCP relays to send UDP packets to the BOOTP port on the DHCP servers (and the reverse traffic). 

Want to go even further? You could put the DHCP traffic into a separate VRF; most decent network devices support [inter-VRF DHCP forwarding](/2023/04/netlab-evpn-dhcp-relay.html).

Finally, Chinar wondered, "*What would Ivan do?"*

I find the idea slightly ridiculous. What exactly are you trying to protect?

-   The DHCP server? DHCP relays (edge switches) must be some of the most trustworthy devices in your infrastructure. If someone breaks into one of them, and you're running EVPN without severe route filters on the route reflectors, it's game over anyway.
-   The switches? You have a bigger problem on your hands if someone breaks into the DHCP server, and the bogus DHCP replies crash your switches. Scream at your vendor.
-   The switches' control plane? Breaking into a DHCP server and using it for lateral moves could be interesting, but it's easy to stop -- configure an ACL on the port to which the DHCP server is connected and allow only UDP traffic from the BOOTP port.
-   The integrity of the DHCP messages? Do you mean those things critical to the proper operation of your compute infrastructure that are nonetheless sent around unencrypted? The only way (that I can see) to do that is to connect a DHCP server directly to the client segment and to use the DHCP guard on the physical or virtual switches.

**Long story short**: wanting to make the DHCP process more secure is perfectly reasonable, but a firewall is probably the wrong tool for the job.
