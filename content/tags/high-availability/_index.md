---
title: high availability
page_title: High-Availability Solutions
minimal_sidebar: true
layout: custom
---
{{<quote source="ChatGPT explaining application high availability to a high school kid">}}
High availability refers to the ability of a system or application to keep running even if there is a problem or failure. This is important because if a system or application goes down, it can cause problems for the people who rely on it. To achieve high availability, multiple copies of the system or application are set up in different locations so that if one fails, the others can take over and keep things running smoothly. This helps ensure that the system or application is always available when it is needed.
{{</quote>}}

Before going into the details, it's worth figuring out what the application (or system) users need as opposed to what they think they need:

{{<series-listing tag="need" year="yes" weight="yeah">}}

Not surprisingly, IT vendors sell magic infrastructure solutions as the high-availability panacea based on the assumption that redundant infrastructure cannot fail. Nothing could be further from the truth:

{{<series-listing tag="fail" year="yes" weight="yeah">}}
 
You can use a plethora of approaches depending on your availability targets:

* Disaster recovery is the right tool for the job in you're OK with the system being down for a few hours.
* Automatic restart of application instances combined with disaster recovery is acceptable if you can accept your system to be down ~0.1% of the time (99.9% availability)
* Availability targets higher than 99.9% can only be reached reliably with proper application design supported by well-designed infrastructure.

### High Availability Concepts, Technologies and Solutions

I wrote {{<page-count round="10">}} blog posts on these topics. It would be impossible to list all of them on a single page; major high availability technologies or concepts thus got dedicated pages:

* [Global and local load balancing with IP anycast](/series/anycast.html)
* [High availability clusters](/series/ha-cluster.html)
* [High availability packet forwarding](/series/ha-switching.html)

{{<series-untagged title="Other High Availability Blog Posts" format="2006">}}