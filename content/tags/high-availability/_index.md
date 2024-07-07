---
title: high availability
page_title: High-Availability Solutions
minimal_sidebar: true
layout: custom
sidebar_box: HA
---
{{<quote source="ChatGPT explaining application high availability to a high school kid">}}
High availability refers to the ability of a system or application to keep running even if there is a problem or failure. This is important because if a system or application goes down, it can cause problems for those who rely on it. To achieve high availability, multiple copies of the system or application are set up in different locations so that if one fails, the others can take over and keep things running smoothly. This helps ensure that the system or application is always available when needed.
{{</quote>}}

Before going into the details, it's worth figuring out what the application (or system) users need as opposed to what they think they need:

{{<series-listing tag="need" year="yes" weight="yeah">}}

Not surprisingly, IT vendors sell magic infrastructure solutions as the high-availability panacea based on the assumption that redundant infrastructure cannot fail. Nothing could be further from the truth:

{{<series-listing tag="fail" year="yes" weight="yeah">}}
 
### High Availability Concepts, Technologies, and Solutions

You can use a plethora of approaches depending on your availability targets:

* Disaster recovery is the right tool for the job if you're OK with the system being down for a few hours.
* Automatic restart of application instances combined with disaster recovery is acceptable if you can accept your system to be down ~0.1% of the time (99.9% availability)
* Availability targets higher than 99.9% can only be reached reliably with proper application design supported by well-designed infrastructure.

I wrote {{<page-count round="10">}} blog posts on these topics. It would be impossible to list all of them on a single page; major high-availability technologies or concepts thus have dedicated pages:

* [Disaster recovery and avoidance](/series/dr/)
* [High availability clusters](/series/ha-cluster/)
* [Public and private cloud deployments](/series/ha-cloud/)
* [Global and local load balancing with IP anycast](/series/anycast/)

One of the prerequisites for highly available services is also redundant networking infrastructure:

{{<series-listing tag="infra" year="yes" site_tag="true" weight="yeah">}}

Regardless of your approach, the only sustainable way to get highly available services is the correct design of the application stack. For more details, watch the [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar; I also wrote a few blog posts on the topic:

{{<series-listing tag="app" year="yes" weight="yeah">}}

### Notable Outages

Finally, here are a few notable outages. TL&DR: it can happen to the big guys and will eventually happen to you.

{{<series-listing tag="outage" year="yes">}}

{{<series-untagged title="Other High Availability Blog Posts" format="2006">}}
