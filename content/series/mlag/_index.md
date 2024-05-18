---
title: Multi-Chassis Link Aggregation
layout: custom
minimal_sidebar: true
sidebar_box: sw
soon_failure:
- title: LAG Member Failures in EVPN/VXLAN Environment
  page: /posts/2024/05/mlag-evpn-rerouting.html
# soon_deep:
# BFD challenge: micro-BFD or BFD across VLANs?
# https://blog.ipspace.net/2022/06/mlag-active-active-layer3.html#1316
# - title: Combining MLAG with BFD
---
Multi-Chassis Link Aggregation (MLAG) is a solution that allows you to terminate a link aggregation group (sometimes also known as *etherchannel*) on multiple devices. 

It's often used to implement redundant server connections; it was also popular in the days of layer-2 fabrics built with Spanning Tree Protocol (STP). The latter use case is mostly obsolete in the VXLAN/EVPN world.

### {{<plushy confused>}}What Is Multi-Chassis Link Aggregation?

{{<series-listing tag="overview" weight="1">}}

{{<series-listing tag="deepdive" title="Technology Deep Dive" soon="soon_deep" weight="1">}}

{{<series-listing tag="evpn" title="Using MLAG Clusters with VXLAN and EVPN" soon="soon_evpn">}}

### {{<plushy master>}}Design Guidelines

{{<series-listing tag="design">}}

### {{<plushy magic>}}MLAG Implementations

{{<series-listing tag="implement">}}

### Failure Scenarios

{{<series-listing tag="failure" soon="soon_failure">}}

### Using MLAG on Server-to-Network Links

{{<series-listing tag="server">}}

### Videos

{{<series-listing tag="video">}}

