---
title: EIGRP
page_title: Enhanced Interior Gateway Routing Protocol (EIGRP)
minimal_sidebar: true
layout: custom
---
EIGRP was the best choice for an interior gateway protocol in late 1990s -- it was fast, efficient, and easy to deploy. OSPF and IS-IS implementations improved in the intervening 30 years, slowly turning EIGRP into a forgotten technology.

On a more serious note, I wouldn't deploy EIGRP in new network designs for compatibility reasons (no major networking vendor apart from Cisco implemented it), and I'd use BGP in designs where a single router has to deal with hundreds of adjacent routers (the only scenario where EIGRP still outshines OSPF and IS-IS).

While the ultimate sources of EIGRP wisdom remain the [EIGRP Network Design Solutions](https://www.ciscopress.com/store/eigrp-network-design-solutions-9781578701650) Cisco Press book and [RFC 7868](https://datatracker.ietf.org/doc/html/rfc7868), you might want to read these articles and blog posts describing EIGRP implementation details and deployment guidelines.

{{<series-listing title="Blog Posts I Forgot to Categorize" notag="yes">}}

### {{<plushy confused>}}The Basics

{{<series-listing tag="basic">}}

### {{<plushy master>}}Implementation Details

{{<series-listing tag="details">}}

### {{<plushy magic>}}EIGRP Deployment Scenarios

{{<series-listing tag="deploy">}}
