---
kb_section: MH_Redundancy
minimal_sidebar: true
title: Summary
alt_section: posts
index: true
---
The design described in this article gives you the ability to implement fully redundant Internet connectivity without having an allocated public IP address space or autonomous system number. Even better, it’s completely static on the Internet side, thus alleviating the need to configure BGP on the gateway routers. However, the simplicity of the design brings a few drawbacks as well; you should use this design only in a stable environment where the switchover from primary to backup ISP is unlikely (but you still need the secondary connection to ensure reliability), as every switchover will cause all established TCP sessions to be terminated.

The article focused solely on the primary/backup scenario. It’s possible to extend it to support rudimentary load sharing, but you have to be careful to make certain that all the IP packets between a pair of inside/outside hosts will always flow across the same gateway router (otherwise the NAT configured on the gateway router will destroy the TCP session). Similarly, it’s possible (although not trivial) to implement publicly accessible inside servers; this topic will be covered in a later article.
