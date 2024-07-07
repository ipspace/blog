---
title: "Worth Reading: Taming the BGP Reconfiguration Transients"
date: 2023-11-01 07:41:00
tags: [ BGP, worth reading ]
---
Almost exactly a decade ago I [wrote about a paper](/2013/10/ibgp-migrations-can-generate-forwarding/) describing how IBGP migrations can cause forwarding loops and how one could [reorder BGP reconfiguration steps to avoid them](https://inl.info.ucl.ac.be/system/files/bgpmig_final.pdf).

One of the paper's authors was [Laurent Vanbever](https://vanbever.eu/) who moved to ETH Zurich in the meantime where his group keeps producing great work, including the [Chameleon tool](https://nsg.ee.ethz.ch/publications/2023-01-01-taming-the-transient-while-reconfiguring-bgp-20-500-11850-612650/) ([code on GitHub](https://github.com/nsg-ethz/Chameleon)) that can [tame transient loops while reconfiguring BGP](https://www.manrs.org/2023/10/taming-the-transient-while-reconfiguring-bgp/). Definitely something worth looking at if you're running a large BGP network.


