---
kb_section: OSPF_DV
minimal_sidebar: true
pre_scroll: true
title: Summary
#url: /kb/Internet/EIGRP_stub/10-dual-homed-sites/
---
Contrary to common wisdom, OSPF is not a pure link-state protocol. It uses link state algorithms within an area, but behaves almost like a distance vector protocol between the areas. The distinction could be considered purely academic if it would not introduce temporary routing instabilities into any multi-area OSPF network that does not use inter-area summarization.

In this article, you’ve seen how any OSPF design that has multiple ABRs in a non-backbone area can lead to temporarily incorrect IP routing within that area after an IP prefix is lost. Using default IOS OSPF parameters, the incorrect routing can persist for up to ten seconds, which is long enough to disrupt mission-critical applications and voice traffic.

You could tweak OSPF parameters (SPF and LSA throttle timers) to reduce the time span during which the Area Border Routers insert incorrect information into the affected area, or you could use OSPF route summarization or Type 3 (summary) LSA filters to prevent an IP prefix to reappear through the backbone area into the area from which it originated.
