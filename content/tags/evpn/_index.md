---
title: EVPN
page_title: Ethernet VPN (EVPN)
minimal_sidebar: true
layout: custom
---
{{<quote source="ChatGPT trying (and failing) to explain EVPN">}}
EVPN, or Ethernet Virtual Private Network, is like a smart system that helps computers and devices in a network talk to each other better. It's like having a super organized mail system where each computer has its own address, and EVPN makes sure messages get to the right place quickly and safely. So, it's kind of like a traffic manager for information on a computer network, making everything run smoothly and securely.{{</quote>}}

### {{<plushy confused>}}What Is EVPN? {#101}

Before going into the technical details, let's start with the basics: What is EVPN, how does it work, and where can you use it?

{{<series-listing tag="intro" weight="sure">}}

### {{<plushy master>}}EVPN Designs {#designs}

EVPN was designed to be used in an IBGP environment on top of an IGP. With the eruption of *EBGP as better IGP* hype, many vendors tried to adapt EVPN to an environment running EBGP instead of OSPF. We covered typical EVPN designs in these blog posts:

{{<series-listing tag="design">}}

### {{<plushy magic>}}EVPN Implementation Details {#mlag}

There are tons of tiny little things that can go wrong when you try to deploy EVPN. I documented them as I stumbled upon them:

{{<series-listing tag="details">}}

### {{<plushy idea>}}Beyond VXLAN {#mpls}

While EVPN is often used with VXLAN today, it was designed to work with the MPLS data plane, resulting in a few quirks:

{{<series-listing tag="mpls">}}

### {{<plushy angry>}}EVPN Rants {#rants}

Some vendors' marketing engineers (or Senior Directors) can't stand anyone telling them their implementation might be suboptimal, going to great lengths to prove to themselves they're right, and generating beautiful fodder for rants.

{{<series-listing tag="rant">}}

### {{<plushy master>}}Videos {#videos}

You can watch numerous videos from the [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar without an ipSpace.net account:

{{<series-listing tag="video">}}

### {{<plushy happy>}} What Others Wrote About EVPN {#read}

{{<series-listing tag="read">}}
{{<series-listing title="Other EVPN Blog Posts" notag="yes">}}
