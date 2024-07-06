---
date: 2018-09-13 07:42:00+02:00
tags:
- automation
- intent-based networking
title: 'Worth Reading: Intent-Based Networking Taxonomy'
lastmod: 2021-11-16 16:25:00
url: /2018/09/worth-reading-intent-based-networking.html
intent-based-networking_tag: overview
---
In September 2018, Saša Ratković (Apstra) published a must-read [Intent-Based Networking Taxonomy](https://blogs.juniper.net/en-us/enterprise-cloud-and-transformation/intent-based-networking-automation-taxonomy)[^1] which (not surprisingly) isn't too far from what I had to say about the topic in a [blog post](/2017/09/intent-based-hype.html) and [related webinar](https://my.ipspace.net/bin/list?id=NetAutUC#CS_INTENT).

It's also interesting to note that the first three levels of intent-based networking he described match closely what we're discussing in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course and what [David Barroso](https://www.ipspace.net/Author:David_Barroso) described in [Network Automation Use Cases webinar](https://my.ipspace.net/bin/list?id=NetAutUC):
<!--more-->
[^1]: Apstra got acquired by Juniper in the meantime, and at least some of their content (including Saša's blog post) was migrated to Juniper's web site. You can also check the [archive.org copy of the original document](https://web.archive.org/web/20180903030331/http://blog.apstra.com/intent-based-networking-taxonomy).

-   Start with basic device configuration automation;
-   Migrate from "device configurations are the ultimate source of information" to single source of truth (abstracted network and services data model);
-   Perform real-time validation of network state.

It's relatively easy to develop an automation solution that meets the first three levels of Saša's definition. After all, that's what the attendees of our network automation online course have to do during a sequence of hands-on exercises, and many of them get to the very end (testing and validation).

The final stage he's describing (self-operation, or [self-driving networks](/2017/09/self-driving-networks-with-kireeti.html) if you work for vendor J) is sometimes called event-driven automation. [David Gee](https://www.ipspace.net/Author:David_Gee) and [Mircea Ulinic](https://www.ipspace.net/Author:Mircea_Ulinic) covered the basics in the [Spring 2018 session of the network automation online course](https://automation.ipspace.net/Public:8-Event_Driven_Automation) -- just enough to show you how complex the topic can be, and how you could get started.

## Revision History

2022-06-04
: Replaced the original link to `blog.apstra.com` with a link to a document migrate to Juniper web site.
