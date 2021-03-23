---
title: "Using Unequal-Cost Multipath to Cope with Leaf-and-Spine Failures"
# date: 2021-03-22 16:15:00
tags: [ fabric, design ]
draft: True
intro: |
  Scott suggested to use UCMP to get around link and node failures in leaf-and-spine fabrics
---
Scott O'Brien (<scott@scottyob.com>) submitted the following comment to <https://blog.ipspace.net/2021/02/does-ucmp-make-sense.html>.

------------------------------------------------------------------------

How about even Large CLOS networks with the same interface capacity, but accounting for things to fail; fabric cards, links or nodes in disaggregated units. You can either UCMP or drain large parts of your network to get the most out of ECMP.
