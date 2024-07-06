---
date: 2017-10-04 07:23:00+02:00
tags:
- design
- WAN
title: Reducing the Number of Transported Routes
url: /2017/10/reducing-number-of-transported-routes.html
---
One of my friends sent me this design challenge:

> Assume you're migrating from another WAN transport technology to MPLS. The existing network has 3000 routes but the MPLS carrier is limiting you to 1000 routes. How could you solve this with MPLS?

Personally, I think MPLS is a red herring.
<!--more-->
A better question would be "*how do you reduce the number of routes transported across your WAN network*" or "*how do you reduce the routing interaction with your MPLS service providers"* (particularly intriguing if you use more than one of them).

As always, there are several options and it's impossible to recommend the best one:

-   Readdressing is usually out of question (or at least too messy to try). It might also break numerous firewall rules and other hard-coded stuff... unless you automated everything, but then it wouldn't be hard to readdress, would it?
-   The usual answer would be to *summarize the routes*. The usual challenge is that you might not be able to do it (because random addressing). Furthermore, summarization is a lossy compression, and loss of forwarding information might result in black holes.
-   RFC 1925 states that there's nothing that cannot be solved with another layer of *abstraction.* In this case, we could use any one [or more](/2011/03/mplsvpn-over-gre-over-ipsec-does-it.html) of a half-dozen overlay technologies (IPsec, GRE, VXLAN, DMVPN, LISP...), or use an overlay technology sprinkled with unicorn dust (aka [SD-WAN](/2015/06/software-defined-wanwell-orchestrated.html)). The beauty of CE-to-CE tunnels is that they [totally eliminate the need for PE-CE routing](/2010/12/where-would-you-need-gre.html), and (when combined with VRFs) create independent routing domains, so you can use multiple SPs without the associated hassle.
-   Finally, you could go for a really exotic solution like Carriers-Carrier (using additional MPLS labels as the data-plane abstraction mechanism).
