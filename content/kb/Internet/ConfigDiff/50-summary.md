---
kb_section: ConfigDiff
minimal_sidebar: true
pre_scroll: true
title: Summary
date: 2025-03-12 07:51:00+0100
---
The Contextual Configuration Diff utility is supposed to give you a meaningful list of differences between two router configuration files. It’s a handy utility, but don’t expect too much from it. While it correctly identifies the changed configuration objects and lists additions and removals made to them, it ignores the order dependency of some IOS configuration commands.

The order dependency of these commands is sometimes wholly ignored (although additions and removals are correctly identified), and sometimes you’re notified that the configuration commands were reordered, but the additions and removals are incorrect. In worst cases, the change is not detected at all.

However, even with these shortcomings (and even though Cisco hasn't fixed them in almost 15 years), the Contextual Configuration Diff utility is a tool that can help immensely with day-to-day router management and troubleshooting. It's not surprising that [NAPALM](https://napalm.readthedocs.io/en/latest/index.html) uses it when [identifying the changes it would have to make](https://napalm.readthedocs.io/en/latest/support/index.html) to Cisco IOS router configurations.
