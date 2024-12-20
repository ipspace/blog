---
kb_section: ConfigChangeLogging
minimal_sidebar: true
pre_scroll: true
title: Summary
date: 2025-02-12 08:01:00+0100
---
Cisco IOS gives you a variety of router configuration management tools. In this article, you’ve seen how to use the Configuration Change Notification and Logging feature to log all router configuration changes. You can also use this feature to send all configuration commands entered on a router to an external *syslog* server to ensure all changes to a router configuration are immediately stored in an off-site archive.

{{<note info>}}
If you want to use the configuration change logging feature as a security audit mechanism, configure *syslog* to [use TCP as the transport protocol](http://ioshints.blogspot.com/2006/10/running-syslog-over-tcp.html).
{{</note>}}
