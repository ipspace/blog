---
title: Disaster Recovery
layout: custom
minimal_sidebar: true
sidebar_box: HA
---
{{<quote source="ChatGPT explaining disaster recovery in simple terms">}}Disaster recovery is a process of restoring data and systems after a disruptive event such as a natural disaster, cyber attack, or power outage. It involves creating a plan to minimize the impact of the disaster, recovering lost data and resources, and restoring normal operations as quickly as possible. The goal of disaster recovery is to ensure business continuity, protect critical data, and minimize financial losses in the event of a disaster.{{</quote>}}

Before going into the details, let's warm up with a few introductory blog posts:

{{<series-listing tag="intro">}}

### Vendors Love Clueless Customers

Even GPT got the gist of disaster recovery right:

* Figure out how you're going to recover from a disaster (plan)
* Recover lost resources and data
* Restore normal operation

Unfortunately, that's a lot of hard work, and people believing in fairy tales have always tried to avoid that. Welcome to the "infrastructure will save the day" la-la land of vendor marketing.

{{<series-listing tag="vendor">}}

### Stretched VLANs

One of the most common "solutions" promoted by virtualization and networking vendors (and consultants drinking their Kool-Aid) is the idea to stretch VLANs across multiple data centers "to automate the recovery and avoid renumbering resources". Needless to say, both claims are totally bogus.

{{<series-listing tag="stretch" weight="yes" >}}

### Stretched Failure Domains

Stretched VLANs have a major drawback: they turn multiple independent data centers into a single failure domain. Here are a few real-life examples of what happens afterwards:

{{<series-listing tag="fail">}}

Is there anything we can do to make things a bit better? Maybe:

{{<series-listing tag="fail_fix">}}

### Faking Disaster Recovery Tests

Building an infrastructure that turns multiple locations into a single failure domain is bad. Faking disaster recovery tests on such infrastructure is even worse.

{{<series-listing tag="fake">}}

### Disaster Avoidance

Could something be worse than the stretched VLAN fairy tales? You bet. Vendors like Cisco, EMC and VMware were happily promoting *disaster avoidance*: the idea that you'd migrate your workload out of a data center that's about to experience a disaster (example: hurricane). Not surprisingly, this idea works best in PowerPoint.

{{<series-listing tag="avoid">}}

### Real-Life Lessons

I had to deal with several (non-networking) disasters over the years. Here are a few lessons I learned:

{{<series-listing tag="life">}}

### I'm Not Alone ;)

For years, I've been one of the very few vocal opponents to the "industry wisdom". Fortunately, I'm no longer alone. This is what others had to say on the topic:

{{<series-listing tag="other">}}

{{<series-untagged title="Blog Posts I Forgot to Tag">}}
