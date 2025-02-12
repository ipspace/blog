---
kb_section: ConfigChangeLogging
minimal_sidebar: true
title: Log Changes to Router Configurations
toc_title: Introduction
tags: [ network management ]
date: 2025-02-14 08:01:00+0100
index: true
alt_section: posts
url: /kb/Internet/ConfigChangeLogging/
---
Whenever you're faced with an "unexpected" network outage that doesn't seem to be caused by a hardware failure, the root cause often tends to be a change in a device configuration, raising these questions:

* What changes were made to the device configuration?
* When were the changes made?
* Who made them?
<!--more-->
{{<note migrated>}}
This text is part of a more extensive article initially published in 2006. It was updated and republished on ipSpace.net in February 2025.
{{</note>}}

Network managers who implemented centralized Authentication, Authorization, and Accounting (AAA) with Cisco’s proprietary TACACS+ protocol could log any command executed on the routers in their network for ages[^OV]. The above questions are also easy to answer in environments using modern network automation workflows like [GitOps](/2018/08/gitops-in-networking/) ([more details](/series/cicd)), but unfortunately, many organizations are still not at that stage.

[^OV]: Several other vendors implemented TACACS+ clients. Some of them also support command authentication or accounting. A few vendors provide similar functionality with RADIUS accounting.

However, your networking vendor might have implemented some rudimentary change logging functionality in the network operating system. Cisco was one of the first vendors to do that; the Configuration Change Notification feature was introduced almost twenty years ago in Cisco IOS release 12.4.
