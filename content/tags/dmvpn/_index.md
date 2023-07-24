---
title: DMVPN
page_title: Dynamic Multipoint VPN (DMVPN)
minimal_sidebar: true
layout: custom
---
DMVPN is an old[^OLD] Cisco-proprietary technology that combines NHRP, IPsec, IKEv2 and multipoint GRE tunnels to build dynamically-provisioned multi-access VPNs.

[^OLD]: As in: created around 2010. For more details, listen to the _[History of DMVPN with Mike Sullenberger](https://labs.ripe.net/history-of-networking/dmvpn-mike-sullenberger/)_.

The easiest way to master DMVPN is to watch the [ipSpace.net DMVPN webinars](https://www.ipspace.net/Roadmap/VPN_webinars), and every now and then someone still finds them somewhat useful:

{{<series-listing tag="training" weight="yes">}}

I also wrote dozens of DMVPN-related blog posts. Hope you'll enjoy them!

### {{<plushy confused>}}The Basics

DMVPN always relies on a hub-and-spoke topology, but enables direct communication between spokes (Phase-2 DMVPN) and simplified routing with NHRP redirects (Phase-3 DMVPN).

{{<series-listing tag="basics" weight="yes">}}

### {{<plushy master>}}Routing Protocols in DMVPN Networks

Routing protocols face significant challenges in DMVPN networks due to very large number of directly-connected neighbors, with EIGRP faring better than OSPF, and BGP being the only viable solution in deployments with a very large hub-to-spoke ratio.

{{<series-listing tag="routing">}}

### {{<plushy magic>}}Typical DMVPN Designs

{{<series-listing tag="design">}}

### DMVPN Deployment Guidelines

{{<series-listing tag="deploy">}}

### {{<plushy confused>}}Integration with Other Network Technologies

{{<series-listing tag="integrate">}}

### DMVPN Alternatives

{{<series-listing tag="alternative">}}

### {{<plushy confused>}}Quirks and Implementation Details

I wrote numerous blog posts documenting DMVPN quirks while preparing the materials for the DMVPN webinars. Most of these blog posts were written in early 2010s and might no longer be relevant.

{{<series-listing tag="quirk">}}

### Other Blog Posts Vaguely Related to DMVPN

{{<series-listing tag="other">}}

{{<series-listing title="Blog Posts I Forgot to Categorize" notag="yes">}}
