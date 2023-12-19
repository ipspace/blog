---
date: 2007-06-28 07:42:00.001000+02:00
ospf_tag: default
tags:
- OSPF
- IP routing
title: 'OSPF Default Route: Design Scenarios'
url: /2007/06/ospf-default-route-design-scenarios.html
---
Here's an interesting OSPF-related question I got::

> "Which one is better: **default-information originate** or **default-information originate always**?"

As always, the answer is *it depends*. If your OSPF edge routers have external default routes (for example, static default routes toward the Internet, see the next diagram), you\'d want them to announce the default route only when they have a default themselves (otherwise, they would attract the traffic and then blackhole it). In this case, you'd use **default-information originate**.
<!--more-->
{{<figure src="/2007/06/OSPF_A.jpg">}}

If you use something other than OSPF as the core routing protocol of your network (as shown in the next diagram), then you'd want the core routers to announce the default route into OSPF to attract the traffic from the edges regardless of whether they have the default route themselves or not. In this scenario, you'd use **default-information originate always**.

{{<figure src="OSPF_B.jpg">}}

{{<note>}}BGP is almost always the core routing protocol of Service Provider networks. You can also use it to make a large enterprise network scalable.{{</note>}}

Last but not least, in the OSPF+BGP scenario, you might want a core router to announce a default route only if it has at least some non-OSPF routes (to prevent an isolated core router from attracting and blackholing the traffic). The command to use is **default-information originate always route-map *name***, which would generate a default route into OSPF only if at least one prefix from the IP routing table matches the specified route map.
