---
date: 2009-05-04 07:14:00.004000+02:00
tags:
- firewall
- security
- QoS
title: Zone-based Traffic Policing
url: /2009/05/zone-based-traffic-policing/
---
The zone-based firewall uses security **policy-maps** to specify how the flows between zones should be handled based on their traffic classes. The obvious actions that you can use in the security policy are **pass**, **drop** and **inspect**, but there's also the **police** action and one of the readers sent me an interesting question: "why would you need the **police** action in the security policy if you already have QoS policing".
<!--more-->
The difference between interface service policy and inter-zone security policy is in the traffic aggregation: the interface service policy works on traffic classes entering or leaving a single interface and the inter-zone policy works on aggregate traffic between zones, including the return traffic if you've used the **inspect** command to configure stateful inspection of the traffic class.

For example, you could limit the amount of HTTP traffic between your internal clients and your DMZ segment to prevent the internal users from overloading your public web servers.

{{<note warn>}}The inter-zone policing algorithm is pretty aggressive. You have to specify high rates and burst sizes, otherwise you can kill all TCP traffic.{{</note>}}