---
kb_section: EIGRP_stub
minimal_sidebar: true
title: Summary
url: /kb/Internet/EIGRP_stub/99-summary/
---
In this article, you’ve seen how you can use the EIGRP stub router functionality (introduced in Cisco IOS release 12.0T and 12.1) to decrease bandwidth utilization on slow links and dramatically improve EIGRP convergence times and its robustness. This functionality is easiest to deploy in stub sites (remote offices) with a single router.

As soon as you’re deploying more than one router on the stub site, each one of them could potentially become a transit router. Cisco has introduced the **leak-map** enhancement to the **eigrp stub** configuration command in IOS release 12.3(11)T that allows you to specify which EIGRP routes a stub router should leak to its neighbor (or, in network design terms, for which IP prefixes the stub router should act as a transit router). Proper deployment of the **leak-map** feature guarantees correct routing even in various failure scenarios, while retaining all the benefits introduced with the EIGRP stub router concept.
