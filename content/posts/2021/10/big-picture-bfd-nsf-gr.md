---
date: 2021-10-28 07:25:00+00:00
distributed-systems_tag: device
high-availability_tag: external
series:
- ha-switching
- distributed-systems
tags:
- networking fundamentals
- high availability
title: 'Big Picture: BFD, Non-Stop Forwarding, and Graceful Restart'
---
_We have school holidays this week, so I'm reposting wonderful comments that would otherwise be lost somewhere in the page margins. Today: Erik Auerswald's [excellent summary of BFD, NSF, and GR](/2021/10/graceful-restart-bfd.html#803)_.

---

I'd suggest to step back a bit and consider the bigger picture: What is BFD good for? What is GR/NSF/NSR/SSO good for?

BFD and GR/NSF/NSR/SSO have different goals: one enables quick fail over, the other prevents fail over. Combining both promises to be interesting.
<!--more-->
Reliably and quickly detecting a forwarding failure is helpful when there is a different path to fail over to. When there is no alternative path, quick failure detection seems less important.

BFD implementations often combine data plane (BFD echo mode) and control plane (BFD session) failure detection and thus assume a shared fate between data plane and control plane.

GR and NSF are based on the assumption that the data plane can still function although the control plane has (temporarily) failed.

NSR/SSO shall hide control plane failures by (more or less) transparently failing over to a different processor.

Some combinations of GR/NSF/NSR/SSO can help to mask temporary control plane failures that do not affect the data plane.

NSF+GR allows forwarding despite temporary control plane failures. Likewise NSF+NSR/SSO.

{{<note>}}IMHO NSR/SSO should be implemented completely transparently and always be enabled when there are two or more control plane processors. Why even have hardware redundancy for the control plane when it does not work well enough to enable unconditionally?{{</note>}}

When routers are not able to quickly react to topology changes (think (multiple) full Internet BGP tables with weak routers), GR seems useful to avoid churn and cascading failures.

BFD is intended to reliably and timely detect forwarding failures. Now what should one do with this information? Continue forwarding down the known failed path with the help of something like GR/NSF/NSR/SSO? Why detect the forwarding failure at all, if it is to be ignored anyway?

How can BFD be used with complex routers where the data plane can still function although the control plane has failed? How to handle a complex router with redundant control plane, e.g., two route processor modules? One idea could be to use BFD echo mode in the data plane with a short detection interval and a control plane session with a long detection interval (or no BFD control plane session at all). Combined with an additional path to fail over to if a data plane failure is detected this can help, but it does add a whole lot of complexity, which might reduce reliability in practice.

A different, simpler approach to network redundancy would be to have less complex routers without NSF/NSR/SSO, but more of those to build redundant paths. Then quick and reliable failure detection, e.g., with BFD, can be used to fail over whenever a data plane or control plane failure is detected.

---

Not surprisingly, smart network designs (example: leaf-and-spine fabric designs by Arista) follow exactly these rules:

* NSF and GR on leaf switches to support hitless software upgrades.
* Simple (non-redundant) control plane on spine switches with BFD between leaf- and spine switches.
