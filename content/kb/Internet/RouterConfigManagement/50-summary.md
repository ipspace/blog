---
kb_section: RouterConfigManagement
minimal_sidebar: true
pre_scroll: true
title: Summary
date: 2025-01-15 08:01:00+0100
---
Cisco IOS gives you a variety of router configuration management tools. In this article, you’ve seen how to use the Configuration Change Notification and Logging feature to log all router configuration changes. You can also use this feature to send all configuration commands entered on a router to an external *syslog* server to ensure all changes to a router configuration are immediately stored in an off-site archive.

{{<note info>}}
If you want to use the configuration change logging feature as a security audit mechanism, configure *syslog* to [use TCP as the transport protocol](http://ioshints.blogspot.com/2006/10/running-syslog-over-tcp.html).
{{</note>}}

The Contextual Configuration Diff utility is supposed to give you a meaningful list of differences between two router configuration files. It’s a handy utility, but don’t expect too much from it. While it correctly identifies the changed configuration objects and lists additions and removals made to them, it ignores the order dependency of some IOS configuration commands.

The order dependency of these commands is sometimes wholly ignored (although additions and removals are correctly identified), and sometimes you’re notified that the configuration commands were reordered, but the additions and removals are incorrect. In worst cases, the change is not detected at all.

However, even with these shortcomings (and even though Cisco hasn't fixed them in almost 15 years), the Contextual Configuration Diff utility is a tool that can help immensely with day-to-day router management and troubleshooting.
