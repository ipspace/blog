---
title: Multi-Chassis Link Aggregation
layout: custom
minimal_sidebar: true
sidebar_box: rb
deep_dive:
- page: /posts/2022/06/mlag-deep-dive-mac-learning.md
  title: Dynamic MAC Learning
- page: /posts/2022/06/mlag-deep-dive-flooding.md
  title: Layer-2 Flooding
- page: /posts/2022/06/mlag-active-active-layer3.md
  title: Active-Active Layer-3 Forwarding
- page: /posts/2022/09/mlag-deep-dive-vxlan-fabric.md
  title: Connecting MLAG Cluster to VXLAN Fabric
- title: Using EVPN/VXLAN with MLAG Clusters
  page: /posts/2022/11/mlag-vxlan-evpn.md
- title: Replacing Peer-Link with VXLAN Fabric
- title: Running Routing Protocols over MLAG Links
  page: /posts/2022/12/mlag-routing.md
# BFD challenge: micro-BFD or BFD across VLANs?
# https://blog.ipspace.net/2022/06/mlag-active-active-layer3.html#1316
# - title: Combining MLAG with BFD
---
Multi-Chassis Link Aggregation (MLAG) is a solution that allows you to terminate a link aggregation group (sometimes also known as *etherchannel*) on multiple devices. 

It's often used to implement redundant server connections; it was also popular in the days of layer-2 fabrics built with Spanning Tree Protocol (STP). The latter use case is mostly obsolete in the VXLAN/EVPN world.

### What Is Multi-Chassis Ling Aggregation?

{{<series-listing tag="overview" weight="1">}}

{{<series-listing tag="deepdive" title="Technology Deep Dive" soon="deep_dive">}}

### Design Guidelines

{{<series-listing tag="design">}}

### MLAG Implementations

{{<series-listing tag="implement">}}

### Using MLAG on Server-to-Network Links

{{<series-listing tag="server">}}

### Videos

{{<series-listing tag="video">}}

