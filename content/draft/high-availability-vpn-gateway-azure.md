---
title: "Implementing High-Availability VPN Gateway in Public Cloud"
# date: 2021-03-22 16:39:00
tags: [ Azure, cloud ]
draft: True
intro: |
  Describe the crazy idea of using two VPN gateways with a load balancer in front of them
---
With the above approach we have bypassed the "super fast" fail-over time of three minutes (at least). We knew about the limitations of this scenario (and the cost impact) of course, but also it resolved the performance issues we have faced with VPN GW.

On a side note I just wanted to give you the details behind the PAT thing and Azure Load Balancer so its a bit more clear:
Two Web Servers on-premises running a dummy HTML that shows the status healthy.
The NVA's have IPSEC tunnels towards on-premises with BGP configured.
The NVA's are not part of the same cluster, they are two individual VM's. Firewall is disabled fully in this case, we just want purely a IPSEC router.
The Azure Load Balancer points towards port 9090 on the internal IP addresses of the NVA's.
The PAT is configured for the internal interface of the NVA (port 9090) to point to the on-premise web server, each NVA points to different web server.
Standard HTTP probe is configured on the Azure Load Balancer.
Create UDR's that point to the Load Balancer IP.
Use the right distribution configuration on the LB.
I know there are some limitations and disasters that can come with this, but they can be carefully addressed during the design and depending on the scenario of course. And sorry to keep on spamming your mailbox like this, I started to behave like my wife over Telegram.
